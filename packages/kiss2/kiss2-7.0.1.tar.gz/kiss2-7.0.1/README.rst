kiss2 - Python KISS Module
*************************

kiss2 is a Python Module that implementations the `KISS Protocol <https://en.wikipedia.org/wiki/KISS_(TNC)>`_ for
communicating with KISS-enabled devices (such as Serial or TCP TNCs). It is based on kiss(Another python module) which is no longer maintained.

Versions
========

- 6.5.x branch will be the last version of this Module that supports Python 2.7.x
- 7.x.x branch and-on will be Python 3.x ONLY.

Installation
============
Install from pypi using pip: ``pip install kiss2``


Usage Examples
==============
Read & print frames from a TNC connected to '/dev/ttyUSB0' at 1200 baud::

    import kiss

    def p(x): print(x)  # prints whatever is passed in.

    k = kiss.SerialKISS('/dev/ttyUSB0', 1200)
    k.start()  # inits the TNC, optionally passes KISS config flags.
    k.read(callback=p)  # reads frames and passes them to `p`.


See also: examples/ directory.


Testing
=======
Run nosetests from a Makefile target::

    make test


Similar Projects
================

* `apex <https://github.com/Syncleus/apex>`_ by Jeffrey Phillips Freeman (WI2ARD). Next-Gen APRS Protocol. (based on this Module! :)
* `aprslib <https://github.com/rossengeorgiev/aprs-python>`_ by Rossen Georgiev. A Python APRS Library with build-in parsers for several Frame types.
* `aprx <http://thelifeofkenneth.com/aprx/>`_ by Matti & Kenneth. A C-based Digi/IGate Software for POSIX platforms.
* `dixprs <https://sites.google.com/site/dixprs/>`_ by HA5DI. A Python APRS project with KISS, digipeater, et al., support.
* `APRSDroid <http://aprsdroid.org/>`_ by GE0RG. A Java/Scala Android APRS App.
* `YAAC <http://www.ka2ddo.org/ka2ddo/YAAC.html>`_ by KA2DDO. A Java APRS Client.
* `Ham-APRS-FAP <http://search.cpan.org/dist/Ham-APRS-FAP/>`_ by aprs.fi: A Perl APRS Parser.
* `Dire Wolf <https://github.com/wb2osz/direwolf>`_ by WB2OSZ. A C-Based Soft-TNC for interfacing with sound cards. Can present as a KISS interface!

Source
======
Github: https://git.scd31.com/laptopdude90/kiss2

Author
======
Greg Albrecht W2GMD oss@undef.net (kiss)
Stephen Downward VA1QLE stephen@stephendownward.ca (kiss2)

https://blog.scd31.com

Copyright
=========
Copyright 2017 Greg Albrecht(kiss), Stephen Downward(kiss2) and Contributors

License
=======
Apache License, Version 2.0. See LICENSE for details.
