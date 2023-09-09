"----------------------------------------------test_measurement_analysis----------------------------------------------"
"""
    Moduł zawierający klasę testującą TestMeasurementAnalysis napisaną w celu przeprowadzennia testów klasy 
MeasurementAnalysis, znajdującej się w module measurement_analysis.
    W ramch testów sprawdzana jest poprawność wytwarzanej ramki danych, czy są generowane wykresy i czy zwracane są         
poprawne wyniki analizy danych.


"""

import unittest
import sqlite3
import pandas as pd
from measurement_analysis import MeasurementAnalysis

class TestMeasurementAnalysis(unittest.TestCase):
    """
        Klasa wykonuje testy jednostkowe dla klasy MeasurementAnalysis.
    """
    def setUp(self):
        """
            Metoda odpowiada za przygotowanie testowej bazy danych z danymi pomiarowymi.
        """

        self.conn = sqlite3.connect('test_database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE measurements (date TEXT, value REAL)')
        self.cursor.execute('INSERT INTO measurements VALUES ("2023-01-01 00:00:00", 10.5)')
        self.cursor.execute('INSERT INTO measurements VALUES ("2023-01-02 00:00:00", 11.2)')
        self.cursor.execute('INSERT INTO measurements VALUES ("2023-01-03 00:00:00", 9.8)')
        self.cursor.execute('INSERT INTO measurements VALUES ("2023-01-04 00:00:00", 12.1)')
        self.cursor.execute('INSERT INTO measurements VALUES ("2023-01-05 00:00:00", 11.7)')
        self.conn.commit()

    def tearDown(self):
        """
            Metoda odpowiada za usunięcie testowej bazy danych.
        """

        self.cursor.execute('DROP TABLE measurements')
        self.conn.close()

    def test_get_data(self):
        """
            Metoda sprawdza czy zwracana jest poprawna ramkę danych.
        """

        analysis = MeasurementAnalysis('test_database.db')
        expected_data = pd.DataFrame([
            ["2023-01-01 00:00:00", 10.5],
            ["2023-01-02 00:00:00", 11.2],
            ["2023-01-03 00:00:00", 9.8],
            ["2023-01-04 00:00:00", 12.1],
            ["2023-01-05 00:00:00", 11.7]], columns=["date", "value"])
        expected_data["date"] = pd.to_datetime(expected_data["date"]) #Konwersja

        actual_data = analysis.get_data()
        actual_data.columns = ["date", "value"]
        actual_data["date"] = pd.to_datetime(actual_data["date"]) #Konwersja

        pd.testing.assert_frame_equal(actual_data, expected_data, check_dtype=False)

    def test_chart(self):
        """
            Metoda sprawdza czy wykres jest generowany.
        """

        analysis = MeasurementAnalysis('test_database.db')

        try:
            analysis.chart()
        except Exception as e:
            self.fail(f"Wystąpił błąd genrowania wykresu: {str(e)}")

    def test_analyze(self):
        """
            Metoda sprawdza czy zwracane są poprawne wyniki analizy.
        """

        analysis = MeasurementAnalysis('test_database.db')
        expected_results = {
            'max_value': 12.1,
            'min_value': 9.8,
            'min_date': '2023-01-03 00:00:00',
            'max_date': '2023-01-04 00:00:00',
            'data_mean': 11.06
        }
        actual_results = analysis.analyze()

        self.assertEqual(actual_results['max_value'], expected_results['max_value'])
        self.assertEqual(actual_results['min_value'], expected_results['min_value'])
        self.assertEqual(round(actual_results['data_mean'], 2), expected_results['data_mean'])
        self.assertEqual(actual_results['min_date'].strftime('%Y-%m-%d %H:%M:%S'), expected_results['min_date'])
        self.assertEqual(actual_results['max_date'].strftime('%Y-%m-%d %H:%M:%S'), expected_results['max_date'])

if __name__ == '__main__':
    unittest.main()
