import sqlite3

# Conectar a SQLite
connection = sqlite3.connect('LittleLemon.db')
cursor = connection.cursor()

# Obtener la cantidad máxima
def get_max_quantity():
    cursor.execute("SELECT MAX(Quantity) FROM Orders")
    return cursor.fetchone()[0]

# Añadir reserva
def add_booking(order_data):
    query = """
    INSERT OR IGNORE INTO Orders (
        OrderID, OrderDate, DeliveryDate, CustomerID, CustomerName, City, Country, PostalCode, CountryCode,
        Sales, Quantity, Discount, DeliveryCost, CourseName, CuisineName, StarterName, DessertName, Drink, Sides
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, order_data)
    connection.commit()

# Actualizar reserva
def update_booking(order_id, updates):
    set_clause = ", ".join([f"{key}=?" for key in updates.keys()])
    query = f"UPDATE Orders SET {set_clause} WHERE OrderID=?"
    cursor.execute(query, list(updates.values()) + [order_id])
    connection.commit()

# Cancelar reserva
def cancel_booking(order_id):
    cursor.execute("DELETE FROM Orders WHERE OrderID=?", (order_id,))
    connection.commit()

# Cerrar conexión
def close_connection():
    cursor.close()
    connection.close()
    print("Conexión a SQLite cerrada.")

max = get_max_quantity()

print(max)

cursor.close()
