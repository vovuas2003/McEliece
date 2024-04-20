#THE PROGRAM ISN'T FINISHED!

#pyinstaller -F -i "icon.ico" McEliece_console.py

import cryptosystem_core as core

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
    print("\nMcEliece cryptosystem implementation by vovuas2003.\n")
    print("All necessary txt files must be located in the directory with this exe program.\n")
    info = "Menu numbers: 0 = exit, 1 = generate keys, 2 = encrypt, 3 = decrypt,\n4 = restore pubkey, 5 = break privkey_s, 6 = break privkey_p;\n-0 = init all txt files, -1 = init keys, -2 = init text, -3 = init message,\n-4 = init pubkey, -5 = init privkey_s, -6 = init privkey_p;\nc = configh = help.\n"
    err = "Error! Check command info and try again!\n"
    ok = "Operation successful.\n"
    inp = [str(i) for i in range(7)] + ['-' + str(i) for i in range(7)] + ['c', 'h'] + ['1337']
    print(info)
    while True:
        s = input("Menu number: ")
        while s not in inp:
            s = input("Wrong menu number, h = help: ")
        if s == 'h':
            print(info)
        elif s == '0':
            print("\nGood luck!")
            break
        elif s == '1':
            print("This operation will rewrite pubkey.txt, privkey_s.txt and privkey_p.txt; are you sure?")
            if(not get_yes_no()):
                continue
            try:
                G, S, P = core.generate()
                with open("pubkey.txt", "w", encoding = "utf-8") as pub, open("privkey_s.txt", "w", encoding = "utf-8") as privs, open("privkey_p.txt", "w", encoding = "utf-8") as privp:
                    pub.write(G)
                    privs.write(S)
                    privp.write(P)
                print(ok)
            except:
                print(err)
        elif s == '2':
            print("Write your text into text.txt; pubkey.txt is required, message.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                encrypt(n, k, order, GF)
                print(ok)
            except:
                print(err)
        elif s == '3':
            print("You need message.txt, privkey_s.txt and privkey_p.txt; text.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                decrypt(n, k, GF, rs)
                print(ok)
            except:
                print(err)
        elif s == '4':
            print("You need privkey_s.txt and privkey_p.txt; pubkey.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                restore_G_(n, k, GF, rs)
                print(ok)
            except:
                print(err)
        elif s == '5':
            print("You need pubkey.txt and privkey_p.txt; privkey_s.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                break_S(n, k, GF)
                print(ok)
            except:
                print(err)
        elif s == '6':
            print("You need pubkey.txt and privkey_s.txt; privkey_p.txt will be rewritten.")
            if(not get_yes_no()):
                continue
            try:
                break_P(n, k, GF, rs)
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

if __name__ == "__main__":
    main()
