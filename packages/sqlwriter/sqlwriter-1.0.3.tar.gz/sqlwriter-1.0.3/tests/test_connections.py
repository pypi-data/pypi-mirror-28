import subprocess as sp
import unittest

import MySQLdb
import psycopg2
from utils import get_config

p = sp.Popen('docker ps', shell=True, stdout=sp.PIPE)
p.wait()
msg, _ = p.communicate()

SKIP_MYSQL = True
SKIP_POSTGRES = True

if 'sqlwriter_postgres_1' in msg:
    SKIP_POSTGRES = False
if 'sqlwriter_mysql_1' in msg:
    SKIP_MYSQL = False


class TestDBConnections(unittest.TestCase):
    def setUp(self):
        self.cfg = get_config('db_creds')
        self.mysql_creds = self.cfg['mysql']
        self.postgres_creds = self.cfg['postgres']

    @unittest.skipIf(SKIP_MYSQL, 'Could not find running MySQL docker container')
    def test_mysql_can_connect(self):
        try:
            conn = MySQLdb.connect(**self.mysql_creds)
            self.assertTrue(True)
            conn.close()
        except Exception as e:
            print(e)
            self.assertTrue(False)

    @unittest.skipIf(SKIP_POSTGRES, 'Could not find running Postgres docker container')
    def test_postgres_can_connect(self):
        try:
            conn = psycopg2.connect(**self.postgres_creds)
            self.assertTrue(True)
            conn.close()
        except Exception as e:
            print(e)
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
