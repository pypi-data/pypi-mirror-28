
muacrypt: Autocrypt and more for mail user agents
=================================================

**this tool is under heavy development, use at your own risk**

``muacrypt`` implements the `Autocrypt Level 1 specification
<https://autocrypt.org/autocrypt-spec-1.0.0.pdf>`_
and offers a way to robustly manage identities through
which Autocrypt headers can be added or parsed with
outgoing or incoming messages.  Each identitiy relates
to an e-mail account and has an Autocrypt key.

This README is intended to help contributors to get setup with running
tests and using the command line. The online docs at
https://muacrypt.readthedocs.io contain
more documentation about overall goals of the project.

testing
+++++++

To use the code and run tests you need to have installed:

- the command line client "gpg", optionally "gpg2",
  available through "gnupg" and "gnugp2" on debian.

- something to speed up gpg key creation, e.g.
  by installing "rng-tools" on debian.

- python2.7 and python3.5 including headers
  ("python2.7-dev" and "python3.5-dev" on debian).

- tox either installed via ``pip install tox``
  or ``apt install python-tox``.

In one command on Debian::

    apt install gnupg2 rng-tools python2.7-dev python3.5-dev python-tox

Afterwards you can run all tests:

    $ tox

this runs all automated tests.


installation
++++++++++++

You'll need the command line client "gpg", optionally "gpg2",
available through "gnupg" and "gnugp2" on debian.

To install the muacrypt command line tool you can install
the "muacrypt" python package into your virtual environment
of choice.  If you don't know about python's virtual environments
you may just install the debian package "python-pip" and then
use "pip" to install the muacrypt library and command line too::

    $ sudo pip install muacrypt

This will install the required dependency "click", a python
framework for writing command line clients.


installation for development
++++++++++++++++++++++++++++

If you plan to work/modify the sources and have
a github checkout we strongly recommend to create
and activate a python virtualenv and then once use
**pip without sudo in edit mode**::

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -e .

Changes you subsequently make to the sources will be
available without further installing the muacrypt
package again.


running the command line
++++++++++++++++++++++++

After installation simply run the main command::

    muacrypt

to see available sub commands and options.  Start by
initializing an Autocrypt account which will maintain
its own keyring and not interfere with your possibly
existing gpg default keyring::

    $ muacrypt init

Afterwards you can create an Autocrypt header
for an email address::

    $ muacrypt make-header x@example.org

You can process and integrate peer's Autocrypt
keys by piping an email message into the ``process-incoming`` subcommand::

    $ muacrypt process-incoming <EMAIL_MESSAGE_FILE

At any point you can show the status of your muacrypt
account::

    $ muacrypt status
