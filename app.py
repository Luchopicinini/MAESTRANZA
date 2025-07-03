from flask import Flask, request, jsonify, send_file, render_template
from functools import wraps

app = Flask(__name__)

# ================== Datos simulados ==================
usuarios = [
    {"id": 1, "nombre": "admin", "rol": "administrador"},
    {"id": 2, "nombre": "juan", "rol": "supervisor"},
    {"id": 3, "nombre": "maria", "rol": "operario"},
    {"id": 4, "nombre": "carlos", "rol": "comprador"}
]

ordenes = []
pausas = []
inventario = []
movimientos = []
kits = []
historial_precios = []
proveedores = []

# ================== Decorador de roles ==================
def requiere_rol(roles_permitidos):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            usuario = request.headers.get('usuario', 'admin')  # ← valor por defecto
            encontrado = next((u for u in usuarios if u["nombre"] == usuario), None)
            if not encontrado or encontrado["rol"] not in roles_permitidos:
                return jsonify({"error": "Acceso denegado"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorador


# ================== Rutas de vistas HTML ==================
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/nuevo_item')
def formulario_nuevo_item():
    return render_template('nuevo_item.html')

@app.route('/movimiento')
def formulario_movimiento():
    return render_template('movimiento.html')

@app.route('/proveedor')
def formulario_proveedor():
    return render_template('proveedor.html')

@app.route('/kit')
def formulario_kit():
    return render_template('kit.html')

@app.route('/vista_inventario')
def vista_inventario():
    return render_template('inventario.html', inventario=inventario)

# ================== Endpoints JSON ==================
@app.route('/inventario', methods=['GET'])
@requiere_rol(['administrador', 'supervisor'])
def ver_inventario():
    return jsonify(inventario)

@app.route('/inventario', methods=['POST'])
@requiere_rol(['administrador', 'supervisor'])
def agregar_item_inventario():
    datos = request.get_json()
    nuevo_item = {
        "id": len(inventario) + 1,
        "item": datos["item"],
        "stock": datos["stock"],
        "descripcion": datos.get("descripcion", ""),
        "nro_serie": datos.get("nro_serie", ""),
        "ubicacion": datos.get("ubicacion", ""),
        "lote": datos.get("lote", ""),
        "fecha_vencimiento": datos.get("fecha_vencimiento", ""),
        "categoria": datos.get("categoria", ""),
        "etiquetas": datos.get("etiquetas", [])
    }
    inventario.append(nuevo_item)
    return jsonify({"mensaje": "Item agregado", "item": nuevo_item}), 201


@app.route('/movimiento', methods=['POST'])
@requiere_rol(['administrador', 'supervisor'])
def registrar_movimiento():
    datos = request.get_json()
    movimiento = {
        "id": len(movimientos) + 1,
        "tipo": datos["tipo"],
        "item_id": datos["item_id"],
        "cantidad": datos["cantidad"],
        "fecha": datos["fecha"],
        "proyecto": datos.get("proyecto", "")
    }
    item = next((i for i in inventario if i["id"] == datos["item_id"]), None)
    if not item:
        return jsonify({"error": "Item no encontrado"}), 404

    if datos["tipo"] in ["salida", "uso"]:
        if item["stock"] < datos["cantidad"]:
            return jsonify({"error": "Stock insuficiente"}), 400
        item["stock"] -= datos["cantidad"]
    elif datos["tipo"] == "entrada":
        item["stock"] += datos["cantidad"]

    movimientos.append(movimiento)
    return jsonify({"mensaje": "Movimiento registrado", "movimiento": movimiento}), 201

@app.route('/alertas', methods=['GET'])
@requiere_rol(['administrador', 'supervisor'])
def alertas_stock_bajo():
    umbral = 10
    alertas = [i for i in inventario if i["stock"] <= umbral]
    return jsonify({"alertas": alertas})

@app.route('/precio', methods=['POST'])
@requiere_rol(['administrador', 'supervisor'])
def registrar_precio():
    datos = request.get_json()
    historial_precios.append({
        "item_id": datos["item_id"],
        "precio": datos["precio"],
        "fecha": datos["fecha"]
    })
    return jsonify({"mensaje": "Precio registrado"}), 200

@app.route('/kits', methods=['POST'])
@requiere_rol(['administrador'])
def crear_kit():
    datos = request.get_json()
    nuevo_kit = {
        "id": len(kits) + 1,
        "nombre": datos["nombre"],
        "componentes": datos["componentes"]
    }
    kits.append(nuevo_kit)
    return jsonify({"mensaje": "Kit creado", "kit": nuevo_kit}), 201

@app.route('/reporte_inventario', methods=['GET'])
@requiere_rol(['administrador', 'supervisor'])
def generar_reporte():
    return jsonify({"inventario": inventario, "movimientos": movimientos})

@app.route('/registrar_movimiento')
def mostrar_formulario_movimiento():
    return render_template('registrar_movimiento.html')


@app.route('/proveedores', methods=['POST'])
@requiere_rol(['administrador'])
def agregar_proveedor():
    datos = request.get_json()
    proveedor = {
        "id": len(proveedores) + 1,
        "nombre": datos["nombre"],
        "contacto": datos["contacto"],
        "condiciones_pago": datos["condiciones_pago"]
    }
    proveedores.append(proveedor)
    return jsonify({"mensaje": "Proveedor agregado", "proveedor": proveedor}), 201

@app.route('/alertas_reposicion')
@requiere_rol(['administrador', 'supervisor'])
def alertas_reposicion():
    umbral = 10  # Puedes hacerlo configurable
    notificaciones_reposicion = [
        {
            "item_id": item["id"],
            "item": item["item"],
            "stock_actual": item["stock"],
            "mensaje": f"El ítem '{item['item']}' tiene stock bajo ({item['stock']})."
        }
        for item in inventario if item["stock"] <= umbral
    ]
    return render_template('alertas_reposicion.html', alertas=notificaciones_reposicion)

@app.route('/historial_precios')
@requiere_rol(['administrador', 'supervisor'])
def ver_historial_precios():
    return render_template('historial_precios.html', historial=historial_precios)

# ================== Usuarios, Órdenes, Pausas, Dashboard ==================
@app.route('/usuarios', methods=['POST'])
@requiere_rol(['administrador'])
def crear_usuario():
    datos = request.get_json()
    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": datos["nombre"],
        "rol": datos["rol"]
    }
    usuarios.append(nuevo_usuario)
    return jsonify({"mensaje": "Usuario creado", "usuario": nuevo_usuario}), 201

@app.route('/ordenes', methods=['POST'])
@requiere_rol(['supervisor', 'administrador'])
def registrar_orden():
    datos = request.get_json()
    nueva_orden = {
        "id": len(ordenes) + 1,
        "tarea": datos["tarea"],
        "operario": datos["operario"],
        "fecha": datos["fecha"]
    }
    ordenes.append(nueva_orden)
    return jsonify({"mensaje": "Orden registrada", "orden": nueva_orden}), 201

@app.route('/dashboard', methods=['GET'])
@requiere_rol(['supervisor', 'administrador'])
def dashboard():
    return jsonify({
        "ordenes_registradas": len(ordenes),
        "pausas_registradas": len(pausas),
        "usuarios_activos": len(usuarios)
    })

@app.route('/pausas', methods=['POST'])
@requiere_rol(['operario'])
def registrar_pausa():
    datos = request.get_json()
    nueva_pausa = {
        "usuario": datos["usuario"],
        "inicio": datos["inicio"],
        "motivo": datos["motivo"]
    }
    pausas.append(nueva_pausa)
    return jsonify({"mensaje": "Pausa registrada"}), 200

@app.route('/recuperar', methods=['POST'])
def recuperar_contraseña():
    datos = request.get_json()
    print(f"Recuperar contraseña para: {datos['correo']}")
    return jsonify({"mensaje": "Correo de recuperación enviado (simulado)"}), 200


# ----------------- Órdenes de Compra -----------------

@app.route('/ordenes_compra', methods=['POST'])
@requiere_rol(['comprador', 'administrador'])
def crear_orden_compra():
    datos = request.get_json()
    proveedor_id = datos.get('proveedor_id')
    items = datos.get('items')  # lista de {item_id, cantidad, precio_unitario}

    if not proveedor_id or not items:
        return jsonify({"error": "Faltan datos de proveedor o items"}), 400

    # Validar proveedor
    proveedor = next((p for p in proveedores if p['id'] == proveedor_id), None)
    if not proveedor:
        return jsonify({"error": "Proveedor no encontrado"}), 404

    # Validar items y calcular total
    total = 0
    for i in items:
        # Validar item
        item = next((it for it in inventario if it['id'] == i['item_id']), None)
        if not item:
            return jsonify({"error": f"Item con id {i['item_id']} no encontrado"}), 404
        if i['cantidad'] <= 0 or i['precio_unitario'] < 0:
            return jsonify({"error": "Cantidad o precio inválidos"}), 400
        total += i['cantidad'] * i['precio_unitario']

    orden = {
        "id": len(ordenes) + 1,
        "proveedor_id": proveedor_id,
        "proveedor_nombre": proveedor['nombre'],
        "fecha": datos.get('fecha', ''),
        "estado": "pendiente",  # pendiente, recibido, cancelado
        "total": total,
        "creado_por": request.headers.get('usuario', 'admin'),
        "items": items
    }
    ordenes.append(orden)
    return jsonify({"mensaje": "Orden de compra creada", "orden": orden}), 201


@app.route('/ordenes_compra', methods=['GET'])
@requiere_rol(['comprador', 'administrador', 'supervisor'])
def listar_ordenes_compra():
    return jsonify(ordenes)


@app.route('/ordenes_compra/<int:orden_id>/estado', methods=['PUT'])
@requiere_rol(['comprador', 'administrador'])
def actualizar_estado_orden(orden_id):
    datos = request.get_json()
    nuevo_estado = datos.get('estado')
    if nuevo_estado not in ['pendiente', 'recibido', 'cancelado']:
        return jsonify({"error": "Estado inválido"}), 400

    orden = next((o for o in ordenes if o['id'] == orden_id), None)
    if not orden:
        return jsonify({"error": "Orden no encontrada"}), 404

    orden['estado'] = nuevo_estado
    return jsonify({"mensaje": "Estado de orden actualizado", "orden": orden})

# --- Opcional: Ruta para ver detalles de un ítem en inventario ---
@app.route('/inventario/<int:item_id>', methods=['GET'])
@requiere_rol(['administrador', 'supervisor'])
def detalle_item(item_id):
    item = next((i for i in inventario if i['id'] == item_id), None)
    if not item:
        return jsonify({"error": "Item no encontrado"}), 404
    return jsonify(item)


if __name__ == '__main__':
    app.run(debug=True)
