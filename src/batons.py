from pyenigma import enigma, rotor

# check if substitution (A B) has contradiction
def no_contradiction(A, B):
    if len(A) != len(B):  
        return False

    mapping = {} 

    for a, b in zip(A, B):
        if a in mapping and mapping[a] != b:
            return False
        if b in mapping and mapping[b] != a:
            return False
        
        mapping[a] = b
        mapping[b] = a

    return True  

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
rotor1 = rotor.ROTOR_I

def batons(plaintext, ciphertext):
    pos_num = 0
    found_keys = []
    # verify each letter from A to Z
    for pos in alpha:
        rotor1.state = pos
        plain_mapped = ""
        cipher_mapped = ""
        # input letters one by one as: ZP^(-i)NP(p) = P^(-i)NP(c)
        for j in range(len(plaintext)):
            plain_mapped += rotor1.encipher_right(plaintext[j])
            cipher_mapped += rotor1.encipher_right(ciphertext[j])
            rotor1.notch()
            if rotor1.is_in_turnover_pos():
                print("* NOTCH REACHED")
    
        print(f"[{pos_num}]{pos}\n{plain_mapped}\n{cipher_mapped}")
        pos_num += 1
        print()
        if no_contradiction(plain_mapped, cipher_mapped):
            found_keys.append(pos)

    if len(found_keys) > 0:
        print(f"Found keys {found_keys} without any contradictions")
    else:
        print("No keys found")
    print()

rotor2 = rotor.ROTOR_II
def batons_v2(plaintext, ciphertext):
    pos_num = 0
    found_keys = []
    # verify each letter from A to Z
    for pos in alpha:
        rotor1.state = pos
        for pos_mid in alpha:
            rotor2.state = pos_mid
            plain_mapped = ""
            cipher_mapped = ""
            # input letters one by one as: ZP^(-i)NP(p) = P^(-i)NP(c)
            for j in range(len(plaintext)):
                if rotor1.is_in_turnover_pos():
                    rotor2.notch()
                    print("* NOTCH REACHED")
                rotor1.notch()
                plain_mapped += rotor2.encipher_right(rotor1.encipher_right(plaintext[j]))
                cipher_mapped += rotor2.encipher_right(rotor1.encipher_right(ciphertext[j]))
        
            print(f"[{pos_num}]{pos}{pos_mid}\n{plain_mapped}\n{cipher_mapped}")
            pos_num += 1
            print()
            if no_contradiction(plain_mapped, cipher_mapped):
                found_keys.append(pos+pos_mid)

    if len(found_keys) > 0:
        print(f"Found keys {found_keys} without any contradictions")
    else:
        print("No keys found")
    print()