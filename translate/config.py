MYSQL_CONFIG = {
    'host': '47.95.36.122',
    'port': 3307,
    'user': 'root',
    'password': 'root',
    'database': 'aihuiyi',
    'pool_size': 5,
    'max_overflow': 10
}

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}" 