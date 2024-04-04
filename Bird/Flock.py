class Flock:
    def __init__(self, chicken, head) -> None:
        self.chicken = chicken
        self.head = head
        
    def hatch(self, value):
        sieved, leftovers = self.sieve(value)
        self.side_effect(leftovers)
        return sieved