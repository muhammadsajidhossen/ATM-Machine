# Inventory Management System

## Overview
The **Inventory Management System** is a simple Python-based application built with `Tkinter` for managing product inventory. It allows users to add, update, delete, view, and search for products. Additionally, it provides the ability to export inventory data as a **PDF report** and import products from a **CSV file**.

## Features
- **Add Products**: Input product name, quantity, and price.
- **Update Products**: Modify existing product details.
- **Delete Products**: Remove a product from the database.
- **View Products**: Display all stored products in a popup window.
- **Prevent Duplicate Names**: The system ensures product names are unique.
- **Low Stock Alerts**: Displays a warning when stock is below 5.
- **Export to PDF**: Generate a PDF report of all products.
- **Import from CSV**: Load multiple products from a CSV file.
- **Dark Mode Toggle**: Switch between light and dark themes.

## Installation

1. **Install Python (if not installed)**
   - Download and install Python from [python.org](https://www.python.org/downloads/).

2. **Install Required Libraries**  
   Open a terminal or command prompt and run:
   ```bash
   pip install tk
   pip install tk fpdf pandas
   ```


## Running the Application

Run the Python script:
```bash
python inventory_management.py
```

## Importing a CSV File

### **Steps to Import a CSV File**
1. Click the **"Import CSV"** button in the application.
2. Select the `inventory_products.csv` file.
3. The products will be added to the inventory database.

### **CSV File Format**
Ensure the CSV file follows this format:
```csv
Product Name,Quantity,Price
Laptop,10,999.99
Mouse,50,19.99
Keyboard,30,49.99
...
```

### **Sample CSV File**
You can download a sample CSV file [here](inventory_products.csv).

## Exporting Products to PDF

1. Click on **"Export to PDF"**.
2. The system will generate a file named `inventory_report.pdf`.
3. The file will contain a list of all stored products.

## License
This project is open-source and available for modification and distribution.

## Author
Developed by **Your Name**  
For inquiries, contact: `your.email@example.com`
