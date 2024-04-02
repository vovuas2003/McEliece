#break cryptosystem if know a half of private key

import numpy as np
import galois

import pubkey
import privkey
import message

n = 127
k = 32
order = 2 ** 7
GF = galois.GF(order)

def main():
    G_ = GF(pubkey.get()) #we need to know a public matrix
    P = GF(privkey.get_P()) #and P - only one of two private matrices
    S = break_S(P, G_) #to calculate S - the second part of private key
    c = GF(message.get())
    print(decode(S, P, c)) #and decode the message

def unpad_message(msg):
    padding_byte = msg[-1]
    for i in range(1, padding_byte + 1):
        if msg[-i] != padding_byte:
            raise ValueError("Incorrect padding!")
    return msg[:-padding_byte]

def my_fix(A):
    #make square matrix by deleting right columns
    l = len(A)
    r = GF.Zeros((l, l))
    for i in range(l):
        for j in range(l):
            r[i][j] = A[i][j]
    return r

def decode(S, P, c):
    rs = galois.ReedSolomon(n, k, field=GF)
    c = c @ np.linalg.inv(P)
    c = rs.decode(c)
    c = c @ np.linalg.inv(S)
    c = [int(i) for i in c]
    c = unpad_message(c)
    c = bytes(c)
    c = c.decode()
    return c

def break_S(P, G_):
    return my_fix(G_ @ np.linalg.inv(P)) #works for Reed-Solomon
    #G_ = S @ G @ P
    rs = galois.ReedSolomon(n, k, field=GF)
    G = rs.G
    G_ = G_ @ np.linalg.inv(P)
    G_ = my_fix(G_)
    G = my_fix(G) #returns E because we use Reed-Solomon algo
    S = G_ @ np.linalg.inv(G)
    return S

if __name__ == "__main__":
    main()
