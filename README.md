# 🏗️ Sistema de Control de Inventarios - Maestranza Unidos S.A.

Este proyecto corresponde al caso semestral **"Desarrollo de un Sistema de Control de Inventarios en Maestranza"**, desarrollado con **Flask (Python)**. El sistema está pensado para ayudar a gestionar eficientemente el inventario, los movimientos de stock, las órdenes de compra y la gestión operativa de la empresa **Maestranzas Unidos S.A.**

---

## 📌 Objetivos del sistema

- Eliminar el uso de registros manuales y hojas de cálculo.
- Mejorar el seguimiento en tiempo real del stock.
- Alertar automáticamente sobre ítems críticos o vencimientos.
- Facilitar la gestión de proveedores y órdenes de compra.
- Asegurar trazabilidad y control de todos los movimientos.

---

## ⚙️ Tecnologías utilizadas

- **Backend:** Flask (Python)
- **Frontend:** HTML (con Flask Templates)
- **Base de datos:** Simulada en memoria (listas en Python)
- **Arquitectura:** MVC simple
- **Control de versiones:** Git + GitHub

---

## 🚀 ¿Cómo ejecutar el sistema?

### 1. Clonar el repositorio

```bash
git clone https://github.com/Luchopicinini/MAESTRANZA.git
cd MAESTRANZA

2. Crear entorno virtual (opcional pero recomendable)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instalar dependencias
pip install flask

4. Ejecutar la aplicación

python app.py o py app.py (Dependiendo la version de phyton)

Luego abrí tu navegador en:
http://127.0.0.1:5000


Estructura del proyecto ----

MAESTRANZA/
│
├── app.py                # Código principal de la aplicación
├── templates/            # Archivos HTML renderizados con Flask
│   ├── index.html
│   ├── nuevo_item.html
│   ├── movimiento.html
│   ├── proveedor.html
│   ├── kit.html
│   └── ...
├── static/               # Carpeta opcional para CSS o JS
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Este archivo

