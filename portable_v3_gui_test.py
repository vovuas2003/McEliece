#G = pubkey; S and P = privkeys; text = plaintext; msg = encrypted text
#all these variables are strings
#Usage:
#G, S, P = generate()
#msg = encrypt(G, text)
#text = decrypt(S, P, msg)
#G = restore_G(S, P)
#S = break_S(G, P)
#P = break_P(G, S)

import portable_v3_core as core
import tkinter as tk

def button1_click():
    new_text1, new_text2, new_text3 = core.generate()
    entry1.delete(0, tk.END)
    entry1.insert(0, new_text1)
    entry2.delete(0, tk.END)
    entry2.insert(0, new_text2)
    entry3.delete(0, tk.END)
    entry3.insert(0, new_text3)

def button2_click():
    G = entry1.get()
    text = entry4.get("1.0", "end-1c")

    # Выполнить какие-либо действия с текстом
    new_text4 = core.encrypt(G, text)

    # Записать текст обратно в поля ввода
    entry4.delete("1.0", tk.END)
    entry4.insert("1.0", new_text4)

def button3_click():
    S = entry2.get()
    P = entry3.get()
    msg = entry4.get("1.0", "end-1c")

    # Выполнить какие-либо действия с текстом
    new_text4 = core.decrypt(S, P, msg)

    # Записать текст обратно в поля ввода
    entry4.delete("1.0", tk.END)
    entry4.insert("1.0", new_text4)

def button4_click():
    S = entry2.get()
    P = entry3.get()

    # Выполнить какие-либо действия с текстом
    new_text1 = core.restore_G(S, P)

    # Записать текст обратно в поля ввода
    entry1.delete(0, tk.END)
    entry1.insert(0, new_text1)

def button5_click():
    G = entry1.get()
    P = entry3.get()

    # Выполнить какие-либо действия с текстом
    new_text2 = core.break_S(G, P)

    # Записать текст обратно в поля ввода
    entry2.delete(0, tk.END)
    entry2.insert(0, new_text2)

def button6_click():
    G = entry1.get()
    S = entry2.get()

    # Выполнить какие-либо действия с текстом
    new_text3 = core.break_P(G, S)

    # Записать текст обратно в поля ввода
    entry3.delete(0, tk.END)
    entry3.insert(0, new_text3)

def button7_click():
    rus = entry4.get("1.0", "end-1c")

    # Выполнить какие-либо действия с текстом
    new_text4 = rus.encode('cp1251').decode('utf8')

    # Записать текст обратно в поля ввода
    entry4.delete("1.0", tk.END)
    entry4.insert("1.0", new_text4)

def action(i):
    print("Test")

window = tk.Tk()
window.title("McEliece by vovuas2003")

# Создать фрейм для кнопок
frame_buttons = tk.Frame(window)
frame_buttons.pack(side=tk.TOP, fill=tk.X)

# Создать 7 кнопок
buttons = []
but_names = ["generate keys", "encrypt text", "decrypt message", "pubkey = s + p", "s = pubkey + p", "p = pubkey + s", "fix Russian encoding"]
but_com = [button1_click, button2_click, button3_click, button4_click, button5_click, button6_click, button7_click]
for i in range(7):
    buttons.append(tk.Button(frame_buttons, text=but_names[i], command=but_com[i]))

# Разместить кнопки в одну строку
for button in buttons:
    button.pack(side=tk.LEFT)

# Создать фрейм для полей ввода текста
frame_entries = tk.Frame(window)
frame_entries.pack(side=tk.TOP, fill=tk.X)
'''
# Создать 3 поля ввода текста
entries = []
for i in range(3):
    entries.append(tk.Entry(frame_entries))

# Разместить поля ввода текста в одну строку
for entry in entries:
    entry.pack(side=tk.LEFT)

# Создать текстовое поле
text = tk.Text(window)
text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
'''
# Создать поля для ввода текста
entry1 = tk.Entry(window, width=50)
entry2 = tk.Entry(window, width=50)
entry3 = tk.Entry(window, width=50)
entry4 = tk.Text(window, height=20, width=50)

#initial text
entry1.insert(0, "pubkey")
entry2.insert(0, "privkey s")
entry3.insert(0, "privkey p")
entry4.insert("1.0", "Write a text or paste a message here!")

# Разместить элементы в окне
entry1.pack()
entry2.pack()
entry3.pack()
entry4.pack(fill=tk.BOTH, expand=True)

# Запустить главное окно
window.mainloop()
