sqlwriter
=========

Writes pandas DataFrame to several flavors of sql database

Flavors
-------

- Postres [building]
- Microsoft SQL [building]
- MySQL [future]
- Oracle [future]

Usage
=====
.. code-block:: pycon

 from sqlwriter import SQLWriter
 import psycopg2
 import pandas as pd

 conn = psycopg2.connect(**db_creds)
 df = pd.DataFrame(data=range(10), columns=['numbers'])

 writer = SQLWriter(conn=conn,
                    database='mydb',
                    table_name='table_name',
                    cols=df.columns,
                    truncate=True)
 writer.write(df.values)
 writer.close()

or

.. code-block:: pycon

 from sqlwriter import SQLDataFrame
 import psycopg2

 conn = psycopg2.connect(**db_creds)

 df = SQLDataFrame(data=range(10), columns=['numbers'])
 df.to_sql(conn=conn,
           database='mydb',
           table_name='table_name',
           cols=df.columns,
           truncate=True)
