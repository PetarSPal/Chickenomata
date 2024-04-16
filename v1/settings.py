"""
Configs for handling reasonable defaults
"""

class Engine_cfg:
    def __init__(self):
        self.runs = 100


class Grass_cfg:
    def __init__(self):
        self._cols = 675
        self._ndims = 1
        ###Currently o
        self._shape = (675, )
        self.asym = 'left'
        self.initial_condition = 'center'
        self.wrap = ''
    
    @property
    def shape(self):
        return self._shape
    
    @shape.setter
    def shape(self, value):
        self._ndims = len(value)
        self._cols = max(value)
        self._shape = value
        
    @property
    def cols(self):
        return self._cols
    
    @cols.setter
    def cols(self, value):
        self._shape = tuple(value for _ in range(self.ndims))
        self._cols = value
    
    @property
    def ndims(self):
        return self._ndims
    
    @ndims.setter
    def ndims(self, value):
        self._shape = tuple(self._cols for _ in range(value))
        self._ndims = value