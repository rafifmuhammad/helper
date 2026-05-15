from config import get_connection
from helper import get_all, execute_query

conn = get_connection()

# Get all Training data
dataTraining = get_all("SELECT * FROM tb_data WHERE Jenis='Training'")

dataTraining