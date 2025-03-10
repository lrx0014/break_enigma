from collections import defaultdict
from itertools import product
from pyenigma import enigma, rotor
from utils import generate_rotor_positions

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Bombe_V2:

    def __init__(self, 
                 plaintext = "INYAIGCVPB", 
                 ciphertext = "YWAILLOTJY",
                 path_routes = ["BYAILG"],
                 path_start = "B"):

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

    
    def add_contradiction(self, letter, letter_cipher):
        if letter not in self.contradictions:
            self.contradictions[letter] = set([letter_cipher])
        else: 
            plug_contradictions = self.contradictions[letter]
            plug_contradictions.add(letter_cipher)
            self.contradictions[letter] = plug_contradictions

        if letter_cipher not in self.contradictions:
            self.contradictions[letter_cipher] = set([letter])
        else: 
            plug_contradictions = self.contradictions[letter_cipher]
            plug_contradictions.add(letter)
            self.contradictions[letter_cipher] = plug_contradictions


    def run(self, rotor_start="AAA", rotor_end="ZZZ"):

        rotor_positions_combinations = generate_rotor_positions(rotor_start, rotor_end)
        self.possibilities = defaultdict()

        for rotor_positions in rotor_positions_combinations:

            self.contradictions = defaultdict()

            for guess in alphabet:
                plugboard = defaultdict()
                plugboard[self.paths_input] = guess
                plugboard[guess] = self.paths_input
                plugboard_possible = True

                # go through paths to check guess
                for path in self.paths:

                    machine = enigma.Enigma(
                            rotor.ROTOR_Reflector_C, 
                            rotor.ROTOR_I,
                            rotor.ROTOR_II, 
                            rotor.ROTOR_III, 
                            str(rotor_positions), # rotors initial position (key)
                            str(f"{path[0]}{guess}") # assume that the start letter is swaped with the guess letter by plugboard
                        )
                    
                    for i in range( len(path) - 1 ): 

                        letter = path[i]
                        letter_connections = self.menu[letter]

                        letter_cipher = path[i+1]
                        letter_cipher_positions = letter_connections[letter_cipher] 

                        cipher_offset = letter_cipher_positions[0]

                        for offset in range(cipher_offset):
                            machine.encipher("X")

                        if ((letter in plugboard) and plugboard_possible): 
                            plug_letter = plugboard[letter]
                            plug_letter_cipher = machine.encipher(plug_letter)

                            if letter_cipher in self.contradictions:

                                plug_contradictions = self.contradictions[letter_cipher]

                                if plug_letter_cipher in plug_contradictions:
                                    
                                    # merge with contradictions dictionary
                                    for plug in plugboard:
                                        plug_cipher = plugboard[plug]
                                        self.add_contradiction(plug, plug_cipher)

                                    # not worth keep checking on an inconsistency
                                    plugboard_possible = False
                                    break
                            
                            if letter_cipher in plugboard:

                                if (plugboard[letter_cipher] == plug_letter_cipher):
                                    break
                                else:
                                    # merge with contradictions dictionary
                                    self.add_contradiction(letter_cipher, plug_letter_cipher)
                                    for plug in plugboard:
                                        plug_cipher = plugboard[plug]
                                        self.add_contradiction(plug, plug_cipher)

                                    # not worth keep checking on an inconsistency
                                    plugboard_possible = False
                                    break
                            else: 
                                plugboard[letter_cipher] = plug_letter_cipher
                                plugboard[plug_letter_cipher] = letter_cipher
                    
                    if not plugboard_possible:
                        # no more assumptions can be made
                        # just skip
                        # let's try another guess
                        # if all the guesses are invalid in the end
                        # we need to try another rotors position and loop again
                        break

                # found a potential result
                if plugboard_possible:
                    tuple_plugboard = tuple(sorted(plugboard.items()))
                    if tuple_plugboard not in self.possibilities:
                        self.possibilities[tuple_plugboard] = [rotor_positions]
                    else:
                        self.possibilities[tuple_plugboard].append(rotor_positions)

        return self.possibilities
