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