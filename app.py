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

    # 보존기간별 통계 초기화
    storage_data = {
        "제1기록관": {p: 0 for p in PRESERVATION_PERIOD_MAP.values()},
        "제2기록관": {p: 0 for p in PRESERVATION_PERIOD_MAP.values()},
        "행정박물관": {p: 0 for p in PRESERVATION_PERIOD_MAP.values()}
    }
    total_sums = {p: 0 for p in PRESERVATION_PERIOD_MAP.values()}
    total_sums["합계"] = 0

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

    # 생산 유형별 통계 초기화
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

# ✅ 문서 검색/활용 페이지 (/search로 변경됨)
@app.route('/search')
def search():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔍 검색 필터 처리
    management_number = request.args.get('management_number', '')
    production_department = request.args.get('production_department', '')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')
    
    # Main_Dashboard에서 전송된 search_query 처리 → 기록물철 제목 검색
    folder_title = request.args.get('folder_title', '')
    search_query = request.args.get('search_query', '')
    if search_query:
        folder_title = search_query

    preservation_period = request.args.get('preservation_period', '')
    document_type = request.args.get('document_type', '')

    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    # 페이지네이션 처리
    per_page = int(request.args.get('per_page', 20))
    current_page = int(request.args.get('page', 1))
    offset = (current_page - 1) * per_page

    # SQL 쿼리 생성 (필터 적용)
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
    query += f" ORDER BY {sort_by} {sort_order}"
    query += " LIMIT %s OFFSET %s"
    params.extend([per_page, offset])

    cursor.execute(query, params)
    documents = cursor.fetchall()

    for doc in documents:
        doc["preservation_period"] = PRESERVATION_PERIOD_MAP.get(doc["preservation_period"], "미확인")
        doc["retrieval_priority"] = RETRIEVAL_PRIORITY_MAP.get(doc["retrieval_priority"], "미확인")

    # 전체 페이지 수 계산 (검색 필터 적용)
    count_query = "SELECT COUNT(*) AS total FROM documents WHERE 1=1"
    count_params = []
    if management_number:
        count_query += " AND management_number LIKE %s"
        count_params.append(f"%{management_number}%")
    if production_department:
        count_query += " AND production_department LIKE %s"
        count_params.append(f"%{production_department}%")
    if start_year and end_year:
        count_query += " AND production_year BETWEEN %s AND %s"
        count_params.extend([start_year, end_year])
    if folder_title:
        count_query += " AND folder_title LIKE %s"
        count_params.append(f"%{folder_title}%")
    if preservation_period:
        count_query += " AND preservation_period = %s"
        count_params.append(preservation_period)
    if document_type:
        count_query += " AND document_type = %s"
        count_params.append(document_type)

    cursor.execute(count_query, count_params)
    total_documents = cursor.fetchone()['total']
    total_pages = (total_documents // per_page) + (1 if total_documents % per_page != 0 else 0)

    cursor.close()
    conn.close()

    return render_template('search.html',
                           documents=documents,
                           per_page=per_page,
                           current_page=current_page,
                           total_pages=total_pages,
                           sort_by=sort_by,
                           sort_order=sort_order)

# CSV 다운로드 (전체 다운로드)
@app.route('/download_csv_all')
def download_csv_all():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM documents")
    documents = cursor.fetchall()

    # 보존기간 및 반출 순위 변환
    for doc in documents:
        doc["preservation_period"] = PRESERVATION_PERIOD_MAP.get(doc["preservation_period"], "미확인")
        doc["retrieval_priority"] = RETRIEVAL_PRIORITY_MAP.get(doc["retrieval_priority"], "미확인")
    
    # 원하는 CSV 헤더(순서 및 이름)
    headers = [
        "연번", "관리번호", "현재기관명", "생산기관명", "서고위치", "서가위치", "박스번호",
        "생산년도", "종료년도", "보존기간", "기록물구분", "기록물형태", "수량",
        "기록물철제목", "부가정보", "이중보존여부", "평가/폐기", "상태검사", "반출순위", "비고"
    ]
    
    # 각 행에서 created_at, updated_at은 출력하지 않고, 나머지 값은 문서 dict의 키에 따라 가져오며, 
    # 없는 키는 빈 문자열로 처리
    new_docs = []
    for idx, doc in enumerate(documents, start=1):
        new_doc = {
            "연번": idx,
            "관리번호": doc.get("management_number", ""),
            "현재기관명": doc.get("current_institution", ""),
            "생산기관명": doc.get("production_department", ""),
            "서고위치": doc.get("storage_location", ""),
            "서가위치": doc.get("shelf_location", ""),  # 해당 데이터가 없다면 빈 문자열로 출력
            "박스번호": doc.get("box_number", ""),
            "생산년도": doc.get("production_year", ""),
            "종료년도": doc.get("end_year", ""),
            "보존기간": doc.get("preservation_period", ""),
            "기록물구분": doc.get("document_type", ""),
            "기록물형태": doc.get("document_format", ""),
            "수량": doc.get("quantity", ""),
            "기록물철제목": doc.get("folder_title", ""),
            "부가정보": doc.get("additional_info", ""),
            "이중보존여부": doc.get("dual_preservation", ""),
            "평가/폐기": doc.get("evaluation_status", ""),
            "상태검사": doc.get("status_check", ""),
            "반출순위": doc.get("retrieval_priority", ""),
            "비고": doc.get("notes", "")
        }
        new_docs.append(new_doc)
    
    # CSV 작성 (UTF-8 BOM 추가: 'utf-8-sig')
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    writer.writerows(new_docs)
    output.seek(0)

    cursor.close()
    conn.close()

    return send_file(io.BytesIO(output.getvalue().encode('utf-8-sig')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='all_documents.csv')

# CSV 다운로드 (검색 목록 다운로드)
@app.route('/download_csv_search')
def download_csv_search():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    management_number = request.args.get('management_number', '')
    production_department = request.args.get('production_department', '')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')
    
    folder_title = request.args.get('folder_title', '')
    search_query = request.args.get('search_query', '')
    if search_query:
        folder_title = search_query

    preservation_period = request.args.get('preservation_period', '')
    document_type = request.args.get('document_type', '')

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

    cursor.execute(query, params)
    documents = cursor.fetchall()

    for doc in documents:
        doc["preservation_period"] = PRESERVATION_PERIOD_MAP.get(doc["preservation_period"], "미확인")
        doc["retrieval_priority"] = RETRIEVAL_PRIORITY_MAP.get(doc["retrieval_priority"], "미확인")
    
    headers = [
        "연번", "관리번호", "현재기관명", "생산기관명", "서고위치", "서가위치", "박스번호",
        "생산년도", "종료년도", "보존기간", "기록물구분", "기록물형태", "수량",
        "기록물철제목", "부가정보", "이중보존여부", "평가/폐기", "상태검사", "반출순위", "비고"
    ]
    
    new_docs = []
    for idx, doc in enumerate(documents, start=1):
        new_doc = {
            "연번": idx,
            "관리번호": doc.get("management_number", ""),
            "현재기관명": doc.get("current_institution", ""),
            "생산기관명": doc.get("production_department", ""),
            "서고위치": doc.get("storage_location", ""),
            "서가위치": doc.get("shelf_location", ""),
            "박스번호": doc.get("box_number", ""),
            "생산년도": doc.get("production_year", ""),
            "종료년도": doc.get("end_year", ""),
            "보존기간": doc.get("preservation_period", ""),
            "기록물구분": doc.get("document_type", ""),
            "기록물형태": doc.get("document_format", ""),
            "수량": doc.get("quantity", ""),
            "기록물철제목": doc.get("folder_title", ""),
            "부가정보": doc.get("additional_info", ""),
            "이중보존여부": doc.get("dual_preservation", ""),
            "평가/폐기": doc.get("evaluation_status", ""),
            "상태검사": doc.get("status_check", ""),
            "반출순위": doc.get("retrieval_priority", ""),
            "비고": doc.get("notes", "")
        }
        new_docs.append(new_doc)
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    writer.writerows(new_docs)
    output.seek(0)

    cursor.close()
    conn.close()

    return send_file(io.BytesIO(output.getvalue().encode('utf-8-sig')),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='search_documents.csv')

if __name__ == '__main__':
    app.run(debug=True)
