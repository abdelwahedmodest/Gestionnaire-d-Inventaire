import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview

# ... (Rest of the code remains the same)

# Create the main window
root = Tk()
root.title("Gestionnaire d'Inventaire")
root.configure(bg="#FF76AF")  # Set background color to dark gray

# Create frames for different sections
product_frame = Frame(root, bg="#1e1e1e")
search_frame = Frame(root, bg="#1e1e1e")
history_frame = Frame(root, bg="#1e1e1e")
result_frame = Frame(root, bg="#1e1e1e")

# ... (Place frames in the root window using grid layout)

# Product information frame
Label(product_frame, text="Nom du produit", fg="white", bg="#1e1e1e").grid(row=0, column=0)
# ... (Other labels and entry fields for product info)

# Search and filter frame
Label(search_frame, text="Recherche par nom ou catégorie", fg="white", bg="#1e1e1e").grid(row=0, column=0)
# ... (Other labels and entry fields for search)

# Transaction history frame
Label(history_frame, text="ID Produit pour historique", fg="white", bg="#1e1e1e").grid(row=0, column=0)
# ... (Entry field and button for transaction history)

# Result frame
tree = Treeview(result_frame, columns=("ID", "Nom", "Description", "Prix", "Stock", "Catégorie"), show="headings")
tree.grid(row=0, column=0)

# ... (Rest of the GUI setup and function definitions)

root.mainloop()