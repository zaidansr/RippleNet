"""Invented clocks/prices; no vendor records or trained parameters published."""
import gzip
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from ripplenet import quote_study as q


def session(day: str) -> q.Session:
    k = np.arange(50, dtype=float)
    return q.construct(day, np.exp(.01*np.sin(k)+.001*k), np.exp(.008*np.sin(k)+.001*k), np.full(50, .01))


def manifest() -> dict:
    return {"files": [{"date": d, "kind": k, "sha256": "0"*64, "csv_sha256": "1"*64,
                       "compressed_bytes": 1, "expanded_bytes": 1} for d in q.DATES for k in ("trades", "quotes")]}


class QuoteStudyTests(unittest.TestCase):
    def test_strict_ties_invalid_latest_and_age_boundary(self) -> None:
        s = q.Series(np.array([0, 1_000_000, 1_000_000, 2_000_000]),
                     np.array([100., 101., np.nan, 103.]), np.zeros(4), np.array([True, True, False, True]), {})
        grid = np.array([0, 1_000_000, 1_000_001, 2_000_000, 2_000_001, 4_000_000])
        p, _ = q.snapshots(s, grid, 1_000_000)
        assert_allclose(p, [np.nan, 100., np.nan, np.nan, 103., np.nan], equal_nan=True)
        c = q.snapshot_counts(s, grid, 1_000_000, p)
        self.assertEqual(sum(c[k] for k in ('missing_predecessor','invalid_latest_state','over_age_limit','valid_snapshots')), len(grid))

    def test_exact_twelve_features_and_ten_clock_target(self) -> None:
        k = np.arange(40, dtype=float)
        lt, lm = .01*k*k, .005*k*k
        s = q.construct('invented', np.exp(lt), np.exp(lm), np.full(40, .02))
        self.assertEqual(s.x.shape, (35, 12))
        assert_allclose(s.x[0, :5], np.diff(lt)[[4,3,2,1,0]])
        assert_allclose(s.x[0, 5:10], np.diff(lm)[[4,3,2,1,0]])
        assert_allclose(s.x[0, 10:], [.02, lt[5]-lm[5]])
        assert_allclose(s.y[0], [lt[15]-lt[5], lm[15]-lm[5]])
        self.assertEqual(s.coverage['paired_scorable'], 25)
        self.assertEqual(s.coverage['session_end_censored'], 10)
        for v in (s.x,s.y,s.scorable): self.assertFalse(v.flags.writeable)

    def test_future_missing_label_cannot_remove_earlier_issued_forecast(self) -> None:
        p, m = np.exp(.001*np.arange(40)), np.exp(.002*np.arange(40))
        a = q.construct('a', p, m, np.full(40,.01))
        changed = m.copy(); changed[15] = np.nan
        b = q.construct('b', p, changed, np.full(40,.01))
        assert_array_equal(a.x[0], b.x[0])
        self.assertTrue(a.scorable[0]); self.assertFalse(b.scorable[0])
        self.assertEqual(sum(b.coverage[k] for k in ('paired_scorable','session_end_censored','future_reference_unavailable')),len(b.x))

    def test_equal_session_weighted_mean_median_and_intercept(self) -> None:
        a = q.Session('a',np.zeros((2,12)),np.ones((2,2)),np.ones(2,dtype=bool),{})
        b = q.Session('b',np.zeros((10,12)),np.full((10,2),3.),np.ones(10,dtype=bool),{})
        model = q.fit_grid([a,b],0)[-1]
        self.assertAlmostEqual(model['target_mean'],2.)
        self.assertEqual(model['target_median'],1.)
        assert_allclose(model['feature_scale'],np.ones(12))
        assert_allclose(model['beta'],np.zeros(12))

    def test_weighted_ols_known_coefficients_and_gap_baseline(self) -> None:
        x = np.random.default_rng(19).normal(size=(100,12)); beta=np.arange(12)*.001
        y = np.column_stack((.2+x@beta,.1-x@beta))
        s = q.Session('s',x,y,np.ones(100,dtype=bool),{})
        model=q.fit_grid([s],0)[0]
        self.assertLess(q.score(s,model,0)['candidate']['mse'],1e-25)
        g = q.Session('g',x,np.column_stack((-x[:,-1],np.zeros(100))),np.ones(100,dtype=bool),{})
        self.assertEqual(q.score(g,model,0)['gap']['mse'],0.)
        self.assertEqual(q.score(g,model,1)['gap']['mse'],0.)

    def test_bounded_gzip_reader_enforces_expansion_before_decode(self) -> None:
        payload=gzip.compress(b'abcdefghij')
        with gzip.GzipFile(fileobj=io.BytesIO(payload)) as raw:
            reader=q.BoundedExpansion(raw,10)
            self.assertEqual(io.BufferedReader(reader).read(),b'abcdefghij')
            self.assertEqual(reader.count,10)
            self.assertEqual(reader.hash.hexdigest(),hashlib.sha256(b'abcdefghij').hexdigest())
        with gzip.GzipFile(fileobj=io.BytesIO(payload)) as raw:
            with self.assertRaises(ValueError): io.BufferedReader(q.BoundedExpansion(raw,9)).read()

    def test_manifest_exact_dates_files_and_byte_bounds(self) -> None:
        m=manifest();q.validate_manifest(m)
        m['files'][0]['expanded_bytes']=257*1024**2
        with self.assertRaises(ValueError):q.validate_manifest(m)

    def test_actual_gzip_parser_preserves_invalid_latest_and_rejects_blank_rows(self) -> None:
        day='2025-06-01'
        start=(q.date.fromisoformat(day)-q.date(1970,1,1)).days*86400*1_000_000
        header=','.join(q.HEADERS['quotes'])+'\n'
        rows=[f'kraken,XBT/USD,{start+i},{start+i},1,{ask},{bid},1\n'
              for i,ask,bid in ((1,101,99),(2,101,102),(3,102,98))]
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'quotes.gz'
            payload=(header+''.join(rows)).encode()
            path.write_bytes(gzip.compress(payload))
            series=q.read_series(path,'quotes',day,q.digest(path),hashlib.sha256(payload).hexdigest())
            assert_array_equal(series.valid,[True,False,True])
            self.assertEqual(series.diagnostics['expanded_bytes'],len(payload))
            p,_=q.snapshots(series,np.array([start+3]),1_000_000)
            self.assertTrue(np.isnan(p[0]))
            with self.assertRaises(ValueError):q.read_series(path,'quotes',day,q.digest(path),'0'*64)
            path.write_bytes(gzip.compress((header+rows[0]+'\n'+rows[1]).encode()))
            with self.assertRaises(ValueError):q.read_series(path,'quotes',day,q.digest(path))
        m=manifest();m['files'][-1]=m['files'][0]
        with self.assertRaises(ValueError):q.validate_manifest(m)

    def test_private_guard_blocks_model_artifacts_inside_repository(self) -> None:
        with self.assertRaises(ValueError):q.private_output(q.ROOT/'results'/'trained-model.json')

    def test_development_test_separation_hashes_and_no_refit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);mp=base/'manifest.json';mp.write_text(json.dumps(manifest()))
            opened=[]
            def load(data,m,day):
                opened.append(day)
                return session(day)
            with patch.object(q,'load_session',load):
                out=base/'private'
                h=q.development(base,mp,out)
                self.assertEqual(opened,list(q.DATES[:9]))
                selection=json.loads((out/'selection.json').read_text(encoding='utf-8'))
                for key in ('feature_mean','feature_scale'):
                    self.assertEqual(selection['targets']['trade']['model'][key],selection['targets']['midpoint']['model'][key])
                opened.clear()
                with patch.object(q,'fit_grid',side_effect=AssertionError('No test fitting')):
                    result=q.test(base,mp,out,h)
                self.assertEqual(opened,list(q.DATES[9:]));self.assertEqual(len(result['daily']),3)
                with self.assertRaises(FileExistsError):q.test(base,mp,out,h)
                (out/'test.json').unlink()
                with patch.object(q,'load_session',side_effect=AssertionError('Must fail before test data')):
                    with self.assertRaises(ValueError):q.test(base,mp,out,'0'*64)


if __name__=='__main__':unittest.main()
