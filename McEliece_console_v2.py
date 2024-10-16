#pyinstaller -F -i "icon.ico" McEliece_console_v2.py

import hashlib
import getpass

def main():
    safe_start()

def safe_start():
    try:
        start_menu()
    except:
        print("\nUnknown error (maybe ctrl+c), emergency exit!")

def start_menu():
    f = True
    print("\nWhat is the author's nickname?")
    #vovuas 2003
    if myhash(getpass.getpass("Letters: ")) != 132782522349988:
        f = False
    if myhash(getpass.getpass("Digits: ")) != 851912389:
        f = False
    if f:
        print("Authorization successful, wait a bit.")
        menu()
    else:
        print("Permission denied.")
    print("\nPress ENTER to exit.", end = '')
    input()

def menu():
    import cryptosystem_core_v2 as ME_core
    core = ME_core.McEliece_core()
    global_info = "All files are interpreted as raw bytes and must be located in the directory with this executable file.\nDefault filenames with .bin extension: pubkey, privkey_S, privkey_p, plaintext, ciphertext, ciphered_string.\nDon't forget to import (or generate) keys before encryption/decryption and after changing config!\nYou can restore any one key from two another (don't forget to import before).\n"
    info = "Menu numbers: 0 = exit, s = print short info, h = print this info, g = print global info, c = change config;\n1 = generate keys, 10 = unsafe generate keys (seed = hash(password)),\n11 = export pubkey, 12 = export privkey_S, 13 = export privkey_p,\n14 = import pubkey, 15 = import privkey_S, 16 = import privkey_p,\n17 = restore pubkey, 18 = restore privkey_S, 19 = restore privkey_p;\n2 = encrypt,\n21 = encrypt non-default filename, 22 = encrypt string from keyboard, 23 = encrypt hided string.\n3 = decrypt,\n31 = decrypt non-default filename, 32 = decrypt string and show on screen\n"
    short_info = "0 = exit, s/h/g = print short/extended/global info, c = change config;\n1 = generate keys, 2 = encrypt, 3 = decrypt\n"
    err = "Error! Check global info (menu number g) and try again!\n"
    ok = "Operation successful.\n"
    inp = ['0', 's', 'h', 'g', 'c'] + [str(i) for i in range(1, 4)] + [str(i) for i in range(10, 20)] + [str(i) for i in range(21, 24)] + [str(i) for i in range(31, 33)] + ['1337']
    print("\nMcEliece cryptosystem implementation by vovuas2003. Version 2.\n")
    print(global_info)
    print(info)
    while True:
        s = input("Menu number: ")
        while s not in inp:
            s = input("Wrong menu number; h = help, s = short help: ")
        if s == '0':
            print("\nGood luck!")
            break
        elif s == 's':
            print(short_info)
        elif s == 'h':
            print(info)
        elif s == 'g':
            print(global_info)
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
                core.generate_keys()
                print(ok)
            except:
                print(err)
        elif s == '10':
            print("It is better to use menu number 1 for true random!")
            if(not get_yes_no()):
                continue
            try:
                core.generate_keys(normalhash(getpass.getpass("Password for hash: ")))
                print(ok)
            except:
                print(err)
        elif s == '11':
            print("Rewrite pubkey.bin!")
            if(not get_yes_no()):
                continue
            try:
                write_file("pubkey.bin", bytes(core.get_pubkey()))
                print(ok)
            except:
                print(err)
        elif s == '12':
            print("Rewrite privkey_S.bin!")
            if(not get_yes_no()):
                continue
            try:
                write_file("privkey_S.bin", bytes(core.get_privkey_S()))
                print(ok)
            except:
                print(err)
        elif s == '13':
            print("Rewrite privkey_p.bin!")
            if(not get_yes_no()):
                continue
            try:
                write_file("privkey_p.bin", bytes(core.get_privkey_p()))
                print(ok)
            except:
                print(err)
        elif s == '14':
            print("Load pubkey.bin into cryptosystem.")
            if(not get_yes_no()):
                continue
            try:
                core.set_pubkey([int(i) for i in read_file("pubkey.bin")])
                print(ok)
            except:
                print(err)
        elif s == '15':
            print("Load privkey_S.bin into cryptosystem.")
            if(not get_yes_no()):
                continue
            try:
                core.set_privkey_S([int(i) for i in read_file("privkey_S.bin")])
                print(ok)
            except:
                print(err)
        elif s == '16':
            print("Load privkey_p.bin into cryptosystem.")
            if(not get_yes_no()):
                continue
            try:
                core.set_privkey_p([int(i) for i in read_file("privkey_p.bin")])
                print(ok)
            except:
                print(err)
        elif s == '17':
            print("Rewrite pubkey inside cryptosystem.")
            if(not get_yes_no()):
                continue
            try:
                core.restore_pubkey()
                print(ok)
            except:
                print(err)
        elif s == '18':
            print("Rewrite privkey_S inside cryptosystem.")
            if(not get_yes_no()):
                continue
            try:
                core.restore_privkey_S()
                print(ok)
            except:
                print(err)
        elif s == '19':
            print("Rewrite privkey_p inside cryptosystem.")
            if(not get_yes_no()):
                continue
            try:
                core.restore_privkey_p()
                print(ok)
            except:
                print(err)
        elif s == '2':
            print("Need plaintext.bin, rewrite ciphertext.bin!")
            if(not get_yes_no()):
                continue
            try:
                write_file("ciphertext.bin", bytes(core.encrypt([int(i) for i in read_file("plaintext.bin")])))
                print(ok)
            except:
                print(err)
        elif s == '21':
            print("Type names with extensions!")
            if(not get_yes_no()):
                continue
            try:
                inp_name = input("File to encrypt: ")
                out_name = input("Name for save: ")
                write_file(out_name, bytes(core.encrypt([int(i) for i in read_file(inp_name)])))
                print(ok)
            except:
                print(err)
        elif s == '22':
            print("Rewrite ciphered_string.bin!")
            if(not get_yes_no()):
                continue
            try:
                inp_str = input("String to encrypt: ")
                write_file("ciphered_string.bin", bytes(core.encrypt([int(i) for i in inp_str.encode('utf-8')])))
                print(ok)
            except:
                print(err)
        elif s == '23':
            print("Rewrite ciphered_string.bin!")
            if(not get_yes_no()):
                continue
            try:
                inp_str = getpass.getpass("Hided string to encrypt: ")
                write_file("ciphered_string.bin", bytes(core.encrypt([int(i) for i in inp_str.encode('utf-8')])))
                print(ok)
            except:
                print(err)
        elif s == '3':
            print("Need ciphertext.bin, rewrite plaintext.bin!")
            if(not get_yes_no()):
                continue
            try:
                write_file("plaintext.bin", bytes(core.decrypt([int(i) for i in read_file("ciphertext.bin")])))
                print(ok)
            except:
                print(err)
        elif s == '31':
            print("Type names with extensions!")
            if(not get_yes_no()):
                continue
            try:
                inp_name = input("File to decrypt: ")
                out_name = input("Name for save: ")
                write_file(out_name, bytes(core.decrypt([int(i) for i in read_file(inp_name)])))
                print(ok)
            except:
                print(err)
        elif s == '32':
            print("Need ciphered_string.bin!")
            if(not get_yes_no()):
                continue
            try:
                print("Deciphered string: " + bytes(core.decrypt([int(i) for i in read_file("ciphered_string.bin")])).decode('utf-8'))
                print(ok)
            except:
                print(err)
        elif s == '1337':
            PT()
        else:
            print("Impossible behaviour, mistake in source code, emergency exit!\nThe string allowed in the inp array is not bound to the call of any function!")
            break

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

def myhash(s, m = 2**61 - 1, p = 257):
    a = 0
    for i in range(len(s)):
    	a = ((a * p) % m + ord(s[i])) % m
    return a

def normalhash(s):
    return int(hashlib.sha256(bytearray(s, 'utf-8')).hexdigest(), 16)

def PT(m = -3, M = 3):
    if m == 0 or abs(m) > M:
        print("PT!")
        return
    s = "PT!"
    p = "   "
    f = False
    if m < 0:
        s, p = p, s
        m *= -1
        f = True
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

if __name__ == "__main__":
    main()
