class card:
    # NOTE: currently assumes all valid attribute names
    # future versions can use __slots__ or set of valid keys
    # currently, to keep card methods/database columns flexible, we are naively assigning. 
    def __init__(self, **kwargs): 
        for key, value in kwargs.items(): 
            setattr(self, key, value)
    

    def __str__(self): 
        accum = ""
        for item in self.__dict__.items():
            accum += str(item) +"\n"
        return accum
            
