import sqlite3

def inicializar_bd():
    conn = sqlite3.connect('maestranza.db')
    cursor = conn.cursor()

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contacto TEXT,
        condiciones_pago TEXT
    );

    CREATE TABLE IF NOT EXISTS ordenes_compra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proveedor_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'pendiente',
        total REAL NOT NULL,
        creado_por TEXT NOT NULL,
        FOREIGN KEY(proveedor_id) REFERENCES proveedores(id)
    );

    CREATE TABLE IF NOT EXISTS detalle_orden (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orden_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY(orden_id) REFERENCES ordenes_compra(id),
        FOREIGN KEY(item_id) REFERENCES inventario(id)
    );
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_bd()
