import numpy as np
import galois

import pubkey

n = 127
k = 32
order = 2 ** 7
GF = galois.GF(order)

def main():
    G_ = GF(pubkey.get())
    print("Message to encode (max len = k-1 = 31):")
    message = input()
    if len(message) > k-1:
        print("Message is too long!")
        return
    ct = encrypt(G_, message)
    ct = list(map(int, ct))
    export(ct)
    print("Done!")

def pad_message(msg: bytes, pad_size: int) -> list[int]:
    padding = pad_size - (len(msg) % pad_size)
    return list(msg + padding.to_bytes() * padding)

def encrypt(G_, text):
    msg = pad_message(text.encode(), k)
    m = GF(msg)
    c = m.T @ G_
    return c

def export(ct):
    output = "ct = [ " + ", ".join([str(int(cell)) for cell in ct]) + " ]"
    with open("message.py", "w") as f:
        f.write(output)
        f.write("\ndef get():\n\treturn ct")

if __name__ == "__main__":
    main()
