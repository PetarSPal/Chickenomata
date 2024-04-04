class Head:
    def __init__(self) -> None:
        self.beak_effect = lambda _, __: __
        self.egg_effect = lambda _, __: __
        
    def beak_spit(self, beak, value):
        self.beak_effect(beak, value)
    
    def egg_crack(self, egg, value):
        self.egg_effect(egg, value)
        
        