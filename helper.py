from config import get_connection

def get_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results

def execute_query(query, params):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())

    conn.commit()
    cursor.close()
    conn.close()