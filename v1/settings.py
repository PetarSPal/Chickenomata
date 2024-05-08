"""
Configuration model
"""


class Cfg:
    """Configuration"""

    def __init__(self):
        # Engine:
        self.runs = 100
        self.width = 1360
        self.height = 690
        self.grayscale = False
        # Grass:
        self._cols = 250
        self._ndim = 1
        self.in_system = 2
        self.num_outputs = 1
        # Currently o
        self._shape = (675, )
        self.asym = 'left'
        self.initial_condition = 'center'
        self.wrap = ''

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._ndim = len(value)
        self._cols = max(value)
        self._shape = value

    @property
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, value):
        self._shape = tuple(value for _ in range(self.ndim))
        self._cols = value

    @property
    def ndim(self):
        return self._ndim

    @ndim.setter
    def ndim(self, value):
        self._shape = tuple(self._cols for _ in range(value))
        self._ndim = value
