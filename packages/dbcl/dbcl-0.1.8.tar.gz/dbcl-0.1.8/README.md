# dbcl

[![Build Status](https://travis-ci.org/ksofa2/dbcl.svg?branch=master)](https://travis-ci.org/ksofa2/dbcl)
[![Maintainability](https://api.codeclimate.com/v1/badges/e4663675580964433469/maintainability)](https://codeclimate.com/github/ksofa2/dbcl/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e4663675580964433469/test_coverage)](https://codeclimate.com/github/ksofa2/dbcl/test_coverage)

A database command line interface that is engine-agnostic.

## Install

```
pip install dbcl
```

You will also need to install the package needed for your database like `cx_Oracle`, `pg8000` or `PyMySQL`.

Once installed, you can connect to a database by specifying the database URL, [as used by SQLAlchemy](http://docs.sqlalchemy.org/en/latest/core/engines.html), for example:

```
dbcl sqlite:///test.db
```

or

```
dbcl postgresql+pg8000://username:password@127.0.0.1:5432/dbname
```
