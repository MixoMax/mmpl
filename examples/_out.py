
import math
from functools import partial

def handle_errors(func, default=None):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result if result is not None else default
        except Exception:
            return default
    return wrapper

class ArrowWrapper:
    def __init__(self, value):
        self.value = value

    def __gt__(self, func):
        if callable(func):
            if isinstance(self.value, (list, tuple, set)):
                return ArrowWrapper(map(func, self.value))
            return ArrowWrapper(func(self.value))
        return ArrowWrapper(self.value)

    def __iter__(self):
        return iter(self.value)


defprime_factors(n):
    factors=[]
    foriin2...math.sqrt(n)+1:
        whilen%i==0:
            factors.append(i)
            n=n/i
            
        
    ifn>1:
        factors.append(n)
        
    returnfactors
    


defmain():
    input_str="65 3 abc -350"
    nums=input_str.split(" ")  ()int if _ is not None else  0
    factors=nums  ()prime_factors
    factors_squared=factors  ()(x)=>:x*x
    print(factors_squared)
    