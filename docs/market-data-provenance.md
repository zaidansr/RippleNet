# Real recorded-trade study: data access and provenance

**Attribution and license:** The acquisition metadata below concerns Binance Vision BTCUSDT spot daily raw-trades archives for 17 August–15 September 2017. Dataset source: [Binance public-data repository](https://github.com/binance/binance-public-data), [archive directory](https://data.binance.vision/?prefix=data/spot/daily/trades/BTCUSDT/), [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md). This document is distributed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Changes: file-integrity and acquisition metadata were calculated; no raw trade rows are reproduced here. This notice applies to this document and its data-derived findings, not independently authored project code. No Binance endorsement is implied.

## Scope, terms and chronology

The user authorized a real recorded-market-data study. Current official dataset terms were rechecked on 7 November 2026 before acquisition. The retrieved version is 1.0, updated 26 August 2026. Its free-access, noncommercial-research and derivative attribution/share-alike provisions support the declared noncommercial historical study and appropriately licensed derived publication. This is not unrestricted commercial permission. [Official dataset terms](https://raw.githubusercontent.com/binance/binance-public-data/master/TERMS_AND_CONDITIONS.md)

Access-time source snapshots are privately retained. Terms SHA256: `99c4921dbe023cd68c1a447775707d621453cc78aec6ac0bfe2e6c06a5114ee0`. README SHA256: `2e133d9945a9263a02781369078e72805eff074680f305cd5460016471c6caad`.

The final 30-consecutive-day dates and 10/5/15 chronological split were published in [plan commit ad52381d89716c20076d07333f8656c97fa415cd](https://github.com/zaidansr/RippleNet/commit/ad52381d89716c20076d07333f8656c97fa415cd) before new trade bodies were downloaded. An earlier five-date candidate was expanded during metadata-only planning; no newly protected prices or targets had been inspected. The previously disclosed 17 August engineering sample remains training-only.

- Training: 17–26 August 2017, ten UTC days.
- Validation: 27–31 August 2017, five UTC days.
- Protected test: 1–15 September 2017, fifteen UTC days.

The preflight read only official terms/README, ZIP HEAD metadata and checksum sidecars. All 30 dates were available, with no alternate date or provider substituted. At this acquisition stage, ZIPs were downloaded and their CSV bytes streamed for CRC and SHA256 only: no trade CSV was text-decoded or parsed, and no protected test prices, features, targets or losses were inspected. Opening protected trade records remains a separate, root-controlled step after executable/model-selection freezes.

## Bounds and integrity checks

Limits were fixed at 2 MiB compressed and 20 MiB expanded per day, with a 60 MiB total compressed cap. Actual totals were **2,750,794 compressed bytes** and **11,287,422 expanded bytes**. The largest ZIP was 166,316 bytes and largest CSV 723,520 bytes. No bound expanded, file failed, account was created, provider contacted, or paid service used.

Acquisition occurred on 7 November 2026, 06:56:14–06:56:22 UTC. The 17 August ZIP was reused from its prior private inspection only after matching the current pinned publisher checksum. Remaining ZIPs were fetched after the public plan freeze. Every ZIP matched its independently retrieved `.CHECKSUM` sidecar; each had one expected unencrypted CSV member using supported compression, stayed within its expanded-size bound, and passed streamed CRC verification. These are byte-integrity checks, not a row-schema or original-online-availability certification.

Private files are in workspace `work/market-study/data/` outside the public repository, named `BTCUSDT-trades-YYYY-MM-DD.zip` with a matching `.zip.CHECKSUM`. The private `download-manifest.json` records source URLs, split roles, exact paths, byte sizes, archive/CSV hashes, source terms, retrieval mode, HTTP metadata and integrity flags. It explicitly records no parsed trade records at this stage. Raw archives and vendor snapshots are not committed to the public repository.

For each table date, the ZIP URL is `https://data.binance.vision/data/spot/daily/trades/BTCUSDT/BTCUSDT-trades-YYYY-MM-DD.zip`; append `.CHECKSUM` for the publisher sidecar. Checksums below pin the acquired versions.

| UTC date | Split | ZIP bytes | Archive SHA256 | CSV SHA256 |
| --- | --- | ---: | --- | --- |
| 2017-08-17 | train | 63039 | `a23fe0dae54b7143d5cffb42184e1a05afe7124aaca641cd438297ce83c9f9ec` | `f1ca7241eba6cf27aac03ac32bea5c4e8a7c88b725b8f2f6276e6b178230d557` |
| 2017-08-18 | train | 95776 | `7f1328d09ff839d498506be281306305f453da632e18a7a15437b78df14bc198` | `949cdfd7fe2e81a04fed327d39841bf2e74ab4e2849fb386a298ae6c20be894c` |
| 2017-08-19 | train | 40219 | `ff74fae2822aea541f55e68c9b3c7c6387f636827f403239869aa2be7578d6a6` | `51503dcf2df972ca42e2dad390599f18d11aa8d541744ffd411b1403db03f59c` |
| 2017-08-20 | train | 43413 | `8902250178bf7ef8d60732af4102b893727428d95f34d9aa5c43486bc3922cff` | `93f21c4adaadd1000057dc5b7e04afcb85f04f98c71aa765599e07a423c0daae` |
| 2017-08-21 | train | 70078 | `04147153807da8cbae39cbd34157957ee7bf91e8a54f9ca5d310a5f7f5d113ac` | `b5ac93ee415e2750b402e0f2aa39129e0f4c9b7a8d49db0894d3b8ba94c6524a` |
| 2017-08-22 | train | 109928 | `0ed6f3837db30630e31ff7e00d8b940022cd674858591f463e2ad8b052c014ab` | `6c9c15da766e09f6ee73b70b87b7785f43a9554096600f5ba984272c8d92d9f7` |
| 2017-08-23 | train | 138575 | `d8efb694e0b601c5ab66e016082e43af1f7d026e30000405cbd529ecba5d199e` | `5f5b2c3f0b50f82dc4f3745686d2d03bfd935b88b8c51526a30c01f2ada15688` |
| 2017-08-24 | train | 108930 | `0b27b5fc99f843f4305b106b1a189f19b7d7c4581908d20d641a663d5ec0b911` | `29d53481ffc0656b4150c050cf3ad05a55fb9e6b4bf254a7d24ccc09974a8d8c` |
| 2017-08-25 | train | 101019 | `8efbbd8118e17f4f46cb13705d1d55a7abe858021cd9f07480985541db35ffcd` | `34091b09050b49b3c913b60992810a3430462ba0edbb98754a5818b1120fcb60` |
| 2017-08-26 | train | 39755 | `7327a039f34fb7b38805bfeb98cd837820bc1e6ca6711caf93bc1d5714b1848e` | `0c28354bf5c24c933dba2fa99d7e5ff426f9fea20b9883a12aa083b144c918b3` |
| 2017-08-27 | validation | 59752 | `6a2f70927a029dc4cfd0c63b779cf3b8d26628148f6d54f0e1417fda0df0aedb` | `07672177a7b3a9f4a641ba90e9151b61c1d796472a09418617f2bf7a24188c12` |
| 2017-08-28 | validation | 73386 | `da96fc891328d9f593b84e0444761ffd04f8e1e94e4794f9ef81f9643ec3b6c0` | `21f016619a610c88a75fbb9238e5c29279b0fbf0190e7547c1e5620298b49109` |
| 2017-08-29 | validation | 71699 | `7f34c8d127cd8fb2ce82aa4b949ef4adeae5a8bc70ec8232d7a75d7faee242c9` | `0aa7b5e0544f866d936a210f39582ed9164a6a6dc2278452f91758b4273706a3` |
| 2017-08-30 | validation | 90252 | `d48e171332b08039ee18c03f44cbd5f48bfd4de75eebf17825fd4dd4b6756d3a` | `4805bcfda12f9f64ba77ee0280fa4a89d856e07867927c0b4c2df496b5babcad` |
| 2017-08-31 | validation | 70346 | `4f8c2910c28bb31a031516ccccfee26a65d551829e817175f7d210cc9869a0d4` | `9a3681fd70e3579dd40f4a8416e94bb319ca56049d3109b487e499eeb74e0892` |
| 2017-09-01 | test | 69645 | `5423da7aabd72711e35fb657b32e78c189b4eb27349b8c9111845df59a03df0a` | `d9c6209d4d150e3940c29f4d0de212d3324354b36c4c681f4dcf9cb131ccc068` |
| 2017-09-02 | test | 116989 | `76bb6e477cf134311ada3be8191db9bb25f2f12bc117fc70828df0cd82b12c08` | `809a9bc579c0b2c21182475255f4fb81bea9d63a0de44f843971d028d93f6e51` |
| 2017-09-03 | test | 99094 | `d1ad9fb5c80b3d3091487d1f47194a65450198314c094ebcda0f2c8bdc490c51` | `097c9e327e6e7d9bb1c6446e77a0130ddb6d6d9c18be5a275502197a64efab1d` |
| 2017-09-04 | test | 151822 | `dfb13d2d5108c65429ee0d0e84e5706740c20c1c015d079654cb3f4f6f62a267` | `c8a48eaaf4fd2514ab43a1a404fac5006402daff9ec200a8ddecda4b4da83b86` |
| 2017-09-05 | test | 159698 | `d5710f134401abb29edf3e155c487a810d79a692534d784472ef91a84c1e3239` | `a3edcaa08191f3ef819bd657e4ee42d5e862a7b11c5af2ac8fde06596fdab4ab` |
| 2017-09-06 | test | 123850 | `0854b45fa6cdc45a7dab85f75e8f7e9257c474eef242ac181e1c82351b3eceb8` | `a11c3dfd3b3803242496cf5df3ca018738135959ee989e682d73ad74ef66e183` |
| 2017-09-07 | test | 56808 | `09fad125efacfeb77478ea92ec05e076425bdff601cf3a7f9fb12147d12846bf` | `fd4c6d24c7f8bf91d021b7a2d29983d5324d5f932603818f2dc710c75a306c88` |
| 2017-09-08 | test | 89090 | `d8ee766cf053c55fcb0139d7f0c9cee32f1aeeb9c35bf48a2084b6e19f08766c` | `d4cf2a92dd66540e248ace4d711c6e1dfbafccd46d4fdc095244d3a5297c6e59` |
| 2017-09-09 | test | 71796 | `4373e35f7bac4985aa54cc0ef39557883654ae137b941210be18d6b199c3530a` | `e5edaa3b768b902a9f8f132863882ad0935111f765c18d59330ad3ff7c7f80aa` |
| 2017-09-10 | test | 65272 | `57441317b49982ca85d5b460e298fa4f94bfca25f18c2109a37e7d10127fed2c` | `dbe6ee59749cf2d4e581fadd7bdfde691c09be7ea0d9572f3b7c8ce950eff89b` |
| 2017-09-11 | test | 77181 | `97852184f57fd0f928d043b8115d28de99a6766b253ea5b994898e0a5736563a` | `55f1e1eff8b8076feb037644e6ed4d431ff8d5a4a493bbd4a7b33367a4614256` |
| 2017-09-12 | test | 110751 | `a3dc4410afc3f84f377fb2cc5c002e76ee49b899779a5c68d691685baa52e272` | `12288986aac339a3d5a01ca17be249c679abfdf6b9231c40ffbc989f3667806e` |
| 2017-09-13 | test | 74503 | `6a6e41cb6040e865592927a6a3d987ba07ecfbdd49b334e5ae7a051a4a8811f5` | `fc19b8dbd40809dfab1de327b0aa4729c8455a808f4b573116e2a550b6704db3` |
| 2017-09-14 | test | 141812 | `bec85c877210205eabc874cd01e330177e056116c46b708e54310eff30bc27c3` | `bc834e005803df0686e7e72054a900d349ebab2f3f193102e2497e133456bd5a` |
| 2017-09-15 | test | 166316 | `e7aff5393af07e17df8934e81a4f4c7ba16568805800440b82dcfb35b6f74038` | `ec228999d3224add6ff58b1df76d34270cce7a919a6e833810a629d24805dcb2` |

## Interpretation and evidence boundary

The [official README](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md) documents the seven-column individual-trades format, publisher checksum files, and the possibility of later archive revisions. All selected dates use the historical millisecond convention; the documented spot archive transition to microseconds begins in 2025. The offline importer must still validate each row and its declared UTC date when root opens the relevant split.

The inspected public HTTP objects carry 2023 Last-Modified metadata. Neither that header nor a current checksum proves what a client could receive in 2017. No original-version history, receiver clock, correction ledger, independently adjudicated recording-error label or latent clean price is supplied by this acquisition.

Accordingly the authorized experiment must remain a **retrieved historical trade-price forecasting study**. It may report appropriately bounded out-of-sample results for that recorded target after the frozen evaluation. It cannot be presented as an original as-of backtest, validation of error-versus-genuine-shock identification, executable profit, or broad market generalization. This provenance stage itself reports no forecast or fitted-model result.

Any later coverage statistics or research results must retain Binance Vision attribution, the applicable CC BY-NC-SA 4.0 conditions, the frozen split, and the distinction between development access and protected final evaluation. A source failure, checksum change, cap breach or malformed input requires an explicit failure report, not silent date substitution or retrospective cleaning.
