from collections import defaultdict
from itertools import product

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_rotor_positions(start="AAA", end="ZZZ"):
    length = len(start)  
    
    all_combinations = [''.join(i) for i in product(alphabet, repeat=length)]
        
    start_idx = all_combinations.index(start)
    end_idx = all_combinations.index(end) + 1  
        
    return all_combinations[start_idx:end_idx]