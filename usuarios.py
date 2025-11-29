#crear funciones
import psycopg2
from connection import get_connected

# crear tabla

def create_table_reg():
    conn = get_connected()
    if conn is None or conn is False:
        print("Error: No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conn.cursor()
        
        # Crear tabla de registro
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registro (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                contrasena VARCHAR(255) NOT NULL
            )
        """)
        
        conn.commit()
        print("Tabla 'registro' creada exitosamente")
        
    except psycopg2.Error as e:
        print(f"Error al crear la tabla: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#create_table_reg()

# insertar datos en la tabla registro
def insertar_registro(nombre, email, contrasena):
    conn = get_connected()
    if conn is None or conn is False:
        print("Error: No se pudo conectar a la base de datos")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Insertar registro
        cursor.execute("""
            INSERT INTO registro (nombre, email, contrasena)
            VALUES (%s, %s, %s)
        """, (nombre, email, contrasena))
        
        conn.commit()
        print(f"Registro insertado exitosamente para: {nombre}")
        return True
        
    except psycopg2.Error as e:
        print(f"Error al insertar el registro: {e}")
        conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# iniciar sesión con email y contrasena
def iniciar_sesion(email, contrasena):
    conn = get_connected()
    if conn is None or conn is False:
        print("Error: No se pudo conectar a la base de datos")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Buscar usuario con email y contrasena
        cursor.execute("""
            SELECT id, nombre, email 
            FROM registro 
            WHERE email = %s AND contrasena = %s
        """, (email, contrasena))
        
        usuario = cursor.fetchone()
        
        if usuario:
            print(f"Sesión iniciada exitosamente. Bienvenido: {usuario[1]}")
            return True
        else:
            print("Email o contraseña incorrectos")
            return False
        
    except psycopg2.Error as e:
        print(f"Error al iniciar sesión: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# verificar si el email existe
def email_existe(email):
    conn = get_connected()
    if conn is None or conn is False:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM registro WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        return usuario is not None
    except psycopg2.Error as e:
        print(f"Error al verificar email: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# recuperar contraseña por email
def recuperar_contrasena(email):
    conn = get_connected()
    if conn is None or conn is False:
        print("Error: No se pudo conectar a la base de datos")
        return None
    
    try:
        cursor = conn.cursor()
        
        # Buscar usuario por email
        cursor.execute("""
            SELECT id, nombre, email, contrasena 
            FROM registro 
            WHERE email = %s
        """, (email,))
        
        usuario = cursor.fetchone()
        
        if usuario:
            print(f"Contraseña recuperada para: {usuario[1]} ({usuario[2]})")
            return usuario[3]  # Retorna la contraseña
        else:
            print("No se encontró un usuario con ese email")
            return None
        
    except psycopg2.Error as e:
        print(f"Error al recuperar la contraseña: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
