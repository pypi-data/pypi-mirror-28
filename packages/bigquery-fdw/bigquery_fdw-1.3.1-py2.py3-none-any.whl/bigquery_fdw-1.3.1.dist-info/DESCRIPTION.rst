bigquery_fdw: BigQuery Foreign Data Wrapper for PostgreSQL
==========================================================

bigquery_fdw is a BigQuery foreign data wrapper for PostgreSQL using
`Multicorn <https://github.com/Kozea/Multicorn>`__.

It allows to write queries in PostgreSQL SQL syntax using a foreign
table. It supports most of BigQuery’s `data
types <docs/data_types.md>`__ and `operators <docs/operators.md>`__.

Features and limitations
------------------------

-  Table partitioning is supported. `You can use partitions in your SQL
   queries <docs/table_partitioning.md>`__.
-  Queries are parameterized when sent to BigQuery
-  BigQuery’s standard SQL support (legacy SQL is not supported)
-  Authentication works with a “`Service
   Account <docs/service_account.md>`__” Json private key

`Read more <docs/README.md>`__.

Requirements
------------

-  PostgreSQL >= 9.5
-  Python 3

Dependencies
------------

Dependencies required to install bigquery_fdw:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``postgresql-server-dev-X.Y``
-  ``python3-pip``
-  ``python3-dev``
-  ``make``
-  ``gcc``

Major dependencies installed automatically during the installation process:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Google Cloud
   BigQuery <https://pypi.org/project/google-cloud-bigquery/>`__
-  `Multicorn <https://github.com/Kozea/Multicorn>`__

Installation
------------

.. code:: bash

    # Install `setuptools` if necessary
    pip3 install --upgrade setuptools

    # Install Multicorn
    git clone git://github.com/Kozea/Multicorn.git && cd Multicorn
    export PYTHON_OVERRIDE=python3
    make && make install

    # Install bigquery_fdw
    pip3 install bigquery-fdw

Usage
-----

We recommend testing the `BigQuery client
connectivity <docs/test_client.md>`__ before trying to use the FDW.

With ``psql``:

.. code:: sql

    CREATE EXTENSION multicorn;

    CREATE SERVER bigquery_srv FOREIGN DATA WRAPPER multicorn
    OPTIONS (
        wrapper 'bigquery_fdw.fdw.ConstantForeignDataWrapper'
    );

    CREATE FOREIGN TABLE my_bigquery_table (
        column1 text,
        column2 bigint
    ) SERVER bigquery_srv
    OPTIONS (
        fdw_dataset  'my_dataset',
        fdw_table 'my_table',
        fdw_key '/opt/bigquery_fdw/user.json'
    );

Options
-------

List of options implemented in ``CREATE FOREIGN TABLE`` syntax:

+-----+----+----+
| Opt | De | De |
| ion | fa | sc |
|     | ul | ri |
|     | t  | pt |
|     |    | io |
|     |    | n  |
+=====+====+====+
| ``f | -  | Bi |
| dw_ |    | gQ |
| dat |    | ue |
| ase |    | ry |
| t`` |    | da |
|     |    | ta |
|     |    | se |
|     |    | t  |
|     |    | na |
|     |    | me |
+-----+----+----+
| ``f | -  | Bi |
| dw_ |    | gQ |
| tab |    | ue |
| le` |    | ry |
| `   |    | ta |
|     |    | bl |
|     |    | e  |
|     |    | na |
|     |    | me |
+-----+----+----+
| ``f | -  | Pa |
| dw_ |    | th |
| key |    | to |
| ``  |    | pr |
|     |    | iv |
|     |    | at |
|     |    | e  |
|     |    | Js |
|     |    | on |
|     |    | ke |
|     |    | y  |
|     |    | (S |
|     |    | ee |
|     |    | `K |
|     |    | ey |
|     |    | st |
|     |    | or |
|     |    | ag |
|     |    | e  |
|     |    | re |
|     |    | co |
|     |    | mm |
|     |    | en |
|     |    | da |
|     |    | ti |
|     |    | on |
|     |    | s  |
|     |    | <d |
|     |    | oc |
|     |    | s/ |
|     |    | ke |
|     |    | y_ |
|     |    | st |
|     |    | or |
|     |    | ag |
|     |    | e. |
|     |    | md |
|     |    | >` |
|     |    | __ |
|     |    | )  |
+-----+----+----+
| ``f | -  | Co |
| dw_ |    | nv |
| con |    | er |
| ver |    | t  |
| t_t |    | Bi |
| z`` |    | gQ |
|     |    | ue |
|     |    | ry |
|     |    | ti |
|     |    | me |
|     |    | zo |
|     |    | ne |
|     |    | fo |
|     |    | r  |
|     |    | da |
|     |    | te |
|     |    | s  |
|     |    | an |
|     |    | d  |
|     |    | ti |
|     |    | me |
|     |    | st |
|     |    | am |
|     |    | ps |
|     |    | to |
|     |    | se |
|     |    | le |
|     |    | ct |
|     |    | ed |
|     |    | ti |
|     |    | me |
|     |    | zo |
|     |    | ne |
|     |    | .  |
|     |    | Ex |
|     |    | am |
|     |    | pl |
|     |    | e: |
|     |    | `` |
|     |    | 'U |
|     |    | S/ |
|     |    | Ea |
|     |    | st |
|     |    | er |
|     |    | n' |
|     |    | `` |
|     |    | .  |
+-----+----+----+
| ``f | `` | Se |
| dw_ | 'f | e  |
| gro | al | `R |
| up` | se | em |
| `   | '` | ot |
|     | `  | e  |
|     |    | gr |
|     |    | ou |
|     |    | pi |
|     |    | ng |
|     |    | an |
|     |    | d  |
|     |    | co |
|     |    | un |
|     |    | ti |
|     |    | ng |
|     |    |  < |
|     |    | do |
|     |    | cs |
|     |    | /r |
|     |    | em |
|     |    | ot |
|     |    | e_ |
|     |    | gr |
|     |    | ou |
|     |    | pi |
|     |    | ng |
|     |    | .m |
|     |    | d> |
|     |    | `_ |
|     |    | _. |
+-----+----+----+
| ``f | -  | Se |
| dw_ |    | e  |
| cas |    | `C |
| tin |    | as |
| g`` |    | ti |
|     |    | ng |
|     |    |  < |
|     |    | do |
|     |    | cs |
|     |    | /c |
|     |    | as |
|     |    | ti |
|     |    | ng |
|     |    | .m |
|     |    | d> |
|     |    | `_ |
|     |    | _. |
+-----+----+----+
| ``f | `` | Se |
| dw_ | 'f | t  |
| ver | al | to |
| bos | se | `` |
| e`` | '` | 't |
|     | `  | ru |
|     |    | e' |
|     |    | `` |
|     |    | to |
|     |    | ou |
|     |    | tp |
|     |    | ut |
|     |    | de |
|     |    | bu |
|     |    | g  |
|     |    | in |
|     |    | fo |
|     |    | rm |
|     |    | at |
|     |    | io |
|     |    | n  |
|     |    | in |
|     |    | Po |
|     |    | st |
|     |    | rg |
|     |    | eS |
|     |    | QL |
|     |    | ’s |
|     |    | lo |
|     |    | gs |
+-----+----+----+
| ``f | `` | Bi |
| dw_ | 's | gQ |
| sql | ta | ue |
| _di | nd | ry |
| ale | ar | SQ |
| ct` | d' | L  |
| `   | `` | di |
|     |    | al |
|     |    | ec |
|     |    | t. |
|     |    | Cu |
|     |    | rr |
|     |    | en |
|     |    | tl |
|     |    | y  |
|     |    | on |
|     |    | ly |
|     |    | `` |
|     |    | st |
|     |    | an |
|     |    | da |
|     |    | rd |
|     |    | `` |
|     |    | is |
|     |    | su |
|     |    | pp |
|     |    | or |
|     |    | te |
|     |    | d. |
+-----+----+----+

More documentation
------------------

See `bigquery_fdw documentation <docs/README.md>`__.


