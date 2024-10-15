#McEliece cryptosystem implementation by vovuas2003
#v2. Power of Python OOP.

#Usage (check main function or class implementation):
#G = pubkey; S and p = privkeys; text = plaintext; msg = encrypted text.
#All these variables must be lists of integers from 0 to 255. Easy to use binary files (check console_v2).
#It is possible to rewrite my class McEliece_core and add changing the order of Galois Field (check galois lib docs) to M, so all these variables will be lists of integers from 0 to M-1.
#But it will be impossible to save keys and encrypted texts as binary files. Also you will need to add polynomial database for pyinstaller.

import numpy as np
import galois
import random

#import cryptosystem_core_v2 as ME_core
#core = ME_core.McEliece_core()

def main(): #comment "return" for testing
    return
    core = McEliece_core()
    n, k = core.get_config()
    print(n, k)
    core.change_config(5, 3) #check comments in class implementation to understand possible values
    n, k = core.get_config()
    print(n, k)
    print()
    core.generate_keys() #true random
    print(core.get_pubkey())
    print(core.get_privkey_S())
    print(core.get_privkey_p())
    print()
    core.generate_keys(sum([ord(i) for i in list("password")])) #very simple seed
    G = core.get_pubkey()
    S = core.get_privkey_S()
    p = core.get_privkey_p()
    print(G)
    print(S)
    print(p)
    print()
    core.change_config(5, 3) #unset all keys inside core
    core.set_privkey_S(S)
    core.set_privkey_p(p)
    core.restore_pubkey()
    print(core.get_pubkey() == G)
    core.change_config(5, 3) #unset all keys inside core
    core.set_pubkey(G)
    core.set_privkey_p(p)
    core.restore_privkey_S()
    print(core.get_privkey_S() == S)
    core.change_config(5, 3) #unset all keys inside core
    core.set_pubkey(G)
    core.set_privkey_S(S)
    core.restore_privkey_p()
    print(core.get_privkey_p() == p)
    print()
    for j in range(2):
        text = [i + 1 for i in range(5)]
        msg = core.encrypt(text)
        print(msg)
        text = core.decrypt(msg)
        print(text)
        print()
    print("All tests are finished!")

class McEliece_core:
    def __init__(self):
        self._order = 256 #p^m = 2**8; encryption of each byte
        self._n = 255 #(order - 1) mod n = 0 for Reed Solomon code; 255 = 3 * 5 * 17 = (order - 1)
        self._k = 210 #2 <= k <= n; randomly change (n - k) div 2 bytes during encryption, but add (n - k + 1) bytes to each chunk with len (k - 1); k != 1 for padding function; k almost equal to n is very bad because of small amount of randomly changed bytes (k == n -> privkey for decryption == numpy.linalg.inv(pubkey))
        self._GF = galois.GF(2, 8, irreducible_poly = "x^8 + x^4 + x^3 + x^2 + 1", primitive_element = "x", verify = False) #hardcoded galois.GF(2**8).properties for pyinstaller
        self._rs = galois.ReedSolomon(self._n, self._k, field = self._GF)
        self._G = self._GF.Zeros((self._k, self._n)) #pubkey
        self._S = self._GF.Zeros((self._k, self._k)) #1st part of privkey
        self._S_inv = self._GF.Zeros((self._k, self._k)) #for decryption
        self._P = self._GF.Zeros((self._n, self._n)) #2nd part of privkey
        self._P_inv = self._GF.Zeros((self._n, self._n)) #for decryption
        self._p = [0 for i in range(self._n)] #compact format of P as a permutation array
    def change_config(self, n, k):
        try:
            if k < 2:
                raise Exception()
            rs = galois.ReedSolomon(n, k, field = self._GF)
        except:
            raise Exception()
        else:
            self._n = n
            self._k = k
            self._rs = rs
            #Also unset all keys!
            self._G = self._GF.Zeros((self._k, self._n))
            self._S = self._GF.Zeros((self._k, self._k))
            self._S_inv = self._GF.Zeros((self._k, self._k))
            self._P = self._GF.Zeros((self._n, self._n))
            self._P_inv = self._GF.Zeros((self._n, self._n))
            self._p = [0 for i in range(self._n)]
    def get_config(self):
        return self._n, self._k
    def generate_keys(self, seed = None):
        if seed == None:
            self._generate_S()
            self._generate_P()
        elif type(seed) != int:
            raise Exception()
        else:
            self._unsafe_generate_S(seed % (2**32))
            self._unsafe_generate_P(seed % (2**32))
        self._G = self._S @ self._rs.G @ self._P
    def get_pubkey(self):
        return [int(i) for j in self._G for i in j]
    def get_privkey_S(self):
        return [int(i) for j in self._S for i in j]
    def get_privkey_p(self):
        return self._p
    def set_pubkey(self, G):
        try:
            G = [G[i - self._n : i] for i in range(self._n, self._n * self._k + self._n, self._n)]
            G = self._GF(G)
        except:
            raise Exception()
        else:
            self._G = G
    def set_privkey_S(self, S):
        try:
            S = [S[i - self._k : i] for i in range(self._k, self._k * self._k + self._k, self._k)]
            S = self._GF(S)
            S_inv = np.linalg.inv(S)
        except:
            raise Exception()
        else:
            self._S = S
            self._S_inv = S_inv
    def set_privkey_p(self, p):
        if sorted(p) != [i for i in range(self._n)]:
            raise Exception()
        else:
            self._p = p
            self._P = self._GF.Zeros((self._n, self._n))
            self._P_inv = self._GF.Zeros((self._n, self._n))
            for i in range(self._n):
                self._P[i, p[i]] = 1
                self._P_inv[p[i], i] = 1
    def restore_pubkey(self):
        self._G = self._S @ self._rs.G @ self._P
    def restore_privkey_S(self):
        S = self._G @ self._P_inv
        S = self._GF(S[:, : self._k])
        try:
            S_inv = np.linalg.inv(S)
        except:
            raise Exception()
        self._S = S
        self._S_inv = S_inv
    def restore_privkey_p(self):
        G = self._rs.G
        G = G.T
        G = [[int(i) for i in j] for j in G]
        GP = self._S_inv @ self._G
        GP = GP.T
        GP = [[int(i) for i in j] for j in GP]
        p = [0 for i in range(self._n)]
        f = False
        for i in range(self._n):
            f = False
            for j in range(self._n):
                if G[i] == GP[j]:
                    p[i] = j
                    f = True
                    break
            if f:
                continue
            raise Exception()
        self._p = p
        self._P = self._GF.Zeros((self._n, self._n))
        self._P_inv = self._GF.Zeros((self._n, self._n))
        for i in range(self._n):
            self._P[i, p[i]] = 1
            self._P_inv[p[i], i] = 1
    def encrypt(self, text):
        try:
            out = []
            while len(text) > self._k - 1:
                tmp = text[: self._k - 1]
                text = text[self._k - 1 :]
                out += self._encrypt_one(tmp)
            out += self._encrypt_one(text)
            return out
        except:
            raise Exception()
    def decrypt(self, msg):
        try:
            msg = [msg[i - self._n : i] for i in range(self._n, len(msg) + self._n, self._n)]
            msg = [self._decrypt_one(self._GF(i)) for i in msg]
            return [i for j in msg for i in j]
        except:
            raise Exception()
#End of top-level functions, please do NOT use functions below without understanding!
    def _generate_S(self):
        S = self._GF.Random((self._k, self._k))
        while np.linalg.det(S) == 0:
            S = self._GF.Random((self._k, self._k))
        self._S = S
        self._S_inv = np.linalg.inv(S)
    def _generate_P(self):
        r = [i for i in range(self._n)]
        p = []
        for i in range(self._n):
            p.append(r.pop(random.randint(0, self._n - 1 - i)))
        self._p = p
        self._P = self._GF.Zeros((self._n, self._n))
        self._P_inv = self._GF.Zeros((self._n, self._n))
        for i in range(self._n):
            self._P[i, p[i]] = 1
            self._P_inv[p[i], i] = 1
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
    def _encrypt_one(self, text):
        msg = self._pad_message(text)
        m = self._GF(msg)
        c = m.T @ self._G
        t = (self._n - self._k) // 2
        z = np.zeros(self._n, dtype = int)
        p = [i for i in range(self._n)]
        for i in range(t):
            ind = p.pop(random.randint(0, self._n - 1 - i)) 
            z[ind] = random.randint(1, self._order - 1)
        c = c + self._GF(z)
        return [int(i) for i in c]
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
            raise Exception()
        return msg
    def _pad_message(self, msg):
        last_value = self._k - (len(msg) % self._k)
        return msg + [last_value] * last_value
    def _unpad_message(self, msg):
        last_value = msg[-1]
        if last_value >= self._k or last_value <= 0:
            raise Exception()
        for i in range(1, last_value + 1):
            if msg[-i] != last_value:
                raise Exception()
        return msg[: -last_value]

if __name__ == "__main__":
    main()
