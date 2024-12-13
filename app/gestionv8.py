import sqlite3
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

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

# Interface Tkinter avec ttkbootstrap
root = ttk.Window(themename="flatly")  # Applique le thème 'flatly'
root.title("Gestionnaire d'Inventaire")
root.geometry("600x500")

# Entrées pour ajouter un produit
ttk.Label(root, text="Nom du produit").grid(row=0, column=0, padx=10, pady=5)
entry_name = ttk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Description").grid(row=1, column=0, padx=10, pady=5)
entry_desc = ttk.Entry(root)
entry_desc.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="Prix").grid(row=2, column=0, padx=10, pady=5)
entry_price = ttk.Entry(root)
entry_price.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(root, text="Stock").grid(row=3, column=0, padx=10, pady=5)
entry_stock = ttk.Entry(root)
entry_stock.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(root, text="Catégorie").grid(row=4, column=0, padx=10, pady=5)
entry_category = ttk.Entry(root)
entry_category.grid(row=4, column=1, padx=10, pady=5)

ttk.Button(root, text="Ajouter un produit", bootstyle=SUCCESS, command=add_product).grid(row=5, column=0, columnspan=2, pady=10)

# Recherche de produit
ttk.Label(root, text="Recherche par nom ou catégorie").grid(row=6, column=0, padx=10, pady=5)
entry_search_name = ttk.Entry(root)
entry_search_name.grid(row=6, column=1, padx=10, pady=5)

ttk.Label(root, text="Catégorie").grid(row=7, column=0, padx=10, pady=5)
entry_search_category = ttk.Entry(root)
entry_search_category.grid(row=7, column=1, padx=10, pady=5)

ttk.Button(root, text="Rechercher un produit", bootstyle=INFO, command=search_product).grid(row=8, column=0, columnspan=2, pady=10)

# Vérification des stocks faibles
ttk.Button(root, text="Vérifier les stocks faibles", bootstyle=DANGER, command=check_low_stock).grid(row=9, column=0, columnspan=2, pady=10)

# Historique des transactions
ttk.Label(root, text="ID Produit pour historique").grid(row=10, column=0, padx=10, pady=5)
entry_product_id = ttk.Entry(root)
entry_product_id.grid(row=10, column=1, padx=10, pady=5)

ttk.Button(root, text="Historique des transactions", bootstyle=PRIMARY, command=show_transaction_history).grid(row=11, column=0, columnspan=2, pady=10)

# Tableau pour afficher les résultats
columns = ("ID", "Nom", "Description", "Prix", "Stock", "Catégorie")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

# Configuration des en-têtes
for col in columns:
    tree.heading(col, text=col)

root.mainloop()
