
CHANGELOG
=========

0.1.16 (2018-02-07)
-------------------

* Send first alert "immediately" if critical temp status.

* Send email alert when tempmon server marks a client as offline.


0.1.15 (2017-11-19)
-------------------

* Add problem report for disabled clients/probes.


0.1.14 (2017-08-08)
-------------------

* Fix alembic script AGAIN


0.1.13 (2017-08-08)
-------------------

* Don't kill tempmon client if DB session.commit() fails

* Grow the ``Reading.degrees_f`` column

* Fix tempmon alembic script per continuum needs


0.1.12 (2017-08-04)
-------------------

* Auto-delete child objects when deleting Client or Probe object


0.1.11 (2017-07-07)
-------------------

* Switch license to GPL v3 (no longer Affero)


0.1.10 (2017-07-06)
-------------------

* Add ``rattail purge-tempmon`` command

* Tweak import placement to fix startup


0.1.9 (2017-06-01)
------------------

* Fix bug when marking client as offline from server loop


0.1.8 (2017-06-01)
------------------

* Refactor main server loop a bit, to add basic retry w/ error logging

* Tweak mail templates a bit, to reference config values


0.1.7 (2017-06-01)
------------------

* Add ``rattail export-hotcooler`` command, for initial hotcooler support

* Add client error logging in case committing session fails..


0.1.6 (2017-02-09)
------------------

* Add configurable delay per client; improve client try/catch


0.1.5 (2016-12-12)
------------------

* Add config for "good temp" email


0.1.4 (2016-12-11)
------------------

* Hopefully fix alert logic when status becomes good


0.1.3 (2016-12-10)
------------------

* Add email config for tempmon-server alerts

* Add mail templates to project manifest


0.1.2 (2016-12-10)
------------------

* Add support for dummy probes (random temp data)

* Add mail templates, plus initial status alert delay for probes


0.1.1 (2016-12-05)
------------------

* Fix import bug in server daemon


0.1.0 (2016-12-05)
------------------

* Initial release.
