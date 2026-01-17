from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import redis
import psycopg2
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'appdb')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

# Redis connection
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
except:
    r = None

# Database connection function
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except:
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'backend-api'
    }), 200

@app.route('/api/status', methods=['GET'])
def status():
    """Get service status with dependencies"""
    redis_status = 'connected' if r and r.ping() else 'disconnected'
    
    db_status = 'disconnected'
    conn = get_db_connection()
    if conn:
        db_status = 'connected'
        conn.close()
    
    return jsonify({
        'api': 'running',
        'redis': redis_status,
        'database': db_status,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items from database"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not available'}), 503
    
    try:
        cur = conn.cursor()
        cur.execute('SELECT id, name, description, created_at FROM items ORDER BY created_at DESC;')
        items = cur.fetchall()
        cur.close()
        conn.close()
        
        items_list = [
            {
                'id': item[0],
                'name': item[1],
                'description': item[2],
                'created_at': item[3].isoformat() if item[3] else None
            }
            for item in items
        ]
        
        return jsonify(items_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items', methods=['POST'])
def create_item():
    """Create new item"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not available'}), 503
    
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;',
            (data['name'], data.get('description', ''))
        )
        item_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        # Invalidate cache
        if r:
            r.delete('items_cache')
        
        return jsonify({
            'id': item_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'message': 'Item created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/test', methods=['GET'])
def test_cache():
    """Test Redis cache"""
    if not r:
        return jsonify({'error': 'Redis not available'}), 503
    
    try:
        # Set a test value
        r.set('test_key', 'Hello from Redis!', ex=60)
        value = r.get('test_key')
        
        return jsonify({
            'cache': 'working',
            'test_value': value
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
