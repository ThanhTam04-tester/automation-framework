from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Khởi tạo DB Khách sạn (Gồm Phòng và Lịch đặt)
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Bảng Phòng
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT, price INTEGER, status TEXT)''')
    # Bảng Đặt phòng
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, room_id INTEGER, customer_name TEXT, phone TEXT)''')
    
    # Thêm sẵn vài phòng mẫu nếu DB trống
    cursor.execute("SELECT COUNT(*) FROM rooms")
    if cursor.fetchone()[0] == 0:
        sample_rooms = [
            ('Phòng 101', 'Standard', 500000, 'Trống'),
            ('Phòng 102', 'VIP', 1200000, 'Trống'),
            ('Phòng 201', 'Family', 850000, 'Trống')
        ]
        cursor.executemany("INSERT INTO rooms (name, type, price, status) VALUES (?, ?, ?, ?)", sample_rooms)
    
    conn.commit()
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    return render_template('index.html')
# THÊM ĐOẠN NÀY ĐỂ MỞ TRANG GIỚI THIỆU
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/blog')
def blog():
    return render_template('blog.html')
@app.route('/rooms')
def rooms():
    return render_template('rooms.html')
    # THÊM ĐOẠN NÀY VÀO APP.PY
@app.route('/contact')
def contact():
    return render_template('contact.html')

# THÊM ĐOẠN NÀY VÀO APP.PY
@app.route('/elements')
def elements():
    return render_template('elements.html')

@app.route('/services')
def services():
    return render_template('services.html')

# --- API CHO AUTOMATION TEST ---

# 1. API Lấy danh sách phòng
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rooms = [{'id': r[0], 'name': r[1], 'type': r[2], 'price': r[3], 'status': r[4]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(rooms)

# 2. API Đặt phòng (Nhận thông tin khách và update trạng thái phòng)
@app.route('/api/book', methods=['POST'])
def book_room():
    data = request.get_json()
    room_id = data.get('room_id')
    customer_name = data.get('customer_name')
    phone = data.get('phone')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Kiểm tra xem phòng còn trống không
    cursor.execute("SELECT status FROM rooms WHERE id = ?", (room_id,))
    room = cursor.fetchone()
    
    if not room or room[0] != 'Trống':
        conn.close()
        return jsonify({'error': 'Phòng này đã có người đặt hoặc không tồn tại!'}), 400
        
    # Lưu thông tin đặt phòng
    cursor.execute("INSERT INTO bookings (room_id, customer_name, phone) VALUES (?, ?, ?)", (room_id, customer_name, phone))
    # Chuyển trạng thái phòng
    cursor.execute("UPDATE rooms SET status = 'Đã đặt' WHERE id = ?", (room_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Đặt phòng thành công!'}), 201

if __name__ == '__main__':
    app.run(debug=True)