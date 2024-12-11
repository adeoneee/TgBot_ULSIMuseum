import asyncio
import asyncpg
import pandas as pd
from dotenv import load_dotenv
import os
 
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
 
EXCEL_FILE_PATH = "D:/submissionbot_ulsim/uploads/submissions.xlsx"
 
async def create_connection():
    conn = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    return conn


 
async def create_tables():
    conn = await create_connection()
    try:
        # Чтение SQL-скрипта
        with open('D:/submissionbot_ulsim/db/create_tables.pgsql', 'r') as file:
            query = file.read()
        await conn.execute(query)
        print("Таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        await conn.close()
 
if __name__ == "__main__":
    asyncio.run(create_tables())

async def save_submission_to_db(data):
    conn = await create_connection()
    query = """
    INSERT INTO submissions (full_name, age, workplace, contacts, description, file_path, username)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    """
    await conn.execute(query, data['full_name'], data['age'], data['workplace'], data['contacts'],
                        data['description'], data['file_path'], data['username'])
    await export_to_excel(conn)
    await conn.close()

async def export_to_excel(conn):
    try:
        query = """
        SELECT full_name, age, workplace, contacts, description, file_path, username
        FROM submissions
        """
        rows = await conn.fetch(query)
        columns = ["full_name", "age", "workplace", "contacts", "description", "file_path", "username"]

        df = pd.DataFrame(rows, columns=columns)
        df.to_excel(EXCEL_FILE_PATH, index=False, engine='openpyxl')

    except Exception as e:
        print(f"Ошибка при экспорте данных в Excel: {e}")
