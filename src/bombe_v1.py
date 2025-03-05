from collections import defaultdict
from itertools import product
from pyenigma import enigma, rotor
from utils import generate_rotor_positions

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Bombe_V1:

    def __init__(self, 
                 plaintext = "INYAIGCVPBGLGL", 
                 ciphertext = "YWAILLOTJYBZLI",
                 path_routes = ["IYAI", "IYBGLI", "IAYBGLI"],
                 path_start = "I"):

        # crib
        self.crib_cipher = ciphertext
        self.crib_plain = plaintext

        # menu paths
        self.n_paths = len(path_routes)
        self.paths = path_routes
        self.paths_input = path_start

        self.create_menu()


    def create_menu(self):

        self.menu = defaultdict()

        for i, letter_cipher in enumerate(self.crib_cipher):
            
            letter_plain = self.crib_plain[i]

            # letter cipher -> letter plain
            if letter_cipher not in self.menu:
                links_dict = defaultdict()
                links_dict[letter_plain] = [i]
                self.menu[letter_cipher] = links_dict
            else: 
                links_dict = self.menu[letter_cipher]
                if letter_plain not in links_dict:
                    links_dict[letter_plain] = [i]
                else:
                    links_list = links_dict[letter_plain]
                    links_list.append(i)
                    links_dict[letter_plain] = links_list
                    
                self.menu[letter_cipher] = links_dict

            # letter plain -> letter 
            if letter_plain not in self.menu:
                links_dict = defaultdict()
                links_dict[letter_cipher] = [i]
                self.menu[letter_plain] = links_dict
            else: 
                links_dict = self.menu[letter_plain]
                if letter_cipher not in links_dict:
                    links_dict[letter_cipher] = [i]
                else:
                    links_list = links_dict[letter_cipher]
                    links_list.append(i)
                    links_dict[letter_cipher] = links_list
                    
                self.menu[letter_plain] = links_dict

        print("----------------------------")
        print("Menu Diagram generated:")
        print("----------------------------")
        print(self.menu)

    def run(self, rotor_start="AAA", rotor_end="ZZZ"):

        rotor_positions_combinations = self.generate_rotor_positions(rotor_start, rotor_end)
        self.possibilities = defaultdict()
        plugboard_possible = defaultdict(list)

        # attempt with different rotors positions from 'AAA' to 'ZZZ'
        for rotor_positions in rotor_positions_combinations:

            self.contradictions = defaultdict()

            # guess plugboard from 'A' to 'Z'
            for guess in alphabet:

                # go through paths to check guess
                for path in self.paths:

                    guess_plug = f"{path[0]}{guess}"
                    machine = enigma.Enigma(
                            rotor.ROTOR_Reflector_C, 
                            rotor.ROTOR_I,
                            rotor.ROTOR_II, 
                            rotor.ROTOR_III, 
                            rotor_positions, # rotors initial position (key)
                            guess_plug  # assume that the start letter is swaped with the guess letter by plugboard
                        )

                    # print(self.paths, "===>", path)
                    # e.g. current path(loop) is I-Y-A-I
                    # then we have 3 edges in this path (IY)(YA)(AI)
                    edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                    c = path[0] # here c is still a plaintext letter
                    for edge in edges:
                        # search in the 'menu' diagram
                        # to tell how many offset is needed to reach next letter (e.g. I->Y)
                        offset = self.menu[edge[0]][edge[1]][0]
                        for _ in range(offset):      
                            # execute offset, to make rotors jump to next position
                            # 'X' here is ignorable, and this will not effect the real cipher c
                            machine.encipher("X") 
                        # encrypt it
                        c = machine.encipher(c)

                    # When all edges are traversed, 
                    # we return to the starting point of the loop again
                    # now verify if our guess is the same as the simulation output
                    if c == guess:
                        # we found a valid guess
                        plugboard_possible[rotor_positions].append(guess_plug)
                        # print(f"{rotor_positions}: {plugboard_possible[rotor_positions]}")
                    # else:
                        # let's try another guess
                        # if all the guesses are invalid in the end
                        # we need to try another rotors position and loop again

        return plugboard_possible
    
    def generate_rotor_positions(self, start="AAA", end="ZZZ"):
        length = len(start)  
    
        all_combinations = [''.join(i) for i in product(alphabet, repeat=length)]
        
        start_idx = all_combinations.index(start)
        end_idx = all_combinations.index(end) + 1  
        
        return all_combinations[start_idx:end_idx]