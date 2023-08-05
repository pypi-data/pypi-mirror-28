==========
LP Monitor
==========


.. image:: https://img.shields.io/pypi/v/lp_monitor.svg
        :target: https://pypi.python.org/pypi/lp_monitor

.. image:: https://img.shields.io/travis/askz/lp_monitor.svg
        :target: https://travis-ci.org/askz/lp_monitor

.. image:: https://readthedocs.org/projects/lp-monitor/badge/?version=latest
        :target: https://lp-monitor.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/askz/lp_monitor/shield.svg
     :target: https://pyup.io/repos/github/askz/lp_monitor/
     :alt: Updates


A Liquidity Provider Node monitoring facility

lp_monitor is an abstract cli client designed for monitoring probes.
Actually it support only two methods:
* getbalance
* is_sync
and three currencies:
* BTC
* KMD
* MNZ

```console
Usage: lp_monitor [OPTIONS] METHOD

  Liquidity Provider Monitoring CLI

Options:
  -c, --coin TEXT       Coin selection: BTC|KMD|MNZ
  -H, --home DIRECTORY  Sets home directory which contains <coins>.conf files
  -h, --help            Show this message and exit.

```

Example:
```console
$ lp_monitor -H $HOME -c mnz is_sync
0
$ lp_monitor -lp_monitor -H $HOME -c mnz getbalance
2233.10000000
```

* Free software: GNU General Public License v3


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.1.0 (2018-01-03)
------------------

* First release on PyPI.


