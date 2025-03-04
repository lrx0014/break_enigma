from bombe import Bombe
from pyenigma import enigma
from pyenigma import rotor
import ast

### CONFIG
plaintext = "INYAIGCVPBGLGL"
ciphertext = "YWAILLOTJYBZLI"
path_routes = ["IYAI", "IYBGLI", "IAYBGLI"]
path_start = "I"

bombe_machine = Bombe(plaintext, ciphertext, path_routes, path_start)

print("--------------------")
print("Started Bombing...")
print("--------------------")

possible_plugboards = bombe_machine.run()
n_possible_plugboards = len(possible_plugboards.keys())

is_decrypted = False

for frozen_plugboard in possible_plugboards:
    plugboard_pairs = ast.literal_eval(str(frozen_plugboard))
    plugboard_pairs = [pair for pair in plugboard_pairs if pair[0] != pair[1]]
    unique_pairs = {frozenset(pair) for pair in plugboard_pairs}
    plugboard_pairs = [tuple(pair) for pair in unique_pairs]
    plugboard_uses = " ".join("".join(pair) for pair in plugboard_pairs)

    rotor_positions = possible_plugboards[frozen_plugboard]
    for rp in rotor_positions:

        machine = enigma.Enigma(
            rotor.ROTOR_Reflector_C, 
            rotor.ROTOR_I,
            rotor.ROTOR_II, 
            rotor.ROTOR_III, 
            str(rp), 
            str(plugboard_uses))
            
        ciphered = machine.encipher(plaintext)
            
        print(rp, ' / ', plugboard_uses, ' / ', ciphered)

        if ciphered == ciphertext:
            print(f"Decrypted!!")
            is_decrypted = True
            break

    if is_decrypted:
        break    
