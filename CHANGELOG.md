# Changelog

## 0.1.8 (2022-10-13)
* Fix problems introduced by update to web3 v6

## 0.1.7 (2022-10-13)
* Update dependencies

## 0.1.6 (2022-10-13)
* Remove typing extensions dependency by @karlb in https://github.com/raiden-network/raiden-common/pull/24

## 0.1.5 (2022-10-06)
* Remove RTC dependencies by @konradkonrad in https://github.com/raiden-network/raiden-common/pull/16
* Fix tests/typing in python 3.10 by @konradkonrad in https://github.com/raiden-network/raiden-common/pull/22
* Add http_retry_with_backoff_middleware by @karlb in https://github.com/raiden-network/raiden-common/pull/23

## 0.1.4 (2022-09-22)
* Add support for nitro ETH client

## 0.1.3 (2022-07-28)
* Split off `raiden-common` package from `raiden` package to allow projects to depend on helpful code without pulling in the whole raiden client.
