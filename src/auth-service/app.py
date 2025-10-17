from flask import Flask, request, jsonify
import jwt
import datetime
from supabase import create_client
import os
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-devops-2024'

# Configuración Supabase
supabase_url = os.getenv('SUPABASE_URL', 'https://vqezennldyqazxjmyrfj.supabase.co')
supabase_key = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxZXplbm5sZHlxYXp4am15cmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNTUzNjIsImV4cCI6MjA3NTgzMTM2Mn0.TSuCHoKKabXAQ2FlRn7BFYa_ii7WKBSBrkRr8xsuf5s')
supabase = create_client(supabase_url, supabase_key)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "auth-service running"})

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
result = supabase.table('users').insert({
    'email': email,
    'password': hashed_password.decode('utf-8'),  # Hasheado
    'role': role
}).execute()
        
        # Generar JWT
        token = jwt.encode({
            'user_id': result.data[0]['id'],
            'email': email,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "message": "Usuario registrado", 
            "token": token,
            "user": {"email": email, "role": role}
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Verificar usuario en Supabase
        result = supabase.table('users').select('*').eq('email', email).execute()
        
if not result.data or not bcrypt.checkpw(password.encode('utf-8'), result.data[0]['password'].encode('utf-8')):
    return jsonify({"error": "Credenciales inválidas"}), 401
            
user = result.data[0]
        
        # Generar JWT
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "message": "Login exitoso",
            "token": token,
            "user": {"email": user['email'], "role": user['role']}
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/verify', methods=['POST'])
def verify_token():
    try:
        token = request.json.get('token')
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({"valid": True, "user": decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "Token inválido"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)