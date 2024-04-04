class Chicken:
    def __init__(self, beak, raptor, egg) -> None:
        self.beak = beak
        self.raptor = raptor
        self.egg = egg
        
    def graze(self, value):
        crop = self.beak.peck(value)
        heritage = self.raptor.bless(crop)
        output = self.egg.hatch(heritage)
        return output