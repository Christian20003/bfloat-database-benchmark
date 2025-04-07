from typing import List
import numpy as np

class Value:
    def __init__(self, row, column, value):
        self.row = row
        self.column = column
        self.value = value
    
    def to_sql_value(self):
        return f'({self.row},{self.column},{self.value})'
    
    def __str__(self):
        return f"Value(row: {self.row}, column: {self.column}, value: {self.value})"
    
    def __repr__(self):
        return f"Value(row: {self.row}, column: {self.column}, value: {self.value})"
    
    @staticmethod
    def values_to_sql(values: List, table_name: str) -> str:
        '''
        This function transforms a list of value objects into a string containing 
        an SQL-INSERT statement with all entries.

        :param values: The list of values which should be considered in the SQL statement.
        :param table_name: The name of the table in which they should be inserted.

        :return: The SQL-INSERT statement with all provided entries.
        '''
        result = f'INSERT INTO {table_name}(rowIndex, columnIndex, val) VALUES '
        for idx, value in enumerate(values):
            result += value.to_sql_value()
            if idx != len(values) - 1:
                result += ","
        result += ";"
        return result
    
    @staticmethod
    def values_to_numpy(values: List, rows: int) -> np.ndarray:
        '''
        This function changes the given list of value objects to a numpy array.

        :param values: The list of values which should be converted.
        :param rows: The number of rows of the resulting array.

        :return: The tensor as numpy array.
        '''
        list = []
        for row in range(rows):
            entries = [element for element in values if element.row == row]
            entries = sorted(entries, key=lambda x: x.column)
            entries = [element.value for element in entries]
            # Could be a vector
            if len(entries) == 1:
                list.append(entries[0])
            else:
                list.append(entries)
        return np.array(list, dtype=float)