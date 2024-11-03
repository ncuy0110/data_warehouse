from os import getenv

input_path = getenv("INPUT_PATH",'input_data/DATASET.xlsx')
output_path = getenv("OUTPUT_PATH",'output_data/')

# Đường dẫn output cho các file CSV
output_path = getenv("OUTPUT_PATH", 'output_data/')

MONGO_HOST = getenv("MONGO_HOST", "localhost")
MONGO_PORT = getenv("MONGO_PORT", "27017")
MONGO_USER = getenv("MONGO_USER", "datawarehouse")
MONGO_PASSWORD = getenv("MONGO_PASSWORD", "123")
MONGO_DB_NAME = getenv("MONGO_DB_NAME", "data_warehouse")