from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import csv

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def hola_mundo():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM personas ORDER BY id DESC')
    lista_usuarios = cursor.fetchall()
    conn.close()
    return render_template('index.html', usuarios=lista_usuarios)

@app.route('/saludo', methods=['POST'])
def saludo():
    nombre_ingresado = request.form.get('usuario')
    if nombre_ingresado:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO personas (nombre) VALUES (?)', (nombre_ingresado,))
        conn.commit()
        conn.close()
    return render_template('saludo.html', nombre=nombre_ingresado)

@app.route('/eliminar/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM personas WHERE id = ?', (usuario_id,))
    conn.commit()
    conn.close()
    return redirect('/')

# RUTA ACTUALIZADA: Exporta a formato CSV para Excel
@app.route('/exportar')
def exportar_datos():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM personas ORDER BY id ASC')
    filas = cursor.fetchall()
    conn.close()

    # Definimos la ruta del archivo con extensión .csv en Descargas
    ruta_excel = '/sdcard/Download/reporte_usuarios.csv'
    
    # Escribimos los datos usando el módulo CSV de Python
    with open(ruta_excel, 'w', newline='', encoding='utf-8-sig') as f:
        escritor = csv.writer(f, delimiter=';') # El punto y coma asegura compatibilidad directa en Excel
        
        # Escribimos los encabezados de las columnas
        escritor.writerow(['ID Único', 'Nombre de Usuario'])
        
        # Escribimos todos los registros
        for id_u, nombre_u in filas:
            escritor.writerow([id_u, nombre_u])

    # Enviamos el archivo listo para abrir en hojas de cálculo
    return send_file(ruta_excel, as_attachment=True, download_name='reporte_usuarios.csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
