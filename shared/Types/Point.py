from typing import List
import numpy as np

class Point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def to_sql_value(self):
        return f"({self.id}, {self.x}, {self.y})"

    def __str__(self):
        return f"Point(id: {self.id}, x: {self.x}, y: {self.y})"
    
    def __repr__(self):
        return f"Point(id: {self.id}, x: {self.x}, y: {self.y})"
    
    @staticmethod
    def points_to_sql(points: List, table_name: str) -> str:
        '''
        This function transforms the list of point objects into a single sql insert statement.

        :param points: The list of points which should be converted.
        :param table_name: The name of the table in which they should be inserted.

        :return: A string which defines the insert statement for all points.
        '''

        result = f'INSERT INTO {table_name}(id, x, y) VALUES '
        for idx, point in enumerate(points):
            result += point.to_sql_value()
            if idx != points.__len__() - 1:
                result += ","
        result += ";"
        return result
    
    @staticmethod
    def points_to_numpy(points: List) -> np.ndarray:
        '''
        This function changes the given list of point objects to a numpy array.

        :param points: The list of points which should be converted.

        :return: All points in a 2 dimensional numpy array.
        '''

        coordinates = []
        for point in points:
            coordinates.append([point.x, point.y])
        return np.array(coordinates, dtype=float)