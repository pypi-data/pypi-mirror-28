[![Build Status](https://travis-ci.org/TimSC/python-oauth10a.svg?branch=master)](https://travis-ci.org/TimSC/python-oauth10a) ![Licence MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)

# Overview
python-oauth10a is a python OAuth 1.0a library fully compatible with python versions: 2.7 and 3.4+.

# Installing

From pypi:

    $ pip install oauth10a

From source:

    $ python setup.py install
    
We recommend using [virtualenv](https://virtualenv.pypa.io/en/latest/).

# Examples

TODO

# Running tests
You can run tests using the following at the command line:

    $ pip install -r requirements.txt
    $ python setup.py test

# History

This code was originally forked from [Leah Culver and Andy Smith's oauth.py code](http://github.com/leah/python-oauth/). Some of the tests come from a [fork by Vic Fryzel](http://github.com/shellsage/python-oauth), while a revamped Request class and more tests were merged in from [Mark Paschal's fork](http://github.com/markpasc/python-oauth). Forked again from [joestump's python-oauth2](https://github.com/joestump/python-oauth2) which seems to be unmaintained. A number of notable differences exist between this code and its forefathers:

* Nearly 100% unit test coverage.
* The <code>DataStore</code> object has been completely ripped out. While creating unit tests for the library I found several substantial bugs with the implementation and confirmed with Andy Smith that it was never fully baked.
* Classes are no longer prefixed with <code>OAuth</code>.
* The <code>Request</code> class now extends from <code>dict</code>.
* The library is likely no longer compatible with Python 2.3.
* The <code>Client</code> class works and extends from <code>httplib2</code>. It's a thin wrapper that handles automatically signing any normal HTTP request you might wish to make.

