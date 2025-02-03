from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    # MariaDB 연결
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="a12345678!",
        database="record_management_db"  # 데이터베이스 이름도 변경 가능
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents;")  # 예시 테이블
    documents = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', documents=documents)

if __name__ == '__main__':
    app.run(debug=True)
