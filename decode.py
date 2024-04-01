import numpy as np
import galois

import privkey
import message

n = 127
k = 32
order = 2 ** 7
GF = galois.GF(order)

def main():
    S = GF(privkey.get_S())
    P = GF(privkey.get_P())
    c = GF(message.get())
    print(decode(S, P, c))

def unpad_message(msg):
    padding_byte = msg[-1]
    for i in range(1, padding_byte + 1):
        if msg[-i] != padding_byte:
            raise ValueError("Incorrect padding!")
    return msg[:-padding_byte]

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

if __name__ == "__main__":
    main()
