import numpy as np
import galois
import random

n = 127
k = 32
order = 2 ** 7
GF = galois.GF(order)

def main():
    S = generate_S()
    G = generate_G()
    P = generate_P()
    G_ = S @ G @ P
    export_pubkey(G_)
    export_privkey(S, P)
    print("Done!")

def generate_S():
    S = GF.Random((k, k))
    while np.linalg.det(S) == 0:
        S = GF.Random((k, k))
    return S

def generate_G():
    rs = galois.ReedSolomon(n, k, field=GF)
    G = rs.G
    return G

def generate_P():
    r = [i for i in range(n)]
    p = []
    for i in range(n):
        p.append(r.pop(random.randint(0, n - 1 - i)))
    P = GF.Zeros((n, n))
    for i in range(n):
        P[i, p[i]] = 1
    return P

def export_pubkey(G_):
    rows = [", ".join([str(int(cell)) for cell in row]) for row in G_]
    output = "G_ = [ " + ",\n".join([f"[{row}]" for row in rows]) + " ]"
    with open("pubkey.py", "w") as f:
        f.write(output)
        f.write("\ndef get():\n\treturn G_")

def export_privkey(S, P):
    rows = [", ".join([str(int(cell)) for cell in row]) for row in S]
    output = "S = [ " + ",\n".join([f"[{row}]" for row in rows]) + " ]\n"
    rows = [", ".join([str(int(cell)) for cell in row]) for row in P]
    output += "P = [ " + ",\n".join([f"[{row}]" for row in rows]) + " ]\n"
    with open("privkey.py", "w") as f:
        f.write(output)
        f.write("\ndef get_S():\n\treturn S")
        f.write("\ndef get_P():\n\treturn P")

if __name__ == "__main__":
    main()
