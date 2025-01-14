import psycopg2
import unittest

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password="password",
            host="127.0.0.1",
            port="5432"
        )
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.conn.close()

    def test_table_exists(self):
        self.cursor.execute("SELECT to_regclass('public.logs');")
        result = self.cursor.fetchone()[0]
        self.assertIsNotNone(result, "Tabela logs não foi criada")

    def test_partition_exists(self):
        self.cursor.execute("SELECT to_regclass('public.logs_20250101');")
        result = self.cursor.fetchone()[0]
        self.assertIsNotNone(result, "Partição logs_20250101 não foi criada")
        
        self.cursor.execute("SELECT to_regclass('public.logs_20250108');")
        result = self.cursor.fetchone()[0]
        self.assertIsNotNone(result, "Partição logs_20250108 não foi criada")

    def test_index_exists(self):
        self.cursor.execute("SELECT to_regclass('public.idx_logs_log_time');")
        result = self.cursor.fetchone()[0]
        self.assertIsNotNone(result, "Índice BRIN idx_logs_log_time não foi criado")

if __name__ == '__main__':
    unittest.main()
