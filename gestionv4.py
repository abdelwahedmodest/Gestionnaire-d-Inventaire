import sqlite3
from tkinter import *
from tkinter.ttk import Treeview

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
    show_products()  # Actualiser la liste des produits affichés

# Fonction pour afficher les produits dans le Treeview
def show_products():
    for row in tree.get_children():
        tree.delete(row)  # Supprimer les anciennes lignes
    
    cursor.execute("SELECT * FROM Products")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)  # Ajouter les produits au Treeview

# Interface Tkinter
root = Tk()
root.title("Gestionnaire d'Inventaire")

# Canvas pour structurer l'interface
canvas = Canvas(root, width=600, height=500, bg="#f0f0f0")
canvas.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

# Ajout d'un titre au Canvas
canvas.create_text(300, 20, text="Gestionnaire d'Inventaire", font=("Arial", 18, "bold"), fill="blue")

# Création de la section pour l'ajout des produits
frame_input = Frame(root)
frame_input.grid(row=1, column=0, padx=20, pady=10)

Label(frame_input, text="Nom du produit").grid(row=0, column=0)
entry_name = Entry(frame_input)
entry_name.grid(row=0, column=1)

Label(frame_input, text="Description").grid(row=1, column=0)
entry_desc = Entry(frame_input)
entry_desc.grid(row=1, column=1)

Label(frame_input, text="Prix").grid(row=2, column=0)
entry_price = Entry(frame_input)
entry_price.grid(row=2, column=1)

Label(frame_input, text="Stock").grid(row=3, column=0)
entry_stock = Entry(frame_input)
entry_stock.grid(row=3, column=1)

Label(frame_input, text="Catégorie").grid(row=4, column=0)
entry_category = Entry(frame_input)
entry_category.grid(row=4, column=1)

Button(frame_input, text="Ajouter", command=add_product).grid(row=5, column=0, columnspan=2)

label_status = Label(frame_input, text="")
label_status.grid(row=6, column=0, columnspan=2)

# Création du Treeview pour afficher les produits
frame_tree = Frame(root)
frame_tree.grid(row=2, column=0, padx=20, pady=10)

tree = Treeview(frame_tree, columns=("ID", "Nom", "Description", "Prix", "Stock", "Catégorie"), show="headings")
tree.grid(row=0, column=0)

tree.heading("ID", text="ID")
tree.heading("Nom", text="Nom")
tree.heading("Description", text="Description")
tree.heading("Prix", text="Prix")
tree.heading("Stock", text="Stock")
tree.heading("Catégorie", text="Catégorie")

# Afficher les produits existants
show_products()

root.mainloop()
