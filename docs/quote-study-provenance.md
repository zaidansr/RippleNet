# Frozen multi-session quote-study acquisition provenance

This records acquisition under [public plan 6993f9a12311d759b8e5d3370fcac8dc2ade6ed7](https://github.com/zaidansr/RippleNet/commit/6993f9a12311d759b8e5d3370fcac8dc2ade6ed7) and [the frozen design](quote-study-plan.md). The plan preceded every new dataset request. The 12 exact Kraken spot XBT/USD first-of-month sessions run from June 2025 through May 2026. June–November 2025 are training, December 2025–February 2026 validation, and March–May 2026 protected test. The previously inspected June 2026 session is excluded. No replacement date, alternative instrument, provider, account, paid resource or cap expansion was used.

**Acquisition passed its byte-integrity gate: all 24 fixed files returned HTTP 200 and passed the declared size bounds, advertised whole-file MD5 comparison, full gzip EOF/CRC validation and SHA256 hashing.** Aggregate compressed size is **124,330,346 bytes**; streamed expanded size is **794,023,732 bytes**. No CSV record, price, ID, target or feature was decoded in this acquisition stage, including the protected test files. Row counts, exact schemas, clock validity, origin eligibility and target coverage remain for the separately frozen loader and must not be inferred from successful decompression.

## Source and publication conditions

Tardis.dev supplied the normalized Kraken data. This document publishes acquisition metadata only. Raw/event-level records, price series, vendor terms copies, fitted parameters, scalers, selections and predictions remain private outside the public repository. It grants no license to vendor data or trained models and does not apply the Binance CC license. Original project code is separate from the provider's data rights. [Current terms, particularly 9.3 and 9.5](https://docs.tardis.dev/legal/terms-of-service)

Immediately before the first dataset GET, the source terms were retrieved once from `https://docs.tardis.dev/legal/terms-of-service.md`. Their SHA256 exactly matched the previously reviewed snapshot: `ea5901192dce12c72f2303702b7f2bf87826b4b1a44806f8659d0fd91b030b11`. The recheck returned HTTP 200 at 2026-11-07T17:07:12.283720+00:00. The terms permit qualifying non-reconstructive aggregate research outputs while restricting dataset substitutes and external model-bearing publication. This remains a source-specific restriction rather than an open-data grant. [Provider terms](https://docs.tardis.dev/legal/terms-of-service)

The provider documents no-key downloads for each month's first day. The two data types were `trades` and `quotes`; all initial requests used the exact pattern `https://datasets.tardis.dev/v1/kraken/{kind}/{YYYY}/{MM}/01/XBT-USD.csv.gz` for the dates below. No authorization header, API key, account, subscription or trial was used. The source documents GET access and deliberately returns 404 to HEAD, so no HEAD inference was used. [Official dataset API](https://docs.tardis.dev/downloadable-csv-files/api)

The fixed namespace is appropriate because all sessions precede the documented July 10, 2026 WS1-to-WS2 and XBT-to-BTC transition. Source metadata places the exchange-server relocation from Dublin to London at November 1, 2025 15:00 UTC, inside the final training session. This is a potential collector-age infrastructure change, not an estimate of end-user latency. [Official Kraken collection details](https://docs.tardis.dev/historical-data-details/kraken), [retrieved exchange summary](https://api.tardis.dev/v1/exchanges/kraken/summary)

## Chronology, integrity and fixed bounds

Acquisition started at 2026-11-07T17:07:11.377129+00:00 and completed at 2026-11-07T17:07:59.036047+00:00. Each file's HTTP length matched its downloaded length, advertised MD5 matched locally computed MD5, and all gzip trailers were read successfully. Compressed and expanded SHA256 values below pin the exact retrieved bytes, not original as-of availability, complete capture, economic truth or immutable future vendor versions.

Per-day limits remained 32 MiB compressed / 256 MiB expanded for trades and 128 MiB compressed / 1 GiB expanded for quotes. Across 12 days the limits were 1,920 MiB compressed and 15 GiB expanded. The frozen two-million/five-million data-row limits are deferred to the record-decoding loader, not claimed checked here. Binary expansion was hashed in bounded chunks and discarded; only compressed data were retained. No CSV text or uncompressed file was persisted. HTTP error, unexpected response, missing verifiable MD5, checksum failure or bound exceedance would stop acquisition without retrying another date or increasing limits.

Private artifacts use `work/quote-study/data/kraken_{kind}_YYYY-MM-DD_XBT-USD.csv.gz`. The private downloader and full manifest are in `work/quote-study/`; the manifest contains initial source URLs, HTTP metadata, sizes, MD5, compressed SHA256, expanded CSV SHA256, UTC request/completion times, split and integrity statuses. Potential redirect URLs are private and are not published. All 24 files have `csv_decoded=false` and `rows_parsed=false`.

Private acquisition script SHA256: `4cc9505252861ea08ea263c14e45b6b19b0fd3abb3179313bb32426683660e79`. Private completed manifest SHA256: `a9e4b81c899ebd359c6aaa07e67c0d5cef53e29c36580ebd4cb906951f398ab0`. These identify this acquisition artifact; later loader/model artifacts require their own provenance.

## Per-file byte counts and compressed hashes

`T` means trades and `Q` quotes. Filenames follow the exact pattern above. Every row has HTTP 200, verified advertised MD5 and successful gzip CRC. Byte counts include CSV headers in the expanded stream.

| UTC date | Split | Kind | Compressed bytes | Expanded bytes | Compressed SHA256 |
| --- | --- | --- | ---: | ---: | --- |
| 2025-06-01 | train | T | 217,381 | 1,341,148 | `81b107c11df163294b6e971f5363d835708cbc41eced545096d1743b8792bfb5` |
| 2025-06-01 | train | Q | 6,448,577 | 41,734,728 | `00d548cabe127b71ea31f11f44426287064137d1ea07d628b4281673b3c785e2` |
| 2025-07-01 | train | T | 379,907 | 2,378,457 | `4d421462f60370d0ed75eb569f35a5553f4fd8fb0d8ef17cbdb4ed6ca188893a` |
| 2025-07-01 | train | Q | 7,127,794 | 45,432,678 | `e3ca3eaa706d9402d33ae30bcc040b284ac019da573e074b7527cc6d2a15ed99` |
| 2025-08-01 | train | T | 782,590 | 4,927,850 | `055ceb17fb9bbda237b02e2fda0f1568896714c32d8414c73fe1ceb4e9702ee3` |
| 2025-08-01 | train | Q | 10,311,849 | 64,676,208 | `1b381def80748d054c249d051e53995428fbc9788fb1c07ded5e2d9d7e11ebc7` |
| 2025-09-01 | train | T | 422,623 | 2,701,965 | `cfd2ef4614d4c18c691fc378cb7f4103d5875d08de52e61dd0258b54a9205af7` |
| 2025-09-01 | train | Q | 10,337,658 | 64,908,533 | `ea0f5c523bdb114d90502dbd913791c188e101a1047ad19c906d3fdf5a21551d` |
| 2025-10-01 | train | T | 480,582 | 3,075,266 | `4c7d2a3206781e82c30c14a7322702395181983ff600992c5b8321888177ca4e` |
| 2025-10-01 | train | Q | 9,514,508 | 62,130,285 | `711e1c9a491c07b19a8b927c2bb752461fbd8d38b5fbb6db2b2e992bdd868c5c` |
| 2025-11-01 | train | T | 211,627 | 1,229,347 | `dc6af89bb6041130d8c01c6faaac7b6eeb3bc4841422f425e1c73e6cbeaa93d7` |
| 2025-11-01 | train | Q | 3,335,583 | 21,645,824 | `0fcec181173ecea3b1b441f3e4f16a2020743c2101bebe140a2bc1e603eae550` |
| 2025-12-01 | validation | T | 796,756 | 5,220,372 | `2584404417ede1b268b90484468b1330395490a7ba3864baeb03ef5ba8247064` |
| 2025-12-01 | validation | Q | 13,915,717 | 87,119,949 | `bed473b72884d52a9d293ad6c460c4f76f01d5376da03c2da889ed181c8e3ddc` |
| 2026-01-01 | validation | T | 343,791 | 2,200,849 | `0132e2687a925b6614277c690d54cd8ae5f1dc1ca412b7710b8e1bc6abfb89ba` |
| 2026-01-01 | validation | Q | 3,823,551 | 24,168,369 | `cb3d9fe4c0e4573a977b736f68eeeedf2302f5cc9f2fb116aeae8c84a87ab9d6` |
| 2026-02-01 | validation | T | 873,477 | 4,959,647 | `4a350fd1850c65396858449df2ef3be017dc98606dfd014266b163f7af336f8b` |
| 2026-02-01 | validation | Q | 20,500,703 | 133,537,076 | `20fa5e22ee27b47e58c141f0ea3123e76e48d59246aa9fdf00247f6d399d40d3` |
| 2026-03-01 | test | T | 711,714 | 5,249,056 | `b47c5a4d2f06e396ed6050470834e9bd6b9de32926aca69a6a501cc8e53a993a` |
| 2026-03-01 | test | Q | 14,500,247 | 94,090,979 | `35135e30290edafa225284278c7f268acef6f2ab8c848ef4e4d54785d966e048` |
| 2026-04-01 | test | T | 626,132 | 4,260,045 | `8ec0cd49956d2e39079e0040ff9f340ddaf6c6478903ff747e3cecfa7e2d33e9` |
| 2026-04-01 | test | Q | 11,598,758 | 72,722,003 | `3275cafe7437e0b33ad85a8b5c567b905c3e361fb2a5192f00c0980321d992b8` |
| 2026-05-01 | test | T | 591,259 | 3,729,891 | `c60408d8d5037f111fef80e5a8d5a0dfe646731101a4077449fdf07c4f7a2045` |
| 2026-05-01 | test | Q | 6,477,562 | 40,583,207 | `7983dd9cd98e70c188a1c0d239aa158b553142d3930f58b893334b7042cca916` |

## Expanded-byte hashes

These hashes were computed from binary decompression only; their presence is not a record/schema inspection or a protected-price disclosure.

| UTC date | Kind | Expanded CSV SHA256 |
| --- | --- | --- |
| 2025-06-01 | T | `476a7a94076801ab493c88b577e923dd07a44455dffc0ff81d254e9bb8e46237` |
| 2025-06-01 | Q | `121afd7ea4008bf905dd5f89f589ebfa6a8801d75715724260466f234f0678f4` |
| 2025-07-01 | T | `2a884f3a136d4f7082f25595e503065e0aa9ed1da4ab682898543cf38f0c520e` |
| 2025-07-01 | Q | `88b33799b4d6f85d08d7490d823c653c1f647269c2d8dea9e76cbe42a901bf46` |
| 2025-08-01 | T | `401694c7410126f3ed6d411fc5778316accd70b41bd5071435444787ca36f9e6` |
| 2025-08-01 | Q | `eb272a4a8595cb8d7dba1cf48e0abfd98766557e1d78291c29d8b8c633997392` |
| 2025-09-01 | T | `8bd4fe662007ba870e19a4e2d0ca5d06b6b79210eeb8ffdd997cd496fbd973d8` |
| 2025-09-01 | Q | `c43a6dbe292257e8aafc5c247a812bb89e0a77493223abe67363042010ccd8c6` |
| 2025-10-01 | T | `0a8b9b12587547589186d3c1dd0ab931531c7bd8ed9d84881715f9d494d0d323` |
| 2025-10-01 | Q | `164fbd7b152ea927ff3bb0d6bcd71d4488ee9452208fd204741cbcedb017751e` |
| 2025-11-01 | T | `8c74e05c4177cddf58dfe40b03558f989cb84e8c9237a05998145489a51d7b93` |
| 2025-11-01 | Q | `2af44d0fcf767ce55f677bb70c91aaa01a7121a2f1ad473a8cc774a58fda9a15` |
| 2025-12-01 | T | `5a1b4c95c17eafef70c735e744582662668615876cb6d66233869f632039e0b6` |
| 2025-12-01 | Q | `7b0ebf0ea7be749ca6c14a6d95cadd871ce38d67b73bf13760844332023b230b` |
| 2026-01-01 | T | `6a0dc9f85cc70ec0b3fdad93d9c26f0e85cd7c62159ea90ba77446d76802006e` |
| 2026-01-01 | Q | `aeab51ea96b32a1c09c982c5bba65f296fb4dedb2f72fa80723d9e4f30ed8429` |
| 2026-02-01 | T | `8aa8c3030ec425991e5553c909cb7eb5f89f19b717fee7f9d0b3a50d6ecb87aa` |
| 2026-02-01 | Q | `97aa8b9133be804b1b4c4de262943311bc3ead0b8332fc71e8589c640553288f` |
| 2026-03-01 | T | `0b60192c3844d246235715c594649e3ca1fa5c65b5f0bad2ba1537b15a588b5e` |
| 2026-03-01 | Q | `ba2fc356cc27b145a149b93e63ceeca6ed5a38e316f19807dee05a68ebc7e83f` |
| 2026-04-01 | T | `9c9ecd596aab3724e56f53c6003d757b27503238e90dbccd77df3a04df8a8432` |
| 2026-04-01 | Q | `ba8e2030378d7d671ddcca43f752a66315b4d03e786d60231b647d91eeaf00b2` |
| 2026-05-01 | T | `120b44abd10d24f21aeef1026bff97f5031d8218dc14a7128d842fefdf847b81` |
| 2026-05-01 | Q | `81bc6e4d84943dbbe5704fd3469c28dde2fc23285e1d1ebc146dc63c675404c4` |

## Remaining evidence limits

Acquisition establishes accessible fixed files and internally consistent retrieved bytes. It does not establish valid records, independent error/shock labels, latent efficient prices, uninterrupted feeds, operational receipt times or forecast gains. The source CSVs omit disconnect markers, and quotes represent the provider's reconstruction; missing markers and cross-channel timing remain limitations of the recorded-market pilot. [Dataset export limitations](https://docs.tardis.dev/downloadable-csv-files/api), [CSV definitions](https://docs.tardis.dev/downloadable-csv-files/data-types)

Development inspection must wait for executable publication. Protected test record decoding must additionally wait for the private fitted-selection hash freeze. Three monthly test sessions support only the descriptive interpretation declared in the plan; this provenance document contains no fitted result.
