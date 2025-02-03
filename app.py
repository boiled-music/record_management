from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MariaDB 연결 함수
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='a12345678!',  # 자신의 MariaDB 비밀번호 입력
        database='record_management_db',
        charset='utf8mb4',
        collation='utf8mb4_general_ci'  # Collation 명시
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM documents')
    documents = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', documents=documents)

if __name__ == '__main__':
    app.run(debug=True)
