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
        print("\nUnknown error (maybe ctrl+c), emergency exit!")

def menu():
    info = "Menu numbers: h = info, t = test clipboard, c = config;\n0 = exit, 1 = generate, 2 = encrypt, 3 = decrypt\n"
    err = "Error, try again!\n"
    ok = "Operation successful.\n"
    inp = ['h', 'c', 't'] + [str(i) for i in range (4)] + ['1337']
    core = McEliece_core()
    print("\nMcEliece password encryption by vovuas2003.\n")
    print(info)
    while True:
        s = input("Menu number: ")
        while s not in inp:
            s = input("Wrong menu number; h = help: ")
        if s == '0':
            print("\nGood luck!")
            break
        elif s == 'h':
            print(info)
        elif s == 't':
            print("Do you want to check Python ability to use clipboard in your OS?")
            if(not get_yes_no()):
                continue
            try:
                print('Trying to write "Hello, world!" to clipboard.')
                mycopy("Hello, world!")
                print("Success! You can check ctrl+v.")
            except:
                print("Python cannot use clipboard. On Linux maybe you need to run command: sudo apt-get install xclip.\nOr try code below to check python error log:\nimport pyperclip #don't forget to pip install pyperclip\npyperclip.copy(\"Hello, world!\")")
        elif s == 'c':
            n, k = core.get_config()
            print("Default config is 255 210, current is " + str(n) + " " + str(k) + ". Change config? Also reset all keys!")
            if(not get_yes_no()):
                continue
            try:
                print("Config is two numbers n >= k >= 2; (3 * 5 * 17) mod n = 0. Larger values = larger keys.\nRandomly change (n - k) div 2 bytes during encryption, but add (n - k + 1) bytes to each chunk with len (k - 1).")
                n, k = map(int, input("Write n and k separated by a space: ").split())
                core.change_config(n, k)
                print(ok)
            except:
                print(err)
        elif s == '1':
            print("Reset all keys!")
            if(not get_yes_no()):
                continue
            try:
                core.generate_keys(normalhash(getpass.getpass("Password for hash: ")))
                print(ok)
            except:
                print(err)
        elif s == '2':
            print("Encrypt hided input (ONLY ONE LINE!!!) from clipboard!")
            if(not get_yes_no()):
                continue
            try:
                inp_str = getpass.getpass("Hided string to encrypt: ")
                out_name = input("Filename to save: ")
                if not out_name:
                    print("Using default name ciphered_string.bin")
                    out_name = "ciphered_string.bin"
                write_file(out_name, bytes(core.encrypt([int(i) for i in inp_str.encode('utf-8')])))
                print(ok)
            except:
                print(err)
        elif s == '3':
            print("Decrypt string from file and copy to clipboard!")
            if(not get_yes_no()):
                continue
            try:
                inp_name = input("Filename to decrypt: ")
                if not inp_name:
                    print("Using default name ciphered_string.bin")
                    inp_name = "ciphered_string.bin"
                mycopy(bytes(core.decrypt([int(i) for i in read_file(inp_name)])).decode('utf-8'))
                print(ok)
            except:
                print(err)
        elif s == '1337':
            mycopy(PT())
        else:
            print("Impossible behaviour, mistake in source code, emergency exit!\nThe string allowed in the inp array is not bound to the call of any function!")
            break

class McEliece_core:
    def __init__(self):
        self._order = 256
        self._n = 255
        self._k = 210
        self._t = (self._n - self._k) // 2
        self._GF = galois.GF(2, 8, irreducible_poly = "x^8 + x^4 + x^3 + x^2 + 1", primitive_element = "x", verify = False)
        self._rs = galois.ReedSolomon(self._n, self._k, field = self._GF)
        self._G = self._GF.Zeros((self._k, self._n))
        self._S = self._GF.Zeros((self._k, self._k))
        self._S_inv = self._GF.Zeros((self._k, self._k))
        self._P = self._GF.Zeros((self._n, self._n))
        self._P_inv = self._GF.Zeros((self._n, self._n))
        self._p = [0 for i in range(self._n)]
    def change_config(self, n, k):
        try:
            if k < 2:
                raise Exception()
            rs = galois.ReedSolomon(n, k, field = self._GF)
        except:
            raise
        else:
            self._n = n
            self._k = k
            self._t = (n - k) // 2
            self._rs = rs
            self._G = self._GF.Zeros((self._k, self._n))
            self._S = self._GF.Zeros((self._k, self._k))
            self._S_inv = self._GF.Zeros((self._k, self._k))
            self._P = self._GF.Zeros((self._n, self._n))
            self._P_inv = self._GF.Zeros((self._n, self._n))
            self._p = [0 for i in range(self._n)]
    def get_config(self):
        return self._n, self._k
    def generate_keys(self, seed):
        seed %= 2**32
        self._unsafe_generate_S(seed)
        self._unsafe_generate_P(seed)
        self._G = self._S @ self._rs.G @ self._P
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
            raise
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
    def _encrypt_one(self, text):
        msg = self._pad_message(text)
        m = self._GF(msg)
        c = m.T @ self._G
        z = np.zeros(self._n, dtype = int)
        p = [i for i in range(self._n)]
        for i in range(self._t):
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
            raise
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

def write_file(name, data):
    with open(name, "wb") as f:
        f.write(data)

def read_file(name):
    with open(name, "rb") as f:
        data = f.read()
    return data

def get_yes_no():
    s = input("Confirm (0 = go back, 1 = continue): ")
    while s not in ['0', '1']:
        s = input("Try again, 0 or 1: ")
    return int(s)

def normalhash(s):
    return int(hashlib.sha256(bytearray(s, 'utf-8')).hexdigest(), 16)

def PT(m = -3, M = 3):
    if m == 0 or abs(m) > M:
        return "PT!"
    s = "PT!"
    p = "   "
    f = False
    if m < 0:
        s, p = p, s
        m *= -1
        f = True
    out = "\n"
    if f:
        out += p * (10 * m + 1) + "\n"
    out += p + (s * 3 + p + s * 3 + p + s + p) * m + "\n"
    out += p + (s + p + s + p * 2 + s + p * 2 + s + p) * m + "\n"
    out += p + (s * 3 + p * 2 + s + p * 2 + s + p) * m + "\n"
    out += p + (s + p * 4 + s + p * 4) * m + "\n"
    out += p + (s + p * 4 + s + p * 2 + s + p) * m + "\n"
    if f:
        out += p * (10 * m + 1) + "\n"
    out += "\n"
    return out

def mycopy(s):
    pyperclip.copy(s)

if __name__ == "__main__":
    main()
