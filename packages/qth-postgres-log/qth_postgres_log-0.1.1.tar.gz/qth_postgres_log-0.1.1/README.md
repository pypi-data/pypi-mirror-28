Qth Postgres Log
================

A logging service for [Qth](https://github.com/mossblaser/qth) which stores Qth
events and properties into a PostgreSQL database.


Usage
-----

Just run:

    $ qth_postgres_log

Which will create and start populating tables `qth_log` and `qth_paths` in the
default database. See `--help` for more.
