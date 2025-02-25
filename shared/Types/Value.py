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