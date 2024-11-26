from models import db
from models.session import Session
from models.paragraph import Paragraph
from models.user_action import UserAction
from models.message import Message
import requests
from constants import *

def create_session(user_id):
    """创建会话并返回第一段文本"""
    # 创建新会话
    new_session = Session(user_id=user_id)
    db.session.add(new_session)
    db.session.commit()
    
    # 获取第一段文本
    paragraph = Paragraph.query.first()
    if not paragraph:
        return None, None
    
    result = paragraph.get_maps()
    result['session_id'] = new_session.id
    
    return result, new_session.id

def handle_user_action(user_id, action_type, target, session_id):
    """处理用户行为"""
    action = UserAction.query.filter_by(
        user_id=user_id,
        action_type=action_type,
        target=target,
        session_id=session_id
    ).first()
    
    if action:
        action.count += 1
    else:
        action = UserAction(
            user_id=user_id,
            action_type=action_type,
            target=target,
            session_id=session_id
        )
        db.session.add(action)
    
    db.session.commit()
    return True

def get_user_actions(user_id, session_id):
    """获取用户行为记录"""
    actions = UserAction.query.filter_by(
        user_id=user_id,
        session_id=session_id
    ).order_by(UserAction.create_time.desc()).all()
    
    return [action.to_dict() for action in actions]

def process_user_message(user_id, session_id, question, thread_id):
    """处理用户消息"""
    # AI请求部分保持不变
    ai_request_data = {
        "message": {
            "content": {
                "type": "text",
                "value": {
                    "showText": question
                }
            }
        },
        "source": AI_SOURCE,
        "from": AI_FROM,
        "openId": AI_OPEN_ID
    }
    
    params = {
        "appId": AI_APP_ID,
        "secretKey": AI_SECRET_KEY
    }
    
    if thread_id and thread_id != "0":
        params["threadId"] = thread_id
    
    response = requests.post(
        AI_BASE_URL,
        params=params,
        json=ai_request_data,
        headers={'Content-Type': 'application/json'}
    )

    print(response)
    
    # if response.status_code != HTTP_OK:
    #     raise Exception(f'AI service error: Status code {response.status_code}')
    
    ai_response = response.json()
    if ai_response.get('status') != 0:
        raise Exception(f'AI service error: {ai_response.get("message", "Unknown error")}')
    
    ai_result = ai_response['data']['content'][0]['data']
    new_thread_id = ai_response['data']['threadId']
    
    # 存储消息
    message = Message(
        user_id=user_id,
        session_id=session_id,
        thread_id=new_thread_id,
        user_content=question,
        ai_result=ai_result
    )
    db.session.add(message)
    db.session.commit()
    
    return ai_result, new_thread_id

def get_message_history(user_id, session_id):
    """获取消息历史"""
    messages = Message.query.filter_by(
        user_id=user_id,
        session_id=session_id
    ).order_by(Message.create_time.asc()).all()
    
    return [message.to_dict() for message in messages]