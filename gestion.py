import sqlite3
from tkinter import *

# Connexion à la base de données
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    category TEXT,
    date_added DATE DEFAULT CURRENT_DATE
)
""")
conn.commit()

# Fonction pour ajouter un produit
def add_product():
    name = entry_name.get()
    desc = entry_desc.get()
    price = float(entry_price.get())
    stock = int(entry_stock.get())
    category = entry_category.get()
    
    cursor.execute("INSERT INTO Products (name, description, price, stock, category) VALUES (?, ?, ?, ?, ?)",
                   (name, desc, price, stock, category))
    conn.commit()
    label_status.config(text="Produit ajouté avec succès !")

# Interface Tkinter
root = Tk()
root.title("Gestionnaire d'Inventaire")

Label(root, text="Nom du produit").grid(row=0, column=0)
entry_name = Entry(root)
entry_name.grid(row=0, column=1)

Label(root, text="Description").grid(row=1, column=0)
entry_desc = Entry(root)
entry_desc.grid(row=1, column=1)

Label(root, text="Prix").grid(row=2, column=0)
entry_price = Entry(root)
entry_price.grid(row=2, column=1)

Label(root, text="Stock").grid(row=3, column=0)
entry_stock = Entry(root)
entry_stock.grid(row=3, column=1)

Label(root, text="Catégorie").grid(row=4, column=0)
entry_category = Entry(root)
entry_category.grid(row=4, column=1)

Button(root, text="Ajouter", command=add_product).grid(row=5, column=0, columnspan=2)
label_status = Label(root, text="")
label_status.grid(row=6, column=0, columnspan=2)

root.mainloop()
