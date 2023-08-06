
Changelog
=========

1.0.0 (2017-12-27)
------------------

* Initial stable release.

1.1.0 (2017-12-28)
------------------

* Added support for interval checks, e.g. `x in [0, 10)`.
* Simplified code generation for set membership checks.
* Improved documentation.

1.1.1 (2018-01-02)
------------------

* Added stricter validation checks when loading compiled program.
* Addressed warnings generated when compiling with strict compiler settings.
* Added support for Python 3.3 and 3.4.

1.2.0 (2018-01-23)
------------------

* Bug fixes for overflow/underflow conditions.
* Limit decimals according to IEEE 754 `decimal128` format.
* Major optimizations for computations involving integer values.
* Support for C coverage reports using gcov.
* Improved trace output for debugging.
