from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json
import csv
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'LUNESSS'  

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Crear directorios si no existen
os.makedirs('datos', exist_ok=True)
os.makedirs('database', exist_ok=True)

# Modelo de base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mensaje = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'mensaje': self.mensaje,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_registro else None
        }

# Crear tablas
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return render_template('usuario.html', nombre=nombre)

# ==================== FORMULARIO ====================
@app.route('/formulario')
def mostrar_formulario():
    return render_template('formulario.html')

# ==================== PERSISTENCIA TXT ====================
@app.route('/guardar_txt', methods=['POST'])
def guardar_txt():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form.get('mensaje', '')
    
    # Guardar en archivo TXT
    with open('datos/datos.txt', 'a', encoding='utf-8') as archivo:
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        linea = f"[{fecha}] Nombre: {nombre} | Email: {email} | Mensaje: {mensaje}\n"
        archivo.write(linea)
    
    flash(f'Datos guardados exitosamente en archivo TXT para {nombre}!', 'success')
    return redirect(url_for('mostrar_formulario'))

@app.route('/leer_txt')
def leer_txt():
    try:
        with open('datos/datos.txt', 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        return render_template('resultado.html', 
                             titulo="Datos desde archivo TXT", 
                             contenido=contenido,
                             tipo="txt")
    except FileNotFoundError:
        return render_template('resultado.html', 
                             titulo="Datos desde archivo TXT", 
                             contenido="No hay datos guardados aún.",
                             tipo="txt")

# ==================== PERSISTENCIA JSON ====================
@app.route('/guardar_json', methods=['POST'])
def guardar_json():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form.get('mensaje', '')
    
    # Crear nuevo registro
    nuevo_registro = {
        'nombre': nombre,
        'email': email,
        'mensaje': mensaje,
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Leer datos existentes
    try:
        with open('datos/datos.json', 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = []
    
    # Agregar nuevo registro
    datos.append(nuevo_registro)
    
    # Guardar datos actualizados
    with open('datos/datos.json', 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
    
    flash(f'Datos guardados exitosamente en archivo JSON para {nombre}!', 'success')
    return redirect(url_for('mostrar_formulario'))

@app.route('/leer_json')
def leer_json():
    try:
        with open('datos/datos.json', 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        return render_template('resultado.html', 
                             titulo="Datos desde archivo JSON", 
                             datos_json=datos,
                             tipo="json")
    except (FileNotFoundError, json.JSONDecodeError):
        return render_template('resultado.html', 
                             titulo="Datos desde archivo JSON", 
                             contenido="No hay datos guardados aún.",
                             tipo="json")

@app.route('/api/datos_json')
def api_datos_json():
    """Endpoint API para obtener datos JSON"""
    try:
        with open('datos/datos.json', 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        return jsonify(datos)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify([])

# ==================== PERSISTENCIA CSV ====================
@app.route('/guardar_csv', methods=['POST'])
def guardar_csv():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form.get('mensaje', '')
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Verificar si el archivo existe para escribir encabezados
    archivo_existe = os.path.exists('datos/datos.csv')
    
    # Guardar en archivo CSV
    with open('datos/datos.csv', 'a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        
        # Escribir encabezados si es un archivo nuevo
        if not archivo_existe:
            writer.writerow(['Fecha', 'Nombre', 'Email', 'Mensaje'])
        
        # Escribir datos
        writer.writerow([fecha, nombre, email, mensaje])
    
    flash(f'Datos guardados exitosamente en archivo CSV para {nombre}!', 'success')
    return redirect(url_for('mostrar_formulario'))

@app.route('/leer_csv')
def leer_csv():
    try:
        with open('datos/datos.csv', 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            datos = list(reader)
        return render_template('resultado.html', 
                             titulo="Datos desde archivo CSV", 
                             datos_csv=datos,
                             tipo="csv")
    except FileNotFoundError:
        return render_template('resultado.html', 
                             titulo="Datos desde archivo CSV", 
                             contenido="No hay datos guardados aún.",
                             tipo="csv")

# ==================== PERSISTENCIA SQLite ====================
@app.route('/guardar_db', methods=['POST'])
def guardar_db():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form.get('mensaje', '')
    
    # Crear nuevo usuario
    nuevo_usuario = Usuario(nombre=nombre, email=email, mensaje=mensaje)
    
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash(f'Datos guardados exitosamente en base de datos para {nombre}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar en base de datos: {str(e)}', 'error')
    
    return redirect(url_for('mostrar_formulario'))

@app.route('/leer_db')
def leer_db():
    usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).all()
    return render_template('resultado.html', 
                         titulo="Datos desde Base de Datos SQLite", 
                         usuarios_db=usuarios,
                         tipo="db")

@app.route('/api/usuarios')
def api_usuarios():
    """Endpoint API para obtener usuarios de la base de datos"""
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios])

@app.route('/eliminar_usuario/<int:user_id>')
def eliminar_usuario(user_id):
    usuario = Usuario.query.get_or_404(user_id)
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash(f'Usuario {usuario.nombre} eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar usuario: {str(e)}', 'error')
    
    return redirect(url_for('leer_db'))

# ==================== RUTAS ADICIONALES ====================
@app.route('/estadisticas')
def estadisticas():
    # Contar registros en cada formato
    stats = {
        'txt': 0,
        'json': 0,
        'csv': 0,
        'db': Usuario.query.count()
    }
    
    # Contar líneas en TXT
    try:
        with open('datos/datos.txt', 'r', encoding='utf-8') as archivo:
            stats['txt'] = len(archivo.readlines())
    except FileNotFoundError:
        pass
    
    # Contar registros en JSON
    try:
        with open('datos/datos.json', 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            stats['json'] = len(datos)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    # Contar registros en CSV
    try:
        with open('datos/datos.csv', 'r', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            stats['csv'] = max(0, len(list(reader)) - 1)  # -1 para excluir encabezados
    except FileNotFoundError:
        pass
    
    return render_template('estadisticas.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)


