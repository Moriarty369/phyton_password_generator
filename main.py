from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip


# ------------------------------------------GENERADOR DE CONTRASEÑA---------------------------------------------------
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    # Eliminimas cualquier password que haya sido insertado en la GUI anteriormente (regenerar contraseña)
    password_entry.delete(0, 'end')
    # Insertamos el paswword generado en la GUI
    password_entry.insert(0, password)
    # Copiamos automaticamente el paswword en el "paperclip" para pegar facilmente en otras ventanas
    pyperclip.copy(password)


# Guardar contraseña
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    is_ok = messagebox.askokcancel(title=website, message=f"Estos son los datos introducidos: \nSitio web: {website} \nUsuario o correo: {email} \nPassword: {password} \n¿Desea salvar los datos?")

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Algo ha ido mal, asegurate de no haber dejado ninguna casilla vacía")

    else:
        if is_ok:
            # abrimos un archivo usando append mode (si no existe, es creado), con el with evitamos tener que cerrar
            # el archivo con archivo.close()
            with open("data.txt", "a")  as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
# Ojo-- falta por hacer responsive los 3 inputs
def on_window_resize(event):
    # Actualizar el tamaño de las columnas y filas para que se ajusten al nuevo tamaño de la ventana
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_rowconfigure(5, weight=1)


window = Tk()
window.title("Gestor de contraseñas")
window.config(padx=50, pady=20)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, columnspan=2, pady=(0, 20))

# Labels
website_label = Label(text="Sitio Web:")
website_label.grid(row=1, column=0, sticky="e")
email_label = Label(text="Correo/Usuario:")
email_label.grid(row=2, column=0, sticky="e")
password_label = Label(text="Contraseña:")
password_label.grid(row=3, column=0, sticky="e")

# Inputs
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2, sticky="w")
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
email_entry.insert(0, "debe_colocar_email")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="w")

# Botones
gen_cont_button = Button(text="Generar contraseña", command=generate_password)
gen_cont_button.grid(row=3, column=2, sticky="w")
add_button = Button(text="Añadir", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, pady=20)

window.bind("<Configure>", on_window_resize)
window.mainloop()
