Release History
===============

1.2.0
-----

* **API CHANGE** the serial object passed into command functions is optional.
* **API CHANGE** call signature changes on command functions.

1.1.2
-----

* Allow external modules to use built-in device detection and connection.

1.1.1
-----

* Unlink command logic from device detection and serial connection.

1.1.0
-----

* Fix broken 'put' and 'get' commands to work with arbitrary file sizes.
* Fix error when working with binary data.
* Update execute function to work with lists of multiple commands.
* Minor refactor to extract raw mode related code.
* Updated tests to keep coverage at 100% on both Python 2 and Python 3.

1.0.2
-----

* Remove spare print call.

1.0.1
-----

* Fix broken setup.

1.0.0
-----

* Full implementation of all the expected features.
* 100% test coverage.
* Comprehensive documentation.

0.0.1
-----

* Initial release. Basic functionality.
