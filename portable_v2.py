#pip install pyinstaller
#pyinstaller -F -i "icon.ico" portable.py
#exe into dist folder

import numpy as np
import galois
import random
import getpass
import base64

def main():
    safe_start()

def safe_start():
    try:
        start_menu()
    except:
        print("\nUnknown error (maybe ctrl+c), emergency exit!")

def start_menu():
    f = True
    print("\nA soldering iron is into a black hole.")
    #thermorectal cryptanalysis
    if myhash(getpass.getpass("Login: ")) != 1314399736851798576:
        f = False
    if myhash(getpass.getpass("Password: ")) != 192441972608755898:
        f = False
    if f:
        print("Authorization successful, wait a bit.")
        menu()
    else:
        print("Permission denied.")
    print("\nPress ENTER to exit.", end = '')
    input()

def menu():
    order = 2 ** 8 # = p^m = 256 = byte size, we well encrypt each byte and save in base64 format
    n = order - 1 # = 255, (order - 1) mod n = 0 for Reed Solomon code (below i will name it RScode), n mod 3 = 0 for base64
    k = 210 #k mod 3 = 0 for base64, n >= k, RScode can correct (n - k) // 2 errors in message
    #
    #print(galois.GF(2 ** 8).properties) to know irreducible_poly and primitive_element (pyinstaller will not add database files)
    #example of path to *.db files is C:\Python_3_12_2\Lib\site-packages\galois\_databases and _interface.py (which opens the database) is also here
    #maybe it is possible to use --add-data pyinstaller option, but I didn't figure out which paths to write so that galois could find the database
    #you can write a function that changes the configuration of the cryptosystem, it is easy to change n and k and rebuild RScode during execution
    #and if you understand how to add database files using Pyinstaller, you can change the order during portable execution too
    #you can even use order = 2**7 (or any from 128 to 255 which is p^m where p is prime, m is natural) for ascii coding or make your own alphabet table
    #but if you want to change the order, you will have to give up the wonderful storage of keys and messages in base64 format...
    #...and use the first version of this program for saving raw integers (or reduce the order and abandon universal work for any encoding)
    #
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #_interface.py causes an error during portable execution if it cannot find the database, but there is a hint at the end of this file:
    #Alternatively, you can find irreducible polynomials with galois.irreducible_poly(p, m) or primitive polynomials with galois.primitive_poly(p, m).
    #maybe it the key to the solution of the database problem (as I understand, these functions don't use database), check it; and maybe verify = True 
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #nothing from the big comment above is needed if you don't want to build portable exe, just GF = galois.GF(order)
    #
    GF = galois.GF(2, 8, irreducible_poly = "x^8 + x^4 + x^3 + x^2 + 1", primitive_element = "x", verify = False)
    rs = galois.ReedSolomon(n, k, field = GF)
    print("\nMcEliece cryptosystem implementation by vovuas2003.\n")
    print("All necessary txt files must be located in the directory with this exe program.\n")
    info = "Menu numbers: 0 = exit, 1 = generate keys, 2 = encrypt, 3 = decrypt,\n4 = restore pubkey, 5 = break privkey_s, 6 = break privkey_p; h = help.\n"
    err = "Error! Check command info and try again!\n"
    ok = "Operation successful.\n"
    inp = [str(i) for i in range(7)] + ['h'] + ['1337']
    print(info)
    while True:
        s = input("Menu number: ")
        while s not in inp:
            s = input("Wrong menu number, h = help: ")
        if s == 'h':
            print(info)
        elif s == '0':
            print("\nGood luck!")
            break
        elif s == '1':
            print("This operation will rewrite pubkey.txt, privkey_s.txt and privkey_p.txt; are you sure?")
            if(not get_yes_no()):
                continue
            try:
                generate(n, k, GF, rs)
                print(ok)
            except:
                print(err)
        elif s == '2':
            print("Write your text into text.txt; pubkey.txt is required, message.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                encrypt(n, k, order, GF)
                print(ok)
            except:
                print(err)
        elif s == '3':
            print("You need message.txt, privkey_s.txt and privkey_p.txt; text.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                decrypt(n, k, GF, rs)
                print(ok)
            except:
                print(err)
        elif s == '4':
            print("You need privkey_s.txt and privkey_p.txt; pubkey.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                restore_G_(n, k, GF, rs)
                print(ok)
            except:
                print(err)
        elif s == '5':
            print("You need pubkey.txt and privkey_p.txt; privkey_s.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                break_S(n, k, GF)
                print(ok)
            except:
                print(err)
        elif s == '6':
            print("You need pubkey.txt and privkey_s.txt; privkey_p.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                break_P(n, k, GF, rs)
                print(ok)
            except:
                print(err)
        elif s == '1337':
            c = input("Move the soldering iron into the black hole number: ")
            try:
                PT(int(c))
            except:
                print("Iron: 'I don't know this hole.'")
                continue
        else:
            print("Impossible behaviour, mistake in source code!\nThe string allowed in the inp array is not bound to the call of any function!")
            break

def get_yes_no():
    s = input("Confirm (0 = go back, 1 = continue): ")
    while s not in ['0', '1']:
        s = input("Try again, 0 or 1: ")
    return int(s)

def myhash(s, m = 2**61 - 1, p = 257):
    a = 0
    for i in range(len(s)):
    	a = ((a * p) % m + ord(s[i])) % m
    return a

def PT(m):
    M = 5
    if m == 0:
        print("Iron: 'OK, I will choose the number by myself.'")
    while m == 0:
        m = random.randint(-M, M)
    s = "PT!"
    p = "   "
    f = False
    if m < 0:
        s, p = p, s
        m *= -1
        f = True
    if m > M:
        print("Iron: 'Are you sure to move me so far?'")
        if(not get_yes_no()):
            return
    print()
    if f:
        print(p * (10 * m + 1))
    print(p + (s * 3 + p + s * 3 + p + s + p) * m)
    print(p + (s + p + s + p * 2 + s + p * 2 + s + p) * m)
    print(p + (s * 3 + p * 2 + s + p * 2 + s + p) * m)
    print(p + (s + p * 4 + s + p * 4) * m)
    print(p + (s + p * 4 + s + p * 2 + s + p) * m)
    if f:
        print(p * (10 * m + 1))
    print()

def generate(n, k, GF, rs):
    S = generate_S(k, GF)
    G = rs.G
    P, p = generate_P(n, GF)
    G_ = S @ G @ P
    write_pubkey(G_)
    write_privkey_s(S)
    write_privkey_p(p)

def generate_S(k, GF):
    S = GF.Random((k, k))
    while np.linalg.det(S) == 0:
        S = GF.Random((k, k))
    return S

def generate_P(n, GF):
    r = [i for i in range(n)]
    p = []
    for i in range(n):
        p.append(r.pop(random.randint(0, n - 1 - i)))
    P = GF.Zeros((n, n))
    for i in range(n):
        P[i, p[i]] = 1
    return P, p

def write_pubkey(G_):
    rows = [bytes(row) for row in G_]
    output = "".join([base64.b64encode(row).decode() for row in rows])
    with open("pubkey.txt", "w") as f:
        f.write(output)

def write_privkey_s(S):
    rows = [bytes(row) for row in S]
    output = "".join([base64.b64encode(row).decode() for row in rows])
    with open("privkey_s.txt", "w") as f:
        f.write(output)

def write_privkey_p(p):
    output = base64.b64encode(bytes(p)).decode()
    with open("privkey_p.txt", "w") as f:
        f.write(output)

def read_pubkey(n, k):
    with open("pubkey.txt", "r") as f:
        out = f.read()
    out = [int(i) for i in base64.b64decode(out)]
    out = [out[i - n : i] for i in range(n, n * k + n, n)]
    return out

def read_privkey_s(k):
    with open("privkey_s.txt", "r") as f:
        out = f.read()
    out = [int(i) for i in base64.b64decode(out)]
    out = [out[i - k : i] for i in range(k, k * k + k, k)]
    return out

def read_privkey_p():
    with open("privkey_p.txt", "r") as f:
        out = f.read()
    return [int(i) for i in base64.b64decode(out)]

def build_P(n, GF, p):
    P = GF.Zeros((n, n))
    for i in range(n):
        P[i, p[i]] = 1
    return P

def build_P_inv(n, GF, p):
    P = GF.Zeros((n, n))
    for i in range(n):
        P[p[i], i] = 1
    return P

def pad_message(msg: bytes, pad_size: int) -> list[int]:
    padding = pad_size - (len(msg) % pad_size)
    return list(msg + padding.to_bytes() * padding)

def unpad_message(msg):
    padding_byte = msg[-1]
    for i in range(1, padding_byte + 1):
        if msg[-i] != padding_byte:
            print("Wrong privkey!")
            raise Exception()
    return msg[: -padding_byte]

def encrypt(n, k, order, GF):
    G_ = GF(read_pubkey(n, k))
    with open("text.txt", "r") as f:
        text = f.read()
    text = text.encode()
    out = ""
    while len(text) > k - 1:
        tmp = text[: k - 1]
        text = text[k - 1 :]
        out += encrypt_one(n, k, order, GF, G_, tmp)
    out += encrypt_one(n, k, order, GF, G_, text)
    with open("message.txt", "w") as f:
        f.write(out)

def encrypt_one(n, k, order, GF, G_, text):
    msg = pad_message(text, k)
    m = GF(msg)
    c = m.T @ G_
    t = (n - k) // 2
    z = np.zeros(n, dtype = int)
    p = [i for i in range(n)]
    for i in range(t):
        ind = p.pop(random.randint(0, n - 1 - i)) 
        z[ind] += random.randint(1, order - 1)
        z[ind] %= order
    c = c + GF(z)
    return base64.b64encode(bytes(c)).decode()

def decrypt(n, k, GF, rs):
    S_inv = np.linalg.inv(GF(read_privkey_s(k)))
    P_inv = GF(build_P_inv(n, GF, read_privkey_p()))
    with open("message.txt", "r") as f:
        msg = f.read()
    msg = [int(i) for i in base64.b64decode(msg)]
    msg = [msg[i - n : i] for i in range(n, len(msg) + n, n)]
    msg = [decrypt_one(rs, S_inv, P_inv, GF(i)) for i in msg]
    msg = [i for j in msg for i in j]
    msg = bytes(msg).decode()
    with open("text.txt", "w") as f:
        f.write(msg)

def decrypt_one(rs, S_inv, P_inv, msg):
    msg = msg @ P_inv
    msg, e = rs.decode(msg, errors = True)
    if e == -1:
        print("Too many erroneous values in message!")
        raise Exception()
    msg = msg @ S_inv
    msg = [int(i) for i in msg]
    msg = unpad_message(msg)
    return msg

def restore_G_(n, k, GF, rs):
    S = GF(read_privkey_s(k))
    G = rs.G
    P = GF(build_P(n, GF, read_privkey_p()))
    G_ = S @ G @ P
    write_pubkey(G_)

def break_S(n, k, GF):
    G_ = GF(read_pubkey(n, k))
    P_inv = GF(build_P_inv(n, GF, read_privkey_p()))
    S = G_ @ P_inv
    S = S[:, : k]
    write_privkey_s(S)

def break_P(n, k, GF, rs):
    G_ = GF(read_pubkey(n, k))
    S_inv = np.linalg.inv(GF(read_privkey_s(k)))
    G = rs.G
    G = G.T
    G = [[int(i) for i in j] for j in G]
    GP = S_inv @ G_
    GP = GP.T
    GP = [[int(i) for i in j] for j in GP]
    p = [0 for i in range(n)]
    f = False
    for i in range(n):
        f = False
        for j in range(n):
            if G[i] == GP[j]:
                p[i] = j
                f = True
                break
        if f:
            continue
        print("Wrong pubkey and privkey_s combination!")
        raise Exception()
    write_privkey_p(p)

if __name__ == "__main__":
    main()
