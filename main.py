from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ------------------------------------------GENERADOR DE CONTRASEÑA---------------------------------------------------
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
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


def search():
    website = website_entry.get()

    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Por favor, ingresa el nombre del sitio web para buscar.")
    else:
        # Creamos toda la lógica dentro del try para evitar crear otro else asociado al mismo a partir del if
        try:
            with open("data.json", "r") as data_file:
                # Leemos datos
                data = json.load(data_file)
                if website in data:
                    email = data[website]["correo"]
                    password = data[website]["contraseña"]
                    messagebox.showinfo(title=website, message=f"Correo/Usuario: {email}\nContraseña: {password}")
                else:
                    messagebox.showinfo(title=website, message="No se encontraron datos para este sitio web.")
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No se encontró el archivo de datos.")


# Guardar contraseña
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "correo": email,
            "contraseña": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Algo ha ido mal, asegurate de no haber dejado ninguna casilla vacía")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Leemos datos
                data = json.load(data_file)
        # Si los datos no existen, creamos el json
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        # En caso de que ya existan datos los actualizamos
        else:
            data.update(new_data)
            # Salvamos los datos actualizados
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
def on_window_resize(event):
    window_width = event.width
    window_height = event.height

    # Centrar el canvas con el logo
    canvas = Canvas(window, height=200, width=200)
    logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)

    # Centrar las etiquetas y las entradas de texto
    website_label.grid(row=1, column=0, sticky="e")
    email_label.grid(row=2, column=0, sticky="e")
    password_label.grid(row=3, column=0, sticky="e")

    website_entry.grid(row=1, column=1, columnspan=2, sticky="w")
    email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
    password_entry.grid(row=3, column=1, sticky="w")

    # Centrar el botón "Generar contraseña"
    gen_pass_button.grid(row=3, column=2, sticky="w")

    # Centrar el marco de botones
    button_frame.grid(row=4, column=0, columnspan=3, pady=(20, 0))
    button_frame.update_idletasks()

    # Actualizar el tamaño de las columnas y filas para que se ajusten al nuevo tamaño de la ventana
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(3, weight=1)
    window.grid_rowconfigure(5, weight=1)






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
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "Ingrese su correo/usuario")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Botones
search_button = Button(text="Buscar", width=13, command=search)
search_button.grid(row=1, column=2, sticky="w")
gen_pass_button = Button(text="Generar contraseña", command=generate_password)
gen_pass_button.grid(row=3, column=2, sticky="w")
add_button = Button(text="Añadir", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, pady=20)

# Marco de botones (responsive)
button_frame = Frame(window)
button_frame.grid(row=5, column=0, columnspan=3, pady=20)


window.bind("<Configure>", on_window_resize)
window.mainloop()
