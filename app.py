from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# ✅ MariaDB 연결 함수
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='a12345678!',  # 자신의 MariaDB 비밀번호 입력
        database='record_management_db',
        charset='utf8mb4',
        collation='utf8mb4_general_ci'  # Collation 명시
    )

# ✅ 메인 대시보드 페이지 (기본 페이지)
@app.route('/')
def main_dashboard():
    return render_template('Main_Dashboard.html')  # 메인 대시보드 파일로 연결

# ✅ 보유 문서 목록 페이지
@app.route('/documents')
def documents():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔍 검색 필터 처리
    management_number = request.args.get('management_number', '')
    production_department = request.args.get('production_department', '')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')
    folder_title = request.args.get('folder_title', '')
    preservation_period = request.args.get('preservation_period', '')
    document_type = request.args.get('document_type', '')

    # 정렬 처리
    sort_by = request.args.get('sort_by', 'id')  # 기본 정렬: ID
    sort_order = request.args.get('sort_order', 'asc')  # asc 또는 desc

    # 페이지네이션 처리
    per_page = int(request.args.get('per_page', 20))
    current_page = int(request.args.get('page', 1))
    offset = (current_page - 1) * per_page

    # SQL 쿼리 생성
    query = "SELECT * FROM documents WHERE 1=1"
    params = []

    if management_number:
        query += " AND management_number LIKE %s"
        params.append(f"%{management_number}%")

    if production_department:
        query += " AND production_department LIKE %s"
        params.append(f"%{production_department}%")

    if start_year and end_year:
        query += " AND production_year BETWEEN %s AND %s"
        params.extend([start_year, end_year])

    if folder_title:
        query += " AND folder_title LIKE %s"
        params.append(f"%{folder_title}%")

    if preservation_period:
        query += " AND preservation_period = %s"
        params.append(preservation_period)

    if document_type:
        query += " AND document_type = %s"
        params.append(document_type)

    # 정렬 기능 추가
    query += f" ORDER BY {sort_by} {sort_order}"

    # LIMIT 및 OFFSET 추가 (페이지네이션 적용)
    query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    documents = cursor.fetchall()

    # 전체 페이지 수 계산
    cursor.execute("SELECT COUNT(*) AS total FROM documents WHERE 1=1")
    total_documents = cursor.fetchone()['total']
    total_pages = (total_documents // per_page) + (1 if total_documents % per_page != 0 else 0)

    cursor.close()
    conn.close()

    return render_template('documents.html',
                           documents=documents,
                           per_page=per_page,
                           current_page=current_page,
                           total_pages=total_pages,
                           sort_by=sort_by,
                           sort_order=sort_order)

# ✅ CSV 다운로드 기능
@app.route('/download_csv')
def download_csv():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM documents")
    documents = cursor.fetchall()

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=documents[0].keys())
    writer.writeheader()
    writer.writerows(documents)

    output.seek(0)
    cursor.close()
    conn.close()

    return send_file(io.BytesIO(output.getvalue().encode('utf-8')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='documents.csv')

if __name__ == '__main__':
    app.run(debug=True)