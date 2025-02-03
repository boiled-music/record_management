import mysql.connector

# MariaDB 연결 설정
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # MariaDB 서버 주소 (localhost로 설정)
        user='root',  # MariaDB 사용자명
        password='a12345678!',  # MariaDB 비밀번호
        database='record_management_db'  # 사용할 데이터베이스 이름
    )
    return connection
