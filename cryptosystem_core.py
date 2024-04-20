#G = pubkey; S and P = privkeys; text = plaintext; msg = encrypted text
#all these variables are strings
#text must be in utf-8 encoding
#keys and messages is saves in base64 format

#Usage (see GUI and console examples):
#G, S, P = generate()
#msg = encrypt(G, text)
#text = decrypt(S, P, msg)
#G = restore_G(S, P)
#S = break_S(G, P)
#P = break_P(G, S)

import numpy as np
import galois
import random
import base64

order = 256 #= p^m = 2**8; encrypt each byte and save in base64 format
n = 255 #(order - 1) mod n = 0 for Reed Solomon code
k = 210 #k <= n, randomly change (n - k) div 2 bytes during encryption
GF = galois.GF(2, 8, irreducible_poly = "x^8 + x^4 + x^3 + x^2 + 1", primitive_element = "x", verify = False) #hardcoded GF.properties for pyinstaller
rs = galois.ReedSolomon(n, k, field = GF)

def main():
    pass

def config(string):
    global n
    global k
    global rs
    try:
        nn, kk = map(int, string.split()[:2])
        if kk < 2:
            raise Exception()
        rrss = galois.ReedSolomon(nn, kk, field = GF)
    except:
        raise Exception()
    else:
        n = nn
        k = kk
        rs = rrss

def generate():
    S = generate_S()
    G = rs.G
    P, p = generate_P()
    G_ = S @ G @ P
    return write_pubkey(G_), write_privkey_s(S), write_privkey_p(p)

def generate_S():
    S = GF.Random((k, k))
    while np.linalg.det(S) == 0:
        S = GF.Random((k, k))
    return S

def generate_P():
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
    row = bytes([i for j in rows for i in j])
    return base64.b64encode(row).decode()

def write_privkey_s(S):
    rows = [bytes(row) for row in S]
    row = bytes([i for j in rows for i in j])
    return base64.b64encode(row).decode()

def write_privkey_p(p):
    return base64.b64encode(bytes(p)).decode()

def read_pubkey(out):
    out = [int(i) for i in base64.b64decode(out)]
    out = [out[i - n : i] for i in range(n, n * k + n, n)]
    return out

def read_privkey_s(out):
    out = [int(i) for i in base64.b64decode(out)]
    out = [out[i - k : i] for i in range(k, k * k + k, k)]
    return out

def read_privkey_p(out):
    return [int(i) for i in base64.b64decode(out)]

def build_P(p):
    P = GF.Zeros((n, n))
    for i in range(n):
        P[i, p[i]] = 1
    return P

def build_P_inv(p):
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
            #print("Wrong privkey!")
            raise Exception()
    return msg[: -padding_byte]

def encrypt(key, text):
    G_ = GF(read_pubkey(key))
    text = text.encode("utf-8")
    out = bytes()
    while len(text) > k - 1:
        tmp = text[: k - 1]
        text = text[k - 1 :]
        out += encrypt_one(G_, tmp)
    out += encrypt_one(G_, text)
    return base64.b64encode(out).decode()

def encrypt_one(G_, text):
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
    return bytes(c)

def decrypt(s, p, msg):
    S_inv = np.linalg.inv(GF(read_privkey_s(s)))
    P_inv = GF(build_P_inv(read_privkey_p(p)))
    msg = [int(i) for i in base64.b64decode(msg)]
    msg = [msg[i - n : i] for i in range(n, len(msg) + n, n)]
    msg = [decrypt_one(S_inv, P_inv, GF(i)) for i in msg]
    msg = [i for j in msg for i in j]
    msg = bytes(msg).decode("utf-8")
    return msg

def decrypt_one(S_inv, P_inv, msg):
    msg = msg @ P_inv
    msg, e = rs.decode(msg, errors = True)
    if e == -1:
        #print("Too many erroneous values in message!")
        raise Exception()
    msg = msg @ S_inv
    msg = [int(i) for i in msg]
    msg = unpad_message(msg)
    return msg

def restore_G(s, p):
    S = GF(read_privkey_s(s))
    G = rs.G
    P = GF(build_P(read_privkey_p(p)))
    G_ = S @ G @ P
    return write_pubkey(G_)

def break_S(key, p):
    G_ = GF(read_pubkey(key))
    P_inv = GF(build_P_inv(read_privkey_p(p)))
    S = G_ @ P_inv
    S = S[:, : k]
    return write_privkey_s(S)

def break_P(key, s):
    G_ = GF(read_pubkey(key))
    S_inv = np.linalg.inv(GF(read_privkey_s(s)))
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
        #print("Wrong pubkey and privkey_s combination!")
        raise Exception()
    return write_privkey_p(p)

if __name__ == "__main__":
    main()
