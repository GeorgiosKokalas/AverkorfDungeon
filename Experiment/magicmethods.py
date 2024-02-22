class A:
    def __init__(self):
        self._b = None
    
    @property
    def b(self):
        return self._b
    
    @b.setter
    def b(self, value):
        if isinstance(value, int):
            self._b = value
        else:
            raise ValueError("b must be an integer")
    
    def __add__(self, other):
        if isinstance(other, int):
            return self.b + other
        else:
            raise ValueError("Only integer can be added to b")

    def __sub__(self, other):
        if isinstance(other, int):
            return self.b - other
        else:
            raise ValueError("Only integer can be subtracted from b")

# Example usage:
obj = A()
obj.b = 5
print(obj.b)  # Output: 5

# Add 3 to b
obj.b += 3
print(obj.b)  # Output: 8

property