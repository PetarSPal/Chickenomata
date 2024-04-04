class Beak:
    def __init__(self, sieve, head) -> None:
        self.sieve = sieve
        self.head = head
        
    def peck(self, value):
        sieved, leftovers = self.sieve(value)
        ##Passing self won't work, I need to manage self-rerence in the container housing the self
        ##Aka I need to work with the flock and and identifier for the beak in the flock
        self.head.beak_spit(self, leftovers)
        return sieved