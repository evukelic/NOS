from tkinter import *
from tkinter import font
from tkinter import messagebox

from Envelope import Envelope
from Signature import Signature
from Seal import Seal

"""
GUI.
Task method calls begin from the line 150.
"""


# create gui
root = Tk()
root.title("NOS lab2")
root.geometry("800x450")


# main window placing calculations
def calc_geometry(window):
    w = root.winfo_reqwidth()
    h = root.winfo_reqheight()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - 2*w
    y = (hs/2) - 1.5*h
    window.geometry('+%d+%d' % (x, y))


# side window placing calculations
def calc_side_geometry(window):
    w = root.winfo_reqwidth()
    h = root.winfo_reqheight()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - 0.3*w
    y = (hs/2) - 0.5*h
    window.geometry('+%d+%d' % (x, y))


calc_geometry(root)

# add the grid
frame = Frame(root)
frame.grid(column=0, row=0, sticky=(N, W, E, S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
frame.pack(padx=20, pady=20)

# title
font_style = font.Font(size=9, family="Helvetica", weight="bold")
font_style_2 = font.Font(size=12, family="Helvetica", weight="bold")
Label(frame, text="Odaberite tip zadatka i ulazne vrijednosti:", font=font_style).grid(row=1, column=0, pady=20)

# vars which will hold selected values
button_value = IntVar()
button_value.set(1)
text = StringVar()
cat1 = StringVar()
cat1_2 = StringVar()
cat1_3 = StringVar()
cat2 = StringVar()
cat2_2 = StringVar()
cat3 = StringVar()
cat3_2 = StringVar()
cat3_3 = StringVar()
cat3_4 = StringVar()

# first button/options group
Radiobutton(frame, text="Digitalna omotnica", variable=button_value, value=1).grid(row=2, column=0)
categories1 = {'AES 128', 'AES 192', 'AES 256', 'DES-3 112', 'DES-3 168'}
categories1_2 = {'ECB', 'CBC'}
categories1_3 = {'RSA 1024', 'RSA 2048', 'RSA 4096'}
cat1.set('Select')
cat1_2.set('Select')
cat1_3.set('Select')
popupMenu1 = OptionMenu(frame, cat1, *categories1).grid(row=2, column=1, pady=10)
popupMenu1_2 = OptionMenu(frame, cat1_2, *categories1_2).grid(row=2, column=2)
popupMenu1_3 = OptionMenu(frame, cat1_3, *categories1_3).grid(row=2, column=3)

# second button/options group
Radiobutton(frame, text="Digitalni potpis", variable=button_value, value=2).grid(row=3, column=0)
categories2 = {'SHA224', 'SHA256'}
categories2_2 = {'RSA 1024', 'RSA 2048', 'RSA 4096'}
cat2.set('Select')
cat2_2.set('Select')
popupMenu2 = OptionMenu(frame, cat2, *categories2).grid(row=3, column=1, pady=10)
popupMenu2_2 = OptionMenu(frame, cat2_2, *categories2_2).grid(row=3, column=2)

# third button/options group
Radiobutton(frame, text="Digitalni pečat", variable=button_value, value=3).grid(row=4, column=0)
categories3 = {'AES 128', 'AES 192', 'AES 256', 'DES-3 112', 'DES-3 168'}
categories3_2 = {'ECB', 'CBC'}
categories3_3 = {'RSA 1024', 'RSA 2048', 'RSA 4096'}
categories3_4 = {'SHA224', 'SHA256'}
cat3.set('Select')
cat3_2.set('Select')
cat3_3.set('Select')
cat3_4.set('Select')
popupMenu3 = OptionMenu(frame, cat3, *categories3).grid(row=4, column=1, pady=10)
popupMenu3_2 = OptionMenu(frame, cat3_2, *categories3_2).grid(row=4, column=2)
popupMenu3_3 = OptionMenu(frame, cat3_3, *categories3_3).grid(row=4, column=3)
popupMenu3_4 = OptionMenu(frame, cat3_4, *categories3_4).grid(row=4, column=4)

Label(root, text="Unesite tekst:", font=font_style).pack(pady=10)
entry1 = Entry(root, textvariable=text, width=50).pack(pady=10)


# on button click
def run_selected():
    new_window = Toplevel(root)
    new_window.geometry("400x270")
    calc_side_geometry(new_window)
    noError = True

    if button_value.get() == 1:
        algorithm = cat1
        mode = cat1_2
        rsa = cat1_3
    elif button_value.get() == 2:
        sha = cat2
        rsa = cat2_2
    else:
        algorithm = cat3
        mode = cat3_2
        rsa = cat3_3
        sha = cat3_4

    # check if everything is selected
    if button_value.get() == 1:
        task = 'Digitalna omotnica'
        if algorithm.get() == 'Select' or mode.get() == 'Select' or rsa.get() == 'Select':
            messagebox.showerror('Error', "Niste odabrali sve vrijednosti!")
            new_window.destroy()
            noError = False
    elif button_value.get() == 2:
        task = 'Digitalni potpis'
        if sha.get() == 'Select' or rsa.get() == 'Select':
            messagebox.showerror('Error', "Niste odabrali sve vrijednosti!")
            new_window.destroy()
            noError = False
    elif button_value.get() == 3:
        task = 'Digitalni pečat'
        if algorithm.get() == 'Select' or mode.get() == 'Select' or rsa.get() == 'Select' or sha.get() == 'Select':
            messagebox.showerror('Error', "Niste odabrali sve vrijednosti!")
            new_window.destroy()
            noError = False

    if text.get() == "" and noError:
        messagebox.showerror('Error', "Niste unijeli tekst!")
        new_window.destroy()
        noError = False

    if noError:
        Label(new_window, text=task.upper(), font=font_style_2).pack(pady=(2, 5))
        Label(new_window, text="Tekst koji ste unijeli:", font=font_style).pack(pady=(40, 5))
        Label(new_window, text=text.get()).pack()

        if button_value.get() == 1:
            Label(new_window, text="Tekst koji je dobiven dekriptiranjem:", font=font_style).pack(pady=(40, 5))
            envelope = Envelope(algorithm.get().split()[0], algorithm.get().split()[1], int(rsa.get().split()[1]), text.get(), mode.get())
            sym_obj = envelope.encrypt()
            decrypted = envelope.decrypt(sym_obj)
            Label(new_window, text=decrypted).pack()

        elif button_value.get() == 2:
            Label(new_window, text="Ishod digitalnog potpisivanja:", font=font_style).pack(pady=(40, 5))
            signature = Signature(sha.get()[3:], int(rsa.get().split()[1]), text.get())
            signature.sign()
            verification = signature.verify()
            Label(new_window, text=verification).pack()

        else:
            seal = Seal(algorithm.get().split()[0], algorithm.get().split()[1], int(rsa.get().split()[1]), text.get(), mode.get(), sha.get()[3:])
            seal.seal()
            decrypted, verification = seal.unseal()
            Label(new_window, text="Tekst koji je dobiven dekriptiranjem:", font=font_style).pack(pady=(20, 5))
            Label(new_window, text=decrypted).pack()
            Label(new_window, text="Ishod digitalnog potpisivanja:", font=font_style).pack(pady=(20, 5))
            Label(new_window, text=verification).pack()


button = Button(text="Pokreni", bg="#4a7dbd", fg="white", command=run_selected).pack(pady=30)

root.mainloop()
