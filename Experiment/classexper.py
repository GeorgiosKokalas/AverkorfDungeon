from typing import Any

class a:
    def __init__(self):
        self.val = 1

    def __call__(self):
        return self.val
    
b = a
print(b)