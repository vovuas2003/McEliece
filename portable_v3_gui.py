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

# Создать главное окно
window = tk.Tk()
window.title("McEliece by vovuas2003")

# Создать поля для ввода текста
entry1 = tk.Entry(window, width=50)
entry2 = tk.Entry(window, width=50)
entry3 = tk.Entry(window, width=50)
entry4 = tk.Text(window, height=10, width=50)

# Создать кнопки
button1 = tk.Button(window, text="generate", command=button1_click)
button2 = tk.Button(window, text="encrypt", command=button2_click)
button3 = tk.Button(window, text="decrypt", command=button3_click)
button4 = tk.Button(window, text="pubkey", command=button4_click)
button5 = tk.Button(window, text="privkey_s", command=button5_click)
button6 = tk.Button(window, text="privkey_p", command=button6_click)

# Разместить элементы в окне
entry1.pack()
entry2.pack()
entry3.pack()
entry4.pack(fill=tk.BOTH, expand=True)
button1.pack()
button2.pack()
button3.pack()
button4.pack()
button5.pack()
button6.pack()

# Запустить главное окно
window.mainloop()
