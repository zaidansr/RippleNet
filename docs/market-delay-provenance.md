# Matched-origin delay study: fresh market-data provenance

**Attribution and license:** This document concerns Binance Vision BTCUSDT spot daily individual-trades archives for 16 September–15 October 2017. Sources: [Binance public-data repository](https://github.com/binance/binance-public-data), [archive directory](https://data.binance.vision/?prefix=data/spot/daily/trades/BTCUSDT/), [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md). This document and its data-derived acquisition findings are distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: integrity and acquisition metadata were computed; no raw trade rows or prices are reproduced here. This notice does not relicense independently written project code or imply Binance endorsement.

## Fixed fresh dates and information boundary

The new source period is thirty consecutive UTC days, with no overlap with the preceding 17 August–15 September study. Dates and split were publicly frozen in [plan commit 1cdfb3d0fe3eed36e1892d10c4c7c78ec84be3c6](https://github.com/zaidansr/RippleNet/commit/1cdfb3d0fe3eed36e1892d10c4c7c78ec84be3c6) before trade ZIP bodies were acquired:

- Training: 16–25 September 2017, ten days.
- Validation: 26–30 September 2017, five days.
- Protected test: 1–15 October 2017, fifteen days.

The prefreeze preflight used only official documentation, ZIP HEAD requests and checksum sidecars. It accessed no trade ZIP bodies. After the public plan freeze, all thirty previously unused date archives were downloaded without substitution. The acquisition worker streamed uncompressed CSV bytes for hash and CRC only, without decoding or parsing trade records from any split. It inspected no prices, features, targets, losses or model-selection outcomes. Later development and final access belong to the root-controlled frozen execution stages; integrity acquisition does not itself open a predictive evaluation.

## Terms and bounded acquisition

Official dataset terms were rechecked on 7 November 2026. The access-time snapshot is version 1.0, updated 26 August 2026. Its free-access, specified noncommercial research and derivative attribution/share-alike provisions support the declared noncommercial historical study and appropriately licensed publication. These are dataset-specific conditions, not unrestricted commercial permission or an inference from the README's code-license heading. [Official terms](https://raw.githubusercontent.com/binance/binance-public-data/master/TERMS_AND_CONDITIONS.md)

Privately retained terms SHA256: `99c4921dbe023cd68c1a447775707d621453cc78aec6ac0bfe2e6c06a5114ee0`. Privately retained README SHA256: `2e133d9945a9263a02781369078e72805eff074680f305cd5460016471c6caad`.

Fixed limits were **2 MiB ZIP per day, 20 MiB expanded per day and 60 MiB ZIP total**. Actual acquisition totals were **4,443,875 compressed bytes** and **18,294,022 expanded bytes**. The largest ZIP was 240,899 bytes; the largest CSV was 1,024,173 bytes. No limit expanded and no source/date failed or was replaced.

Acquisition started at `2026-11-07T15:58:37.688742+00:00` and finished at `2026-11-07T15:58:48.186131+00:00`. Each ZIP matched its preflight-pinned publisher SHA256 sidecar. Each contained one expected unencrypted CSV member in supported stored/deflated form and passed bounded streamed decompression/CRC verification. These checks do not assert that every row meets the parser contract; row-level validation remains part of the later authorized importer run.

Private artifacts are in workspace `work/market-delay/data/`, outside the public repository. Names are `BTCUSDT-trades-YYYY-MM-DD.zip` and the same name plus `.CHECKSUM`. The private `download-manifest.json` records dates, split, source URLs, local paths, archive/CSV hashes, sizes, source-term metadata, retrieval times, HTTP headers and integrity flags. Its acquisition flags explicitly state that no trade records were parsed at this stage. Raw data and copied vendor snapshots are not published here. No account, API token, provider contact, purchase or paid service was used.

## Pinned versions

For each date below, the archive URL is `https://data.binance.vision/data/spot/daily/trades/BTCUSDT/BTCUSDT-trades-YYYY-MM-DD.zip`; append `.CHECKSUM` for its publisher sidecar. Every file was acquired after the public plan freeze rather than reused from a prior price inspection.

| UTC date | Split | ZIP bytes | Archive SHA256 | CSV SHA256 |
| --- | --- | ---: | --- | --- |
| 2017-09-16 | train | 134170 | `abd546a555a3137c66f081768f2d23b9e988bf9720b28d20991bbe7d58cf0eba` | `b2636ed9ff6887aa7f3a6a2cdacd0089656ba75a1b8a031738e0209e6c2ac2c8` |
| 2017-09-17 | train | 98006 | `24a22a085abbbf405c20f9888bb4aeee9d6a2c67178af9abcbf623ce5b8b9b0c` | `447dd13497f330e7d2bfe61a9f7dffd6dc621e1899f127f8cf2774244c7cff88` |
| 2017-09-18 | train | 134626 | `965a061cb25a1e16c3aafb9188451a104a62a7940d4be4367aec02f84fed5fec` | `3c091ab01a1975b32ed5eaf7d4960d75691e163569f69f147ec84661db1855bb` |
| 2017-09-19 | train | 123964 | `68f0f54feaaa0594b0bd9e6680014858b3c47f9a5034ed18748e2a3f7d7d84b6` | `b24661947e363296c415b9982c5d02e0ab76fa85c6ceb4f3f06bddbf34ec1dbb` |
| 2017-09-20 | train | 125278 | `626b13e233258c9fcc0bd85ef646fb5ff3c386d8d79a9bece9eb8adc21522ffb` | `180ac27d0a355cd2f473e29c307f0193d38457fd252ad04cbb70d3581908dedd` |
| 2017-09-21 | train | 145794 | `a2be549ccbb22fe2bfb1d98926a87665c626de846d83c1eefc3597663f0ab8a5` | `c20be1e13da01b2f06b44bcd5d441b1d35761e153a9358a55c184f470c56e1d1` |
| 2017-09-22 | train | 139845 | `f938d156b3b47412805bd30394f342130d9af54b53adc8263689792b104760d5` | `c23141929a5aa2683067e297656bb94f5baad008be990044c2f4ee913bc27145` |
| 2017-09-23 | train | 144379 | `173bd5da257e14996bd03bf28adeb272991c8dd91f10be6fa8a3410f8d8c6aaa` | `cf47b1df5a20e3177b1c4d664ff448617f347221ad09748a1022dc3557a28dcf` |
| 2017-09-24 | train | 144242 | `e8c0fbe998182d841b3ac49ca2337b2a90c1851a76bb2b051709641b39aa2398` | `ed742bb263a9ad12130051c58362f9b2ee9719af832874b9203b70ff2d9c772a` |
| 2017-09-25 | train | 156164 | `d4c1cb840f555163c056a39b833f5daf76d6d0720f594e140cd3474a37cca73b` | `7906b631857624933bd896479ea8ed5b4113be5da6bd8101592c9ebe72ad0021` |
| 2017-09-26 | validation | 130436 | `1953b1396e86a66d5a18580bc3c9a6657656646b693dd33a6b2c8eb658a64f6e` | `834db8dc287e06e7005aa85ca2a7a3df9334b0961e862b0e822877c29c0f88ff` |
| 2017-09-27 | validation | 133209 | `243add620c1d03ff6f958f9d504dc5c06bdea8c345844b2f4b6135763b5e6fd6` | `69ebc77571ee4b99d95ad877b850b96ce21dcbca3c4b0b11b02f99d389c75dc2` |
| 2017-09-28 | validation | 182974 | `f5fb9b158a0642214c1af7e82b8372b6e6986b818e23f2e14cff80c2e3e31ca6` | `9c8d1d01620b3173458034d83cfbeb1fb35aa3dc2ce3e43556ef686a8fb65b9f` |
| 2017-09-29 | validation | 240899 | `abc10d41c5decf4766f4d599a3a207ed5f272d1cc36150d947edf391fe4c4c0a` | `6ff47be51d84e89f5d539187b5bae871f5d8d727c8c21631ea77f377938a1b4d` |
| 2017-09-30 | validation | 158161 | `321125b45fed350a907d9c7d29881267aa8d3002bc2911ee6dd330e5164abeac` | `3e2f668edab5b061309ae95bfabaa6f80dd0a85a9e681540081ecd9028c2b7b3` |
| 2017-10-01 | test | 164599 | `95121a7a4bd4a159817bd70a6209f246a108a816fd1ca78bee1fa46540512c5f` | `90d04742d4b8cf445e7ffec46d97e90aa695a911fd90fc40ccdb23bd74b9426c` |
| 2017-10-02 | test | 135851 | `99700ac5053aea321da082c96b2b2a9b13d6fee2966b52ee024ed3b29ac364c9` | `464eebdc3fc9fcd862acb10669dc115c8c579a1199e9df288c2a24476ab8536e` |
| 2017-10-03 | test | 201678 | `a3e4766cab90c56bb4e4fb840066945abd1e22d3c365698db7361dc81703a6dd` | `8ea763a18c048c771c15035934c7c3b5512dc69a0692643d09f5a19fca296e70` |
| 2017-10-04 | test | 181998 | `3d96d77c7a74f976e59ac53dac00f7a8a708619fef05bba18543599b09de00a6` | `d4cc90d5f0b7f2e8e2a7cc7be0a8d637c5b77c52a334dafa731b4899d3b6ef86` |
| 2017-10-05 | test | 151803 | `e47b465def8dbee353daf7f6e523e4660cea6b05854b64570aab7fcfe8100413` | `bcd06fa5024a1946b6557a96a38e75d63f6c83dcdbe641b4bb28b579172f167a` |
| 2017-10-06 | test | 107337 | `17edb60049d6b36faac39b36400c8edcf1d68786518b29fb109aa64b841a896e` | `17d93ec4aba9990da509df03097cd9e02925525f26e8850c044fb348942290b7` |
| 2017-10-07 | test | 81162 | `04b0d4899dc757e74cec613fba5b11d3f750ed2878e32a37cd978bffec07f134` | `2aaee223b4dac50148b6d63b03024971f23be019b791d3fb0a6e39decb6e8213` |
| 2017-10-08 | test | 122010 | `9feb3c953bce9dbbcbf3e7448a32b27a78dd9486c60b167ff54b74ec0ba4409f` | `f2f6ab49b2d054d286b0d721812ce8f167a90a1612c9d56c1562a68fb02546c3` |
| 2017-10-09 | test | 176525 | `d1190fd3b7428bc678b9f70f1806e25fdc9cf39e0277975e3cf7fd6d2422426e` | `fb932afeda0c9977cf6f43e4b1ee60159f878e3282f32320798a254cae9cccaa` |
| 2017-10-10 | test | 201524 | `2964175491d5fe9faefdb99f12527d20f9bd391d78f8f0104b01a935ae13efbe` | `5361c4ce769d9a0c69e637a2a51217c21caff2c3ab18d23fe0e376ccd6717e5f` |
| 2017-10-11 | test | 97148 | `8aa27f5e5b9f092ea8e48df682d5a108c1bb0c3e4ee7c27e68d04edfd1febf22` | `c32f1dda2eb8be17ca2f379fa94375532cca019d667c43662ab17f4a62279f30` |
| 2017-10-12 | test | 141666 | `08a7c5e847bc34db3bdb259d04c1c23ac59b2fa36710dae99939a568e83733f4` | `3af4dfcd7f7681da7c0fc576f1e3c964f5504df148c1ae4fd38c91c71914c0f2` |
| 2017-10-13 | test | 218731 | `7956e57ff91bcc2a97036e57b5f9b46bd60fa95e3762859b12534ae171ea72a5` | `3ec24f3e7f0d5ab890f15aea27e72bbd6f7dec300c3fe3e2748ba02ebd658572` |
| 2017-10-14 | test | 124524 | `b303cc4b27b03f264910e475c49e647a3ef01c9f075abb31e404be854ba36429` | `9f2b1ddcf494544550224f294ff02f833520bfbd1ee614938267f67d60dc9c91` |
| 2017-10-15 | test | 145172 | `cdabc09793d237e38e3307117550f0f6082642837cad839fdc478d7480cf0639` | `b2d4d7b18c0a45e2b304bf4451e792439cdabb48f352ab754b7fba04aaccdde6` |

## Scope of any subsequent result

The [official README](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md) documents the individual-trade schema, checksum sidecars and possible later archive updates. These historical spot dates use the millisecond regime; microseconds begin in the documented 2025 archive regime. The importer must still preserve ties/file order, validate each declared UTC day and retain censored or failed-origin coverage.

Checksums pin the acquired historical-file versions, not original online publication. No receiver-time record, contemporaneous revision ledger, independently adjudicated error/shock label or latent efficient price is supplied by this download. A protected chronological evaluation can therefore support a scoped retrieved-trade-price forecasting comparison, not an original as-of backtest, cause identification, executable profit or broad market generalization.

The matched-origin target definitions, delay contrasts, preprocessing, model selection, code freezes and statistical analysis belong to the [study plan](market-delay-plan.md) and later execution artifacts. This provenance document reports acquisition metadata only and contains no fitted model, forecast result or outcome-driven date choice. Any downstream data-derived publication must preserve attribution, the applicable CC BY-NC-SA 4.0 conditions and the declared development/test separation.
