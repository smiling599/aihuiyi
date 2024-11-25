import pymysql
import json
from datetime import datetime
import requests

def get_connection(db_config):
    return pymysql.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['username'],
        passwd=db_config['password'],
        db=db_config['db'],
        charset='utf8mb4',
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor
    )

def read_from_db(db_config, sql, params=None):
    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
            
        result = cursor.fetchall()
        return result
    finally:
        if connection:
            connection.close()

def insert_into_db(db_config, sql, params=None):
    connection = None
    try:
        connection = get_connection(db_config)
        cursor = connection.cursor()
        
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
            
        connection.commit()
        last_id = cursor.lastrowid
        return last_id
    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if connection:
            connection.close()