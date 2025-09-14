# repository.py
from __future__ import annotations
import mysql.connector
from typing import List, Optional
from models import Producto

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "appweb",
    "port": 3307
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# -------------------- PRODUCTOS --------------------

def init_db() -> None:
    """Crea la tabla productos si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio FLOAT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            idusuario INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(255) NOT NULL,
            mail VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# CRUD PRODUCTOS
def crear_producto(p: Producto) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (id, nombre, cantidad, precio) VALUES (%s,%s,%s,%s)",
        (p.id, p.nombre, p.cantidad, p.precio)
    )
    conn.commit()
    cursor.close()
    conn.close()

def listar_todos() -> List[Producto]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Producto(r["id"], r["nombre"], r["cantidad"], r["precio"]) for r in rows]

def obtener_por_id(id_: int) -> Optional[Producto]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id=%s", (id_,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row: return None
    return Producto(row["id"], row["nombre"], row["cantidad"], row["precio"])

def eliminar_producto(id_: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id_,))
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_nombre(id_: int, nombre: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET nombre=%s WHERE id=%s", (nombre, id_))
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_cantidad(id_: int, cantidad: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET cantidad=%s WHERE id=%s", (cantidad, id_))
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_precio(id_: int, precio: float) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET precio=%s WHERE id=%s", (precio, id_))
    conn.commit()
    cursor.close()
    conn.close()

def buscar_por_nombre(patron: str) -> List[Producto]:
    patron_like = f"%{(patron or '').strip()}%"
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE LOWER(nombre) LIKE LOWER(%s) ORDER BY id", (patron_like,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Producto(r["id"], r["nombre"], r["cantidad"], r["precio"]) for r in rows]

# -------------------- USUARIOS --------------------

def crear_usuario(nombre: str, mail: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, mail) VALUES (%s,%s)", (nombre, mail))
    conn.commit()
    cursor.close()
    conn.close()

def listar_usuarios() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios ORDER BY idusuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

def obtener_usuario_por_id(idusuario: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE idusuario=%s", (idusuario,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def actualizar_usuario(idusuario: int, nombre: str, mail: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET nombre=%s, mail=%s WHERE idusuario=%s", (nombre, mail, idusuario))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_usuario(idusuario: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE idusuario=%s", (idusuario,))
    conn.commit()
    cursor.close()
    conn.close()
