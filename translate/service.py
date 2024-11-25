import json
import requests
from constants import *

def create_session(user_id, db_util):
    """创建会话并返回第一段文本"""
    # 创建新的会话记录
    session_sql = "INSERT INTO session (user_id) VALUES (%s)"
    session_id = db_util.insert_into_db(DB_CONFIG, session_sql, (user_id,))
    
    # 查询paragraph表的第一条记录
    paragraph_sql = "SELECT * FROM paragraph ORDER BY id LIMIT 1"
    data = db_util.read_from_db(DB_CONFIG, paragraph_sql)
    
    if not data or len(data) == 0:
        return None, None
    
    data = data[0]
    
    # 解析JSON字符串
    word_map = json.loads(data['word_map']) if data['word_map'] else {}
    sentence_map = json.loads(data['sentence_map']) if data['sentence_map'] else {}
    
    return {
        'content': data['content'],
        'word_translate': word_map,
        'sentence_translate': sentence_map,
        'session_id': session_id
    }, session_id

def handle_user_action(user_id, action_type, target, session_id, db_util):
    """处理用户行为"""
    query_sql = """
        SELECT id, count FROM user_action 
        WHERE user_id = %s AND action_type = %s AND target = %s AND session_id = %s
        LIMIT 1
    """
    data = db_util.read_from_db(DB_CONFIG, query_sql, (user_id, action_type, target, session_id))
    
    if data:
        update_sql = "UPDATE user_action SET count = count + 1 WHERE id = %s"
        db_util.insert_into_db(DB_CONFIG, update_sql, (data[0]['id'],))
    else:
        insert_sql = """
            INSERT INTO user_action (user_id, action_type, target, session_id, count) 
            VALUES (%s, %s, %s, %s, 1)
        """
        db_util.insert_into_db(DB_CONFIG, insert_sql, (user_id, action_type, target, session_id))
    
    return True

def get_user_actions(user_id, session_id, db_util):
    """获取用户行为记录"""
    sql = """
        SELECT id, user_id, action_type, target, session_id, count
        FROM user_action 
        WHERE user_id = %s AND session_id = %s
        ORDER BY create_time DESC
    """
    
    results = db_util.read_from_db(DB_CONFIG, sql, (user_id, session_id))
    return results

def process_user_message(user_id, session_id, question, thread_id, db_util):
    """处理用户消息"""
    ai_request_data = {
        "message": {
            "content": {
                "type": "text",
                "value": {
                    "showText": question
                }
            }
        }
    }
    
    params = {
        "appId": AI_APP_ID,
        "secretKey": AI_SECRET_KEY
    }
    if thread_id and thread_id != 0:
        params["threadId"] = thread_id

    print(params)

    response = requests.post(
        AI_BASE_URL,
        params=params,
        json=ai_request_data,
        headers={'Content-Type': 'application/json'}
    )

    print(response.status_code, " ", response.content)

    
    ai_response = response.json()
    if ai_response.get('status') != 0:
        raise Exception(f'AI service error: {ai_response.get("message", "Unknown error")}')
    
    ai_result = ai_response['data']['content'][0]['data']
    new_thread_id = ai_response['data']['threadId']

    print('in')
    
    # 存储消息记录
    sql = """
        INSERT INTO message 
            (user_id, session_id, thread_id, user_content, ai_result, create_time, update_time)
        VALUES 
            (%s, %s, %s, %s, %s, NOW(), NOW())
    """
    db_util.insert_into_db(
        DB_CONFIG, 
        sql, 
        (user_id, session_id, new_thread_id, question, ai_result)
    )
    
    return ai_result, new_thread_id

def get_message_history(user_id, session_id, db_util):
    """获取消息历史记录"""
    sql = """
        SELECT 
            id,
            user_id,
            session_id,
            thread_id,
            user_content,
            ai_result,
            DATE_FORMAT(create_time, '%Y-%m-%d %H:%i:%s') as create_time
        FROM message 
        WHERE user_id = %s AND session_id = %s
        ORDER BY create_time ASC
    """
    
    results = db_util.read_from_db(DB_CONFIG, sql, (user_id, session_id))
    return results