import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview  # Importer Treeview depuis tkinter.ttk

# Connexion à la base de données
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Création des tables si elles n'existent pas
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
cursor.execute("""
CREATE TABLE IF NOT EXISTS Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    change INTEGER NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (product_id) REFERENCES Products(id)
)
""")
conn.commit()

# Fonction pour ajouter un produit
def add_product():
    try:
        name = entry_name.get()
        desc = entry_desc.get()
        price = float(entry_price.get())
        stock = int(entry_stock.get())
        category = entry_category.get()
        
        cursor.execute("INSERT INTO Products (name, description, price, stock, category) VALUES (?, ?, ?, ?, ?)",
                       (name, desc, price, stock, category))
        conn.commit()
        messagebox.showinfo("Succès", "Produit ajouté avec succès!")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")

# Fonction pour rechercher un produit
def search_product():
    name = entry_search_name.get()
    category = entry_search_category.get()
    
    query = "SELECT * FROM Products WHERE name LIKE ? OR category LIKE ?"
    cursor.execute(query, ('%' + name + '%', '%' + category + '%'))
    results = cursor.fetchall()
    
    # Affichage des résultats dans le tableau
    for row in results:
        tree.insert("", "end", values=row)

# Fonction pour afficher les stocks faibles
def check_low_stock():
    cursor.execute("SELECT * FROM Products WHERE stock < 10")
    results = cursor.fetchall()
    
    # Affichage des résultats dans le tableau
    for row in results:
        tree.insert("", "end", values=row)

# Fonction pour afficher l'historique des transactions
def show_transaction_history():
    product_id = entry_product_id.get()
    
    cursor.execute("""
    SELECT t.id, t.change, t.date, p.name 
    FROM Transactions t
    JOIN Products p ON t.product_id = p.id
    WHERE p.id = ?""", (product_id,))
    
    results = cursor.fetchall()
    
    # Affichage des résultats dans le tableau
    for row in results:
        tree.insert("", "end", values=row)

# Interface Tkinter
root = Tk()
root.title("Gestionnaire d'Inventaire")

# Canvas pour structurer l'interface
canvas = Canvas(root, width=800, height=600, bg="#e0f7fa")
canvas.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Ajout d'un titre au Canvas
canvas.create_text(400, 30, text="Gestionnaire d'Inventaire", font=("Arial", 20, "bold"), fill="navy")

# Section pour ajouter un produit
frame_input = Frame(root, bg="#b2ebf2", relief="sunken", padx=20, pady=20)
frame_input.grid(row=1, column=0, padx=10, pady=10, sticky="w")

Label(frame_input, text="Nom du produit", bg="#b2ebf2").grid(row=0, column=0)
entry_name = Entry(frame_input)
entry_name.grid(row=0, column=1)

Label(frame_input, text="Description", bg="#b2ebf2").grid(row=1, column=0)
entry_desc = Entry(frame_input)
entry_desc.grid(row=1, column=1)

Label(frame_input, text="Prix", bg="#b2ebf2").grid(row=2, column=0)
entry_price = Entry(frame_input)
entry_price.grid(row=2, column=1)

Label(frame_input, text="Stock", bg="#b2ebf2").grid(row=3, column=0)
entry_stock = Entry(frame_input)
entry_stock.grid(row=3, column=1)

Label(frame_input, text="Catégorie", bg="#b2ebf2").grid(row=4, column=0)
entry_category = Entry(frame_input)
entry_category.grid(row=4, column=1)

Button(frame_input, text="Ajouter un produit", command=add_product).grid(row=5, column=0, columnspan=2)

# Section pour rechercher un produit
frame_search = Frame(root, bg="#b2ebf2", relief="sunken", padx=20, pady=20)
frame_search.grid(row=2, column=0, padx=10, pady=10, sticky="w")

Label(frame_search, text="Recherche par nom ou catégorie", bg="#b2ebf2").grid(row=0, column=0)
entry_search_name = Entry(frame_search)
entry_search_name.grid(row=0, column=1)

Label(frame_search, text="Catégorie", bg="#b2ebf2").grid(row=1, column=0)
entry_search_category = Entry(frame_search)
entry_search_category.grid(row=1, column=1)

Button(frame_search, text="Rechercher un produit", command=search_product).grid(row=2, column=0, columnspan=2)

# Vérification des stocks faibles
Button(root, text="Vérifier les stocks faibles", command=check_low_stock).grid(row=3, column=0, columnspan=2)

# Historique des transactions
frame_transaction = Frame(root, bg="#b2ebf2", relief="sunken", padx=20, pady=20)
frame_transaction.grid(row=4, column=0, padx=10, pady=10, sticky="w")

Label(frame_transaction, text="ID Produit pour historique", bg="#b2ebf2").grid(row=0, column=0)
entry_product_id = Entry(frame_transaction)
entry_product_id.grid(row=0, column=1)

Button(frame_transaction, text="Historique des transactions", command=show_transaction_history).grid(row=1, column=0, columnspan=2)

# Tableau pour afficher les résultats
tree = Treeview(root, columns=("ID", "Nom", "Description", "Prix", "Stock", "Catégorie"), show="headings")
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

tree.heading("ID", text="ID")
tree.heading("Nom", text="Nom")
tree.heading("Description", text="Description")
tree.heading("Prix", text="Prix")
tree.heading("Stock", text="Stock")
tree.heading("Catégorie", text="Catégorie")

root.mainloop()
