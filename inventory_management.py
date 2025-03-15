import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import csv
from fpdf import FPDF

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("700x500")
        self.dark_mode = False  # Dark mode flag
        self.language = "en"  # Default language

        self.create_database()
        self.create_widgets()
        self.refresh_table()

    def create_database(self):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        # Entry Fields
        tk.Label(self.root, text="Product ID").grid(row=0, column=0)
        self.product_id = tk.Entry(self.root)
        self.product_id.grid(row=0, column=1)

        tk.Label(self.root, text="Product Name").grid(row=1, column=0)
        self.product_name = tk.Entry(self.root)
        self.product_name.grid(row=1, column=1)

        tk.Label(self.root, text="Quantity").grid(row=2, column=0)
        self.quantity = tk.Entry(self.root)
        self.quantity.grid(row=2, column=1)

        tk.Label(self.root, text="Price").grid(row=3, column=0)
        self.price = tk.Entry(self.root)
        self.price.grid(row=3, column=1)

        # Buttons
        tk.Button(self.root, text="Add Product", command=self.add_product).grid(row=4, column=0)
        tk.Button(self.root, text="Update Product", command=self.update_product).grid(row=4, column=1)
        tk.Button(self.root, text="Delete Product", command=self.delete_product).grid(row=5, column=0)
        tk.Button(self.root, text="Export PDF", command=self.export_pdf).grid(row=5, column=1)
        tk.Button(self.root, text="Import CSV", command=self.import_csv).grid(row=6, column=0)
        tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode).grid(row=6, column=1)

        # Search Bar
        tk.Label(self.root, text="Search").grid(row=7, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=7, column=1)
        tk.Button(self.root, text="Search", command=self.search_product).grid(row=7, column=2)

        # Treeview Table
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Quantity", "Price"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.grid(row=8, column=0, columnspan=3)

    def add_product(self):
        name = self.product_name.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a float")
            return

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE name=?", (name,))
        existing_product = c.fetchone()

        if existing_product:
            messagebox.showerror("Error", "Product name already exists.")
        else:
            c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
            conn.commit()
            messagebox.showinfo("Success", "Product added successfully")

            if quantity < 5:
                messagebox.showwarning("Stock Alert", f"{name} is running low!")

        conn.close()
        self.refresh_table()
        self.clear_fields()

    def update_product(self):
        product_id = self.product_id.get()
        name = self.product_name.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if not product_id or not name or not quantity or not price:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid input types")
            return

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?", (name, quantity, price, product_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product updated successfully")
        self.refresh_table()
        self.clear_fields()

    def delete_product(self):
        product_id = self.product_id.get()
        if not product_id:
            messagebox.showerror("Error", "Product ID is required")
            return

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product deleted successfully")
        self.refresh_table()
        self.clear_fields()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()

        for product in products:
            self.tree.insert("", "end", values=product)

    def search_product(self):
        search_term = self.search_entry.get()
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_term + '%',))
        products = c.fetchall()
        conn.close()

        for product in products:
            self.tree.insert("", "end", values=product)

    def export_pdf(self):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Inventory Report", ln=True, align="C")
        
        for product in products:
            pdf.cell(200, 10, f"ID: {product[0]}, Name: {product[1]}, Qty: {product[2]}, Price: {product[3]}", ln=True)

        pdf.output("inventory_report.pdf")
        messagebox.showinfo("Success", "PDF Report Generated!")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (row[0], int(row[1]), float(row[2])))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Products imported successfully!")
        self.refresh_table()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.root.configure(bg="black" if self.dark_mode else "white")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()
