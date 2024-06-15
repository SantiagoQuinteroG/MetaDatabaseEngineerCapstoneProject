import pandas as pd
import sqlite3

# Ruta del archivo Excel
excel_file_path = './data/sample_data_meta.xlsx'

# Nombre del archivo de la base de datos SQLite
sqlite_db_path = 'LittleLemon.db'

# Leer el archivo Excel
df_orders = pd.read_excel(excel_file_path, sheet_name='Orders')

# Conectar a la base de datos SQLite (se creará si no existe)
connection = sqlite3.connect(sqlite_db_path)
cursor = connection.cursor()

# Crear la tabla Orders si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    OrderID TEXT PRIMARY KEY,
    OrderDate TEXT,
    DeliveryDate TEXT,
    CustomerID TEXT,
    CustomerName TEXT,
    City TEXT,
    Country TEXT,
    PostalCode TEXT,
    CountryCode TEXT,
    Sales REAL,
    Quantity INTEGER,
    Discount REAL,
    DeliveryCost REAL,
    CourseName TEXT,
    CuisineName TEXT,
    StarterName TEXT,
    DessertName TEXT,
    Drink TEXT,
    Sides TEXT
);
""")

# Insertar datos en la tabla Orders
for index, row in df_orders.iterrows():
    # Convertir fechas a cadena en formato ISO
    order_date = row['Order Date'].strftime('%Y-%m-%d') if pd.notnull(row['Order Date']) else None
    delivery_date = row['Delivery Date'].strftime('%Y-%m-%d') if pd.notnull(row['Delivery Date']) else None

    query = """
    INSERT OR IGNORE INTO Orders (
        OrderID, OrderDate, DeliveryDate, CustomerID, CustomerName, City, Country, PostalCode, CountryCode,
        Sales, Quantity, Discount, DeliveryCost, CourseName, CuisineName, StarterName, DessertName, Drink, Sides
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    data = (
        row['Order ID'], order_date, delivery_date, row['Customer ID'], row['Customer Name'], row['City'],
        row['Country'], row['Postal Code'], row['Country Code'], row['Sales'], row['Quantity'], row['Discount'],
        row['Delivery Cost'], row['Course Name'], row['Cuisine Name'], row['Starter Name'], row['Desert Name'],
        row['Drink'], row['Sides']
    )
    cursor.execute(query, data)

# Confirmar los cambios
connection.commit()

print("Datos insertados exitosamente en la tabla Orders.")

# Cerrar la conexión
cursor.close()
connection.close()
print("Conexión a SQLite cerrada.")
