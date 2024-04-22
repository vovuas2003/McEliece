#pyinstaller -F -i "icon.ico" McEliece_console.py

import getpass
import random

def main():
    safe_start()

def safe_start():
    try:
        start_menu()
    except:
        print("\nUnknown error (maybe ctrl+c), emergency exit!")

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
    import cryptosystem_core as core
    print("\nMcEliece cryptosystem implementation by vovuas2003.\n")
    print("All necessary txt files must be in utf-8 and located in the directory with this exe program.\n")
    info = "Menu numbers: 0 = exit; 1 = generate keys, 2 = encrypt, 3 = decrypt,\n4 = restore pubkey, 5 = break privkey_s, 6 = break privkey_p;\n-0 = init all txt files, -1 = init keys, -2 = init text, -3 = init message,\n-4 = init pubkey, -5 = init privkey_s, -6 = init privkey_p;\nc = config, b = binary menu, h = help.\n"
    err = "Error! Check command info and try again!\n"
    ok = "Operation successful.\n"
    inp = [str(i) for i in range(7)] + ['-' + str(i) for i in range(7)] + ['c', 'b', 'h'] + ['1337']
    print(info)
    while True:
        s = input("Menu number: ")
        while s not in inp:
            s = input("Wrong menu number, h = help: ")
        if s == 'h':
            print(info)
        elif s == 'b':
            print("Go to binary files encryption menu?")
            if(not get_yes_no()):
                continue
            try:
                if(bin_menu()):
                    break
            except:
                raise Exception()
        elif s == 'c':
            print("Default config is 255 210, current is " + str(core.n) + " " + str(core.k) + ". Change config?")
            if(not get_yes_no()):
                continue
            try:
                print("Config is two numbers n >= k >= 2; (3 * 5 * 17) mod n = 0.")
                core.config(input("Write n and k separated by a space: "))
                print(ok)
            except:
                print(err)
        elif s == '0':
            print("\nGood luck!")
            break
        elif s == '1':
            print("This operation will rewrite pubkey.txt, privkey_s.txt and privkey_p.txt; are you sure?")
            if(not get_yes_no()):
                continue
            try:
                G, S, P = core.generate()
                write_txt("pubkey", G)
                write_txt("privkey_s", S)
                write_txt("privkey_p", P)
                print(ok)
            except:
                print(err)
        elif s == '2':
            print("Write your text into text.txt; pubkey.txt is required, message.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                G = read_txt("pubkey")
                text = read_txt("text")
                msg = core.encrypt(G, text)
                write_txt("message", msg)
                print(ok)
            except:
                print(err)
        elif s == '3':
            print("You need message.txt, privkey_s.txt and privkey_p.txt; text.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                S = read_txt("privkey_s")
                P = read_txt("privkey_p")
                msg = read_txt("message")
                text = core.decrypt(S, P, msg)
                write_txt("text", text)
                print(ok)
            except:
                print(err)
        elif s == '4':
            print("You need privkey_s.txt and privkey_p.txt; pubkey.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                S = read_txt("privkey_s")
                P = read_txt("privkey_p")
                G = core.restore_G(S, P)
                write_txt("pubkey", G)
                print(ok)
            except:
                print(err)
        elif s == '5':
            print("You need pubkey.txt and privkey_p.txt; privkey_s.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                G = read_txt("pubkey")
                P = read_txt("privkey_p")
                S = core.break_S(G, P)
                write_txt("privkey_s", S)
                print(ok)
            except:
                print(err)
        elif s == '6':
            print("You need pubkey.txt and privkey_s.txt; privkey_p.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                G = read_txt("pubkey")
                S = read_txt("privkey_s")
                P = core.break_P(G, S)
                write_txt("privkey_p", P)
                print(ok)
            except:
                print(err)
        elif s == '-0':
            print("Create (or make empty) all 5 necessary txt files in right utf-8 encoding.")
            if(not get_yes_no()):
                continue
            try:
                write_txt("pubkey", "")
                write_txt("privkey_s", "")
                write_txt("privkey_p", "")
                write_txt("text", "")
                write_txt("message", "")
                print(ok)
            except:
                print(err)
        elif s == '-1':
            print("Create (or make empty) all 3 keys txt files in right utf-8 encoding.")
            if(not get_yes_no()):
                continue
            try:
                write_txt("pubkey", "")
                write_txt("privkey_s", "")
                write_txt("privkey_p", "")
                print(ok)
            except:
                print(err)
        elif s == '-2':
            print("Create (or make empty) text.txt in right utf-8 encoding.")
            if(not get_yes_no()):
                continue
            try:
                write_txt("text", "")
                print(ok)
            except:
                print(err)
        elif s == '-3':
            print("Create (or make empty) message.txt in right utf-8 encoding.")
            if(not get_yes_no()):
                continue
            try:
                write_txt("message", "")
                print(ok)
            except:
                print(err)
        elif s == '-4':
            print("Create (or make empty) pubkey.txt in right utf-8 encoding.")
            if(not get_yes_no()):
                continue
            try:
                write_txt("pubkey", "")
                print(ok)
            except:
                print(err)
        elif s == '-5':
            print("Create (or make empty) privkey_s.txt in right utf-8 encoding.")
            if(not get_yes_no()):
                continue
            try:
                write_txt("privkey_s", "")
                print(ok)
            except:
                print(err)
        elif s == '-6':
            print("Create (or make empty) privkey_p.txt in right utf-8 encoding.")
            if(not get_yes_no()):
                continue
            try:
                write_txt("privkey_p", "")
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

def bin_menu():
    import cryptosystem_core as core
    print("\nName of encrypted and based64 binary file is binary.txt, first line in it is a name of the original file.")
    info = "Binary menu numbers: 0 = go back to common menu; 1 = encrypt, 2 = decrypt; h = help.\n"
    err = "Error! Check command info and try again!\n"
    ok = "Operation successful.\n"
    inp = [str(i) for i in range(3)] + ['h']
    print(info)
    while True:
        s = input("Binary menu number: ")
        while s not in inp:
            s = input("Wrong menu number, h = help: ")
        if s == 'h':
            print(info)
        elif s == '0':
            print("Go back to common menu.\n")
            break
        elif s == '1':
            print("You need pubkey.txt and any file that you want to encrypt; binary.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                G = read_txt("pubkey")
                name = input("Write name of file with extension: ")
                with open(name, "rb") as f:
                    b = f.read()
                out = core.bin_encrypt(G, b)
                with open("binary.txt", "w") as f:
                    f.write(name + '\n')
                    f.write(out)
                print(ok)
            except:
                print(err)
        elif s == '2':
            print("You need privkey_s.txt, privkey_p.txt and binary.txt.")
            if(not get_yes_no()):
                continue
            try:
                S = read_txt("privkey_s")
                P = read_txt("privkey_p")
                with open("binary.txt", "r") as f:
                    name = f.readline()[: -1]
                    msg = f.readline()
                text = core.bin_decrypt(S, P, msg)
                with open(name, "wb") as f:
                    f.write(text)
                print(ok)
            except:
                print(err)
        else:
            print("Impossible behaviour, mistake in source code!\nThe string allowed in the inp array is not bound to the call of any function!")
            return 1
    return 0

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

def PT(m, M = 3):
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

def write_txt(name, string):
    with open(name + ".txt", "w", encoding = "utf-8") as f:
        f.write(string)

def read_txt(name):
    with open(name + ".txt", "r", encoding = "utf-8") as f:
        out = f.read()
    return out

if __name__ == "__main__":
    main()
