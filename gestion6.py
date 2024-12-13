import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview

# Connect to the database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create tables if they don't exist
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

# Function to add a product
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
        messagebox.showinfo("Success", "Product added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid values.")

# Function to search for a product
def search_product():
    name = entry_search_name.get()
    category = entry_search_category.get()

    query = "SELECT * FROM Products WHERE name LIKE ? OR category LIKE ?"
    cursor.execute(query, ('%' + name + '%', '%' + category + '%'))
    results = cursor.fetchall()

    # Display results in the Treeview
    for row in results:
        tree.insert("", "end", values=row)

# Function to check low stock
def check_low_stock():
    cursor.execute("SELECT * FROM Products WHERE stock < 10")
    results = cursor.fetchall()

    # Display results in the Treeview
    for row in results:
        tree.insert("", "end", values=row)

# Function to show transaction history
def show_transaction_history():
    product_id = entry_product_id.get()

    cursor.execute("""
    SELECT t.id, t.change, t.date, p.name 
    FROM Transactions t
    JOIN Products p ON t.product_id = p.id
    WHERE p.id = ?""", (product_id,))

    results = cursor.fetchall()

    # Display results in the Treeview
    for row in results:
        tree.insert("", "end", values=row)

# Create the main window
root = Tk()
root.title("Gestionnaire d'Inventaire")
root.configure(bg="#1e1e1e")  # Set background color to dark gray

# Create labels and entry fields for adding a product
Label(root, text="Nom du produit", fg="white", bg="#1e1e1e").grid(row=0, column=0)
entry_name = Entry(root)
entry_name.grid(row=0, column=1)

Label(root, text="Description", fg="white", bg="#1e1e1e").grid(row=1, column=0)
entry_desc = Entry(root)
entry_desc.grid(row=1, column=1)

Label(root, text="Prix", fg="white", bg="#1e1e1e").grid(row=2, column=0)
entry_price = Entry(root)
entry_price.grid(row=2, column=1)

Label(root, text="Stock", fg="white", bg="#1e1e1e").grid(row=3, column=0)
entry_stock = Entry(root)
entry_stock.grid(row=3, column=1)

Label(root, text="Catégorie", fg="white", bg="#1e1e1e").grid(row=4, column=0)
entry_category = Entry(root)
entry_category.grid(row=4, column=1)

# Create button to add a product
Button(root, text="AJOUTER UN PRODUIT", fg="white", bg="#4285f4", command=add_product).grid(row=5, column=0, columnspan=2)

# Create labels and entry fields for searching a product
Label(root, text="Recherche par nom ou catégorie", fg="white", bg="#1e1e1e").grid(row=6, column=0)
entry_search_name = Entry(root)
entry_search_name.grid(row=6, column=1)

Label(root, text="Catégorie", fg="white", bg="#1e1e1e").grid(row=7, column=0)
entry_search_category = Entry(root)
entry_search_category.grid(row=7, column=1)

# Create button to search for a product
Button(root, text="RECHERCHER UN PRODUIT", fg="white", bg="#4285f4", command=search_product).grid(row=8, column=0, columnspan=2)

# Create button to check low stock
Button(root, text="VERIFIER LES STOCKS FAIBLES", fg="white", bg="#4285f4", command=check_low_stock).grid(row=9, column=0, columnspan=2)

# Create label and entry field for transaction history
Label(root, text="ID Produit pour historique", fg="white", bg="#1e1e1e").grid(row=10, column=0)
entry_product_id = Entry(root)
entry_product_id.grid(row=10, column=1)

# Create button to show transaction history
Button(root, text="HISTORIQUE DES TRANSACTIONS", fg="white", bg="#4285f4", command=show_transaction_history).grid(row=11, column=0, columnspan=2)

# Create Treeview widget to display results
tree = Treeview(root, columns=("ID", "Nom", "Description", "Prix", "Stock", "Catégorie"), show="headings")
tree.grid(row=12, column=0, columnspan=2)

tree.heading("ID", text="ID")
tree.heading("Nom", text="Nom")
tree.heading("Description", text="Description")
tree.heading("Prix", text="Prix")
tree.heading("Stock", text="Stock")
tree.heading("Catégorie", text="Catégorie")

# Start the GUI
root.mainloop()