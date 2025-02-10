from flask import Flask, render_template, request, send_file
import mysql.connector
import csv
import io

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

# ✅ 보존기간 변환 매핑
PRESERVATION_PERIOD_MAP = {
    45: "영구",
    40: "준영구",
    30: "30년",
    10: "10년",
    5: "5년",
    3: "3년",
    1: "1년",
    0: "미확인"
}

# ✅ 반출 순위 변환 매핑
RETRIEVAL_PRIORITY_MAP = {
    1: "1순위",
    2: "2순위",
    3: "3순위",
    0: "미확인"
}

# ✅ 메인 대시보드 페이지 (통계 포함)
@app.route('/')
def main_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ 보존기간별 통계 초기화
    storage_data = {
        "제1기록관": {p: 0 for p in PRESERVATION_PERIOD_MAP.values()},
        "제2기록관": {p: 0 for p in PRESERVATION_PERIOD_MAP.values()},
        "행정박물관": {p: 0 for p in PRESERVATION_PERIOD_MAP.values()}
    }

    total_sums = {p: 0 for p in PRESERVATION_PERIOD_MAP.values()}
    total_sums["합계"] = 0  # 전체 합계 초기화

    cursor.execute("""
        SELECT storage_location, preservation_period, COUNT(*) AS total
        FROM documents
        WHERE storage_location IN ('제1기록관', '제2기록관', '행정박물관')
        GROUP BY storage_location, preservation_period
    """)

    location_totals = {"제1기록관": 0, "제2기록관": 0, "행정박물관": 0}

    for row in cursor.fetchall():
        location = row["storage_location"]
        period = PRESERVATION_PERIOD_MAP.get(row["preservation_period"], "미확인")

        if location in storage_data:
            storage_data[location][period] += row["total"]
            location_totals[location] += row["total"]

        total_sums[period] += row["total"]
        total_sums["합계"] += row["total"]

    # ✅ 생산 유형별 통계 초기화
    format_data = {
        "제1기록관": {f: 0 for f in ["문서", "카드", "대장", "도면", "필름", "앨범", "테이프", "간행물", "행정박물"]},
        "제2기록관": {f: 0 for f in ["문서", "카드", "대장", "도면", "필름", "앨범", "테이프", "간행물", "행정박물"]},
        "행정박물관": {f: 0 for f in ["문서", "카드", "대장", "도면", "필름", "앨범", "테이프", "간행물", "행정박물"]}
    }

    total_format_sums = {f: 0 for f in ["합계", "문서", "카드", "대장", "도면", "필름", "앨범", "테이프", "간행물", "행정박물"]}

    location_format_totals = {"제1기록관": 0, "제2기록관": 0, "행정박물관": 0}

    cursor.execute("""
        SELECT storage_location, document_format, COUNT(*) AS total
        FROM documents
        WHERE storage_location IN ('제1기록관', '제2기록관', '행정박물관')
        GROUP BY storage_location, document_format
    """)

    for row in cursor.fetchall():
        location = row["storage_location"]
        format_type = row["document_format"]

        if location in format_data:
            format_data[location][format_type] += row["total"]
            location_format_totals[location] += row["total"]

        total_format_sums[format_type] += row["total"]
        total_format_sums["합계"] += row["total"]

    cursor.close()
    conn.close()

    return render_template(
        'Main_Dashboard.html',
        storage_data=storage_data,
        total_sums=total_sums,
        format_data=format_data,
        total_format_sums=total_format_sums,
        location_totals=location_totals,
        location_format_totals=location_format_totals
    )

if __name__ == '__main__':
    app.run(debug=True)


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

    # ✅ 변환 적용 (보존기간, 반출 순위)
    for doc in documents:
        doc["preservation_period"] = PRESERVATION_PERIOD_MAP.get(doc["preservation_period"], "미확인")
        doc["retrieval_priority"] = RETRIEVAL_PRIORITY_MAP.get(doc["retrieval_priority"], "미확인")

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

    # ✅ 보존기간 및 반출 순위 변환 후 CSV 저장
    for doc in documents:
        doc["preservation_period"] = PRESERVATION_PERIOD_MAP.get(doc["preservation_period"], "미확인")
        doc["retrieval_priority"] = RETRIEVAL_PRIORITY_MAP.get(doc["retrieval_priority"], "미확인")

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
