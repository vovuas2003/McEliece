#pyinstaller -F -i "icon.ico" McEliece_GUI.py

#Thanks for AI, I don't know tkinter lib

import cryptosystem_core as core
import tkinter as tk
from tkinter.messagebox import showerror, showwarning, showinfo

def show_error():
    showerror("Error!", "Press help button to show common mistakes in usage.")

def button0_click():
    showinfo("Source code: github.com/vovuas2003/McEliece", "1st line = current configuration of cryptosystem.\n2nd line = public key (send to anybody).\n3rd line = first half (s) of private key (keep in secret!).\n4th line = second half (p) of private key (keep in secret!).\nBig field = place for writing text or pasting message.\nGenerate keys = rewrite all 3 keys.\nEncrypt = pubkey is required.\nDecrypt = both privkeys are required.\nYou can restore any key from the other two.\nConfig = change cryptosystem parameters n and k.\n(two numbers separated by a space, default: 255 210).\n(255 mod n = 0; 255 = 3*5*17)\n(2 <= k <= n; (n - k) div 2 bytes are randomly changed)\n\nPT! = just easter egg :)")

def button1_click():
    try:
        new_text1, new_text2, new_text3 = core.generate()
        entry1.delete(0, tk.END)
        entry1.insert(0, new_text1)
        entry2.delete(0, tk.END)
        entry2.insert(0, new_text2)
        entry3.delete(0, tk.END)
        entry3.insert(0, new_text3)
    except:
        show_error()

def button2_click():
    try:
        G = entry1.get()
        text = entry4.get("1.0", "end-1c")
        new_text4 = core.encrypt(G, text)
        entry4.delete("1.0", tk.END)
        entry4.insert("1.0", new_text4)
    except:
        show_error()

def button3_click():
    try:
        S = entry2.get()
        P = entry3.get()
        msg = entry4.get("1.0", "end-1c")
        new_text4 = core.decrypt(S, P, msg)
        entry4.delete("1.0", tk.END)
        entry4.insert("1.0", new_text4)
    except:
        show_error()

def button4_click():
    try:
        S = entry2.get()
        P = entry3.get()
        new_text1 = core.restore_G(S, P)
        entry1.delete(0, tk.END)
        entry1.insert(0, new_text1)
    except:
        show_error()

def button5_click():
    try:
        G = entry1.get()
        P = entry3.get()
        new_text2 = core.break_S(G, P)
        entry2.delete(0, tk.END)
        entry2.insert(0, new_text2)
    except:
        show_error()

def button6_click():
    try:
        G = entry1.get()
        S = entry2.get()
        new_text3 = core.break_P(G, S)
        entry3.delete(0, tk.END)
        entry3.insert(0, new_text3)
    except:
        show_error()

def button7_click():
    try:
        core.config(entry0.get())
    except:
        entry0.delete(0, tk.END)
        entry0.insert(0, str(core.n) + " " + str(core.k))
        show_error()

def button8_click():
    showwarning("PT!", "PT!" * 10)

window = tk.Tk()
window.title("McEliece by vovuas2003")

frame_buttons = tk.Frame(window)
frame_buttons.pack(side = tk.TOP, fill = tk.X)

buttons = []
but_names = ["help", "generate keys", "encrypt text", "decrypt message", "pubkey = s + p", "s = pubkey + p", "p = pubkey + s", "change config", "PT!"]
but_com = [button0_click, button1_click, button2_click, button3_click, button4_click, button5_click, button6_click, button7_click, button8_click]
for i in range(9):
    buttons.append(tk.Button(frame_buttons, text = but_names[i], command = but_com[i]))

for button in buttons:
    button.pack(side = tk.LEFT)

entry0 = tk.Entry(window, width = 50)
entry1 = tk.Entry(window, width = 50)
entry2 = tk.Entry(window, width = 50)
entry3 = tk.Entry(window, width = 50)
entry4 = tk.Text(window, height = 20, width = 50)

entry0.insert(0, "255 210 (default config)")
entry1.insert(0, "pubkey")
entry2.insert(0, "privkey s")
entry3.insert(0, "privkey p")
entry4.insert("1.0", "Write a text or paste a message here!\nAll utf-8 symbols are supported, e.g. alt codes and Russian text.\n\n(use ctrl+a before crtl+v or ctrl+c)\n(switch keyboard layout to english to use these shortcuts)\n\nYou can't resize window, but can scroll down.\nProgram can work slow, don't kill it please :)")

entry0.pack()
entry1.pack()
entry2.pack()
entry3.pack()
entry4.pack(fill = tk.BOTH, expand = True)

window.resizable(False, False)
window.mainloop()
