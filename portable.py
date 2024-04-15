#pip install pyinstaller
#pyinstaller -F -i "icon.ico" portable.py

import numpy as np
import galois
import random
import getpass

def main():
    start_menu()

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
    order = 2 ** 8
    n = order - 1
    k = 210
    #print(galois.GF(2 ** 8).properties)
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
                decrypt(n, GF, rs)
                print(ok)
            except:
                print(err)
        elif s == '4':
            print("You need privkey_s.txt and privkey_p.txt; pubkey.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                restore_G_(n, GF, rs)
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
                break_P(n, GF, rs)
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
    write_privkey(S, p)

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
    rows = [" ".join([str(int(cell)) for cell in row]) for row in G_]
    output = "\n".join(rows)
    with open("pubkey.txt", "w") as f:
        f.write(output)

def write_privkey(S, p):
    output = " ".join([str(i) for i in p])
    with open("privkey_p.txt", "w") as f:
        f.write(output)
    rows = [" ".join([str(int(cell)) for cell in row]) for row in S]
    output = "\n".join(rows)
    with open("privkey_s.txt", "w") as f:
        f.write(output)

def read_pubkey():
    out = []
    tmp = []
    with open("pubkey.txt", "r") as f:
        while True:
            tmp = f.readline()
            if not tmp:
                break
            out.append([int(i) for i in tmp.split()])
    return out

def read_privkey_s():
    out = []
    tmp = []
    with open("privkey_s.txt", "r") as f:
        while True:
            tmp = f.readline()
            if not tmp:
                break
            out.append([int(i) for i in tmp.split()])
    return out

def read_privkey_p():
    with open("privkey_p.txt", "r") as f:
        out = f.readline().split()
    return [int(i) for i in out]

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
    return msg[:-padding_byte]

def encrypt(n, k, order, GF):
    G_ = GF(read_pubkey())
    with open("text.txt", "r") as f:
        text = f.read()
    text = text.encode()
    with open("message.txt", "w") as f:
        while len(text) > k - 1:
            tmp = text[: k - 1]
            text = text[k - 1 :]
            c = encrypt_one(n, k, order, GF, G_, tmp)
            f.write(" ".join([str(i) for i in c]))
            f.write("\n")
        c = encrypt_one(n, k, order, GF, G_, text)
        f.write(" ".join([str(i) for i in c]))

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
    return c + GF(z)

def decrypt(n, GF, rs):
    S_inv = np.linalg.inv(GF(read_privkey_s()))
    P_inv = GF(build_P_inv(n, GF, read_privkey_p()))
    s = []
    with open("message.txt", "r") as inp, open("text.txt", "w") as out:
        while True:
            msg = inp.readline()
            if not msg:
                break
            msg = GF(list(map(int, msg.split())))
            s += decrypt_one(rs, S_inv, P_inv, msg)
        out.write(bytes(s).decode())

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

def restore_G_(n, GF, rs):
    S = GF(read_privkey_s())
    G = rs.G
    P = GF(build_P(n, GF, read_privkey_p()))
    G_ = S @ G @ P
    write_pubkey(G_)

def break_S(n, k, GF):
    G_ = GF(read_pubkey())
    P_inv = GF(build_P_inv(n, GF, read_privkey_p()))
    S = G_ @ P_inv
    S = S[:, : k]
    rows = [" ".join([str(int(cell)) for cell in row]) for row in S]
    output = "\n".join(rows)
    with open("privkey_s.txt", "w") as f:
        f.write(output)

def break_P(n, GF, rs):
    G_ = GF(read_pubkey())
    S_inv = np.linalg.inv(GF(read_privkey_s()))
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
    output = " ".join([str(i) for i in p])
    with open("privkey_p.txt", "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
