import numpy as np
import galois
import random
import getpass
import hashlib
import pyperclip

def main():
    try:
        menu()
    except:
        print("Error!")

def menu():
    core = McEliece_core()
    core.generate_keys(normalhash(getpass.getpass("Password: ")))
    pyperclip.copy(bytes(core.decrypt([int(i) for i in read_file("only_password")])).decode('utf-8'))
    print("OK!")

class McEliece_core:
    def __init__(self):
        self._order = 256
        self._n = 255
        self._k = 210
        self._GF = galois.GF(2, 8, irreducible_poly = "x^8 + x^4 + x^3 + x^2 + 1", primitive_element = "x", verify = False)
        self._rs = galois.ReedSolomon(self._n, self._k, field = self._GF)
        self._G = self._GF.Zeros((self._k, self._n))
        self._S = self._GF.Zeros((self._k, self._k))
        self._S_inv = self._GF.Zeros((self._k, self._k))
        self._P = self._GF.Zeros((self._n, self._n))
        self._P_inv = self._GF.Zeros((self._n, self._n))
        self._p = [0 for i in range(self._n)]
    def generate_keys(self, seed):
        seed %= 2**32
        self._unsafe_generate_S(seed)
        self._unsafe_generate_P(seed)
        self._G = self._S @ self._rs.G @ self._P
    def decrypt(self, msg):
        try:
            msg = [msg[i - self._n : i] for i in range(self._n, len(msg) + self._n, self._n)]
            msg = [self._decrypt_one(self._GF(i)) for i in msg]
            return [i for j in msg for i in j]
        except:
            raise
    def _unsafe_generate_S(self, seed):
        pseudo = np.random.RandomState(seed)
        S = self._GF(pseudo.randint(0, self._order, (self._k, self._k)))
        while np.linalg.det(S) == 0:
            S = self._GF(pseudo.randint(0, self._order, (self._k, self._k)))
        self._S = S
        self._S_inv = np.linalg.inv(S)
    def _unsafe_generate_P(self, seed):
        pseudo = np.random.RandomState(seed)
        p = [i for i in range(self._n)]
        pseudo.shuffle(p)
        self._p = p
        self._P = self._GF.Zeros((self._n, self._n))
        self._P_inv = self._GF.Zeros((self._n, self._n))
        for i in range(self._n):
            self._P[i, p[i]] = 1
            self._P_inv[p[i], i] = 1
    def _decrypt_one(self, msg):
        msg = msg @ self._P_inv
        msg, e = self._rs.decode(msg, errors = True)
        if e == -1:
            raise Exception()
        msg = msg @ self._S_inv
        msg = [int(i) for i in msg]
        try:
            msg = self._unpad_message(msg)
        except:
            raise
        return msg
    def _unpad_message(self, msg):
        last_value = msg[-1]
        if last_value >= self._k or last_value <= 0:
            raise Exception()
        for i in range(1, last_value + 1):
            if msg[-i] != last_value:
                raise Exception()
        return msg[: -last_value]

def read_file(name):
    with open(name, "rb") as f:
        data = f.read()
    return data

def normalhash(s):
    return int(hashlib.sha256(bytearray(s, 'utf-8')).hexdigest(), 16)

if __name__ == "__main__":
    main()
