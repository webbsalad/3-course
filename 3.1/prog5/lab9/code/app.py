from flask import Flask, request, jsonify
import psycopg2
import jwt
import bcrypt
from psycopg2 import sql
from dotenv import load_dotenv
import os
import datetime
from functools import wraps

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

class JWTFactory:
    def __init__(self, secret_key, algorithm='HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, user_id, expiration_minutes=60):
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expiration_minutes)
        payload = {
            'user_id': user_id,
            'exp': expiration_time
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None  
        except jwt.InvalidTokenError:
            return None  

jwt_factory = JWTFactory(SECRET_KEY)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user_id = jwt_factory.decode_token(token)
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        kwargs['user_id'] = user_id
        return f(*args, **kwargs)
    
    return decorated

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

class BonusLevelObserver:
    def __init__(self, db_conn):
        self.conn = db_conn

    def update_bonus_level(self, user_id, new_spendings):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT level_id FROM user_info WHERE id = %s;", (user_id,))
            result = cursor.fetchone()
            if not result:
                return False, 'User not found'
            current_level_id = result[0]

            cursor.execute("""
                SELECT id, name, min_spendings, cashback_percentage
                FROM bonus_levels
                WHERE min_spendings <= %s
                ORDER BY min_spendings DESC
                LIMIT 1;
            """, (new_spendings,))
            new_level = cursor.fetchone()

            if not new_level:
                return False, 'No suitable bonus level found'

            new_level_id = new_level[0]

            if new_level_id != current_level_id:
                cursor.execute("UPDATE user_info SET level_id = %s WHERE id = %s;", (new_level_id, user_id))
                self.conn.commit()
                return True, 'Bonus level updated'
            else:
                return True, 'No change in bonus level'
        except Exception as e:
            self.conn.rollback()
            return False, str(e)
        finally:
            cursor.close()

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM user_info WHERE username = %s;", (username,))
        if cursor.fetchone():
            return jsonify({'error': 'Username already exists'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("SELECT id FROM bonus_levels ORDER BY min_spendings ASC LIMIT 1;")
        bonus_level = cursor.fetchone()
        if not bonus_level:
            return jsonify({'error': 'Bonus levels not found'}), 500

        level_id = bonus_level[0]

        cursor.execute("""
            INSERT INTO user_info (username, passhash, level_id)
            VALUES (%s, %s, %s) RETURNING id;
        """, (username, hashed_password, level_id))
        user_id = cursor.fetchone()[0]
        conn.commit()

        token = jwt_factory.create_token(user_id)

        return jsonify({'token': token, 'user_id': user_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, passhash FROM user_info WHERE username = %s;", (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_id, stored_hash = user
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            token = jwt_factory.create_token(user_id)
            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/users/<int:id>/bonus', methods=['GET'])
@token_required
def get_user_bonus(id, user_id):
    if id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT b.id, b.name, b.min_spendings, b.cashback_percentage
            FROM user_info u
            JOIN bonus_levels b ON u.level_id = b.id
            WHERE u.id = %s;
        """, (id,))
        bonus = cursor.fetchone()

        if not bonus:
            return jsonify({'error': 'Bonus level not found'}), 404

        bonus_data = {
            'id': bonus[0],
            'name': bonus[1],
            'min_spendings': bonus[2],
            'cashback_percentage': bonus[3]
        }

        return jsonify(bonus_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/users/<int:id>/transactions', methods=['POST'])
@token_required
def add_transaction(id, user_id):
    if id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    amount = data['amount']
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid transaction amount'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO transactions (user_id, amount) VALUES (%s, %s) RETURNING id;",
            (id, amount)
        )
        transaction_id = cursor.fetchone()[0]

        cursor.execute(
            "UPDATE user_info SET spendings = spendings + %s WHERE id = %s RETURNING spendings;",
            (amount, id)
        )
        new_spendings = cursor.fetchone()[0]
        conn.commit()

        observer = BonusLevelObserver(conn)
        success, message = observer.update_bonus_level(id, new_spendings)

        response = {
            'transaction_id': transaction_id,
            'amount': amount,
            'new_spendings': new_spendings,
            'bonus_update': message
        }

        return jsonify(response), 201 if success else 400
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
