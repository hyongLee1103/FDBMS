import psycopg2
import os
from psycopg2 import Error, OperationalError
from psycopg2.extensions import connection

def get_db_connection() -> connection:
    
    db_info = {
    	'host': '192.168.49.171',
        'port': 62484,
        'database': 'farmmap_database_v01',
        'user': 'Opt-Ai',
        'password': 'opt-ai'
    }

    try:
        conn = psycopg2.connect(**db_info)
        conn.autocommit = False
        return conn
         
    except OperationalError as e:
        print(f"데이터베이스 연결 오류 발생: {e}\n")
        return None
    
def execute_query(query) -> None:
	try:
		with get_db_connection() as connection:
			with connection.cursor() as cursor:   
				cursor.execute(query)
				connection.commit()
				print(f"쿼리 정상 수행 완료\n")

	except Error as e:
		print(f"데이터베이스 오류 발생: {e}\n")

	except Exception as e:
		print(f"알 수 없는 오류 발생: {e}\n")
		
def export_table_to_csv(schema: str, table: str) -> None:

	current_path = os.path.dirname(os.path.abspath(__file__))
	file_path = os.path.join(current_path, f"{table}.csv")

	copy_command = f"""
					COPY
					(
						SELECT * FROM {schema}."{table}"
					)
					TO STDOUT WITH CSV HEADER
					"""
	
	try:
		with open(file_path, "w", encoding="utf-8-sig") as f:
			try:
				with get_db_connection() as connection:
					with connection.cursor() as cursor:
						cursor.copy_expert(copy_command, f)
						print(f"{table}.csv 추출완료\n")

			except Error as e:
				print(f"데이터베이스 오류 발생: {e}\n")

	except OSError as e:
		print(f"파일 시스템 오류 발생: {e}\n")	

	except Exception as e:
		print(f"알 수 없는 오류 발생: {e}\n")
		

export_table_to_csv('statistics_db', '2025_팜맵갱신성과검증')

