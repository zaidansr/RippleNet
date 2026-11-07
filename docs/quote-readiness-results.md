# Paired trade/quote readiness outcome

The fixed free Tardis Kraken XBT/USD sample for **1 June 2026** was acquired and inspected successfully. It contains real trades and reconstructed best bid/ask quotes for the same spot product. This passes a bounded access/schema/alignment gate; it is not a new forecasting result, a trained RippleNet or validation of a latent cause mechanism.

**Source and publication scope:** [Tardis Kraken documentation](https://docs.tardis.dev/historical-data-details/kraken), [current terms](https://docs.tardis.dev/legal/terms-of-service). Findings below are aggregate research statistics computed from the sample, not raw rows, an aligned event dataset or trained model parameters. No open-data license is claimed. The Binance CC notice does not apply to these findings. Raw records, vendor snapshots and detailed inspection artifacts remain private; eligible reports and independently authored general code may be published under the source-specific conditions.

## Frozen acquisition and actual evidence

The [acquisition plan](quote-acquisition-plan.md) was published as `6fed87f6b17d930d721b1c7387a0f56cf81638e2` before requesting data bodies. Both exact first-of-month sample URLs returned HTTP 200 without an API key, account or payment. No date, instrument or provider was substituted. The two compressed files total 12,460,410 bytes; expanded CSV totals 78,513,685 bytes. All advertised MD5 checks and complete gzip integrity checks passed within every frozen byte/row cap.

| Check | Trades | Quotes |
| --- | ---: | ---: |
| Recorded rows | 73,704 | 862,680 |
| Invalid value rows | 0 | 0 |
| Collector-time backsteps | 0 | 0 |
| Adjacent collector-time ties | 37,564 | 8,798 |
| Missing trade IDs | 73,704 | Not a trade-ID feed |

Actual headers match the documented trade and quote schemas, with integer microsecond exchange and collector timestamps. Both files identify `kraken` and `XBT/USD`. No locked/crossed quote rows were found in this sample. These checks do not certify economic truth, completeness or another day's data quality. [Detailed acquisition and schema audit](quote-sample-audit.md).

## Backward alignment

For each trade, the audit selects only the last supplied quote with a **strictly earlier collector timestamp**. The independently reproduced rule is equivalent to:

```python
index = np.searchsorted(quote_local_times, trade_local_times, side="left") - 1
```

No nearest-time join, sorting, deduplication or future quote is used. The most recent preceding quote would be counted as invalid rather than bypassed if invalid; this sample has no invalid quotes, so it does not exercise that branch.

| Preceding-quote diagnostic | Trade count |
| --- | ---: |
| No strictly earlier quote | 1 |
| Age at most 100 ms | 39,911 |
| Age over 100 ms, at most 1 s | 27,080 |
| Age over 1 s, at most 5 s | 6,423 |
| Age over 5 s | 289 |

Thus **90.89%** of trades have a strictly preceding quote observed within one second. This is a coverage diagnostic, not a chosen forecast filter or proof that an older unchanged quote is invalid. For 2,688 trades a same-collector-time quote exists and is deliberately excluded as ambiguous. Supplied order within each file does not resolve cross-file ties.

## Material limitations

All trade IDs are empty. There are 381 consecutive identical trade CSV rows, preserved as supplied; without source identifiers we cannot determine whether these represent distinct executions or duplicate feed records. Do not manufacture unique exchange IDs or deduplicate them into a cleaner-looking market.

The quote reference is reconstructed from exchange L2 messages. CSV processing, omitted disconnect markers, revisions, separate channel collection and clock synchronization assumptions remain relevant. The timestamp is the provider's collector clock, not a demonstrated receipt/processing time for a particular trading client or an exchange-wide total order. Hashes pin this retrieved version rather than proving its original publication history.

One session does not establish sufficient independent data, statistical power, useful headroom, generalisation, a viable trading strategy or recording-error/genuine-shock ground truth. This new Kraken/USD source and period must be evaluated internally; it cannot serve as a quote ablation for the old Binance/USDT sessions.

## Decision and next operation

Proceed toward a **separately frozen multi-session collector-clock comparison**, conditional on the same access and rights checks. Before opening additional outcomes, specify the dates and protected split; common clock grid, horizon and delayed-start control; strict tie/latency, age, invalid-book and outage rules; and one identical full-information feature vector for compared methods. A full-input linear baseline is essential. Score MSE and MAE with explicit reference denominators and coverage; define practical relevance from intended use rather than reuse a synthetic threshold. The [comparison contract](quote-comparison-contract.md) lists these gates.

The inspected June 1 session is now disclosed development material. It must not be presented as an untouched protected test for design choices informed by this audit.

Any fitted parameters, model-bearing configurations and raw/event-level outputs from this source must stay private. Publish general code and qualifying aggregate reports, rather than copying the former Binance model-JSON publication pattern. No model was fitted or forecast target evaluated in this audit.

The engineering subagent performed the bounded inspection. The [independent review](quote-sample-review.md) rebuilt integrity, parsing, validity and alignment checks from both files; a separate root implementation also reproduced every age band. The mathematical subagent established the clock/target contract. Existing executable research modules and numerical findings are unchanged, so their tests were not rerun for this documentation-only publication. No spending, paid service, account or provider contact occurred.
