#crear los endpoints
from flask import Flask, request, jsonify
from flask_cors import CORS
from usuarios import create_table_reg, insertar_registro, iniciar_sesion, recuperar_contrasena, email_existe

app = Flask(__name__)
CORS(app)



# Registrar usuario
@app.route('/registro', methods=['POST'])
def registro():
    try:
        data = request.get_json()
        
        # Validar que los campos sean obligatorios
        if not data.get('nombre') or not data.get('email') or not data.get('contrasena'):
            return jsonify({"message": "Todos los campos son obligatorios: nombre, email, contrasena"}), 400
        
        nombre = data['nombre']
        email = data['email']
        contrasena = data['contrasena']
        
        # Validar que el email no esté registrado
        if email_existe(email):
            return jsonify({"message": "El email ya está registrado"}), 400
        
        # Insertar registro
        resultado = insertar_registro(nombre, email, contrasena)
        
        if resultado:
            return jsonify({"message": "Registro exitoso"}), 200
        else:
            return jsonify({"message": "Error al registrar"}), 500
            
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validar que los campos sean obligatorios
        if not data.get('email') or not data.get('contrasena'):
            return jsonify({"message": "Email y contraseña son obligatorios"}), 400
        
        email = data['email']
        contrasena = data['contrasena']
        
        # Iniciar sesión
        resultado = iniciar_sesion(email, contrasena)
        
        if resultado:
            return jsonify({"message": "Login exitoso"}), 200
        else:
            return jsonify({"message": "Credenciales incorrectas"}), 401
            
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Recuperar contraseña
@app.route('/recuperar-contrasena', methods=['POST'])
def recuperar_password():
    data = request.get_json()
    contrasena = recuperar_contrasena(data['email'])
    return jsonify({"contrasena": contrasena}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

    