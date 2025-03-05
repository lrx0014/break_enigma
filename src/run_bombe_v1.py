from bombe_v1 import Bombe_V1
from pyenigma import enigma
from pyenigma import rotor
import ast

### CONFIG
plaintext = "INYAIGCVPBGLGL"
ciphertext = "YWAILLOTJYBZLI"
path_routes = ["IAYBGLI", "IYA", "IYBGLI", "LI", "LG"]
path_start = "I"

bombe_machine = Bombe_V1(plaintext, ciphertext, path_routes, path_start)

print("--------------------")
print("Started Bombing...")
print("--------------------")

possible_plugboards = bombe_machine.run(rotor_start="AAA", rotor_end="AAZ")

for k, v in possible_plugboards.items():
    print(k, v)
