from flask import Flask, request, jsonify
from models import db
from service import *
from constants import *
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 5
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10

db.init_app(app)

with app.app_context():
    db.create_all()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

def make_response(code=API_CODE_SUCCESS, msg=API_MSG_SUCCESS, data=None):
    return jsonify({
        "code": code,
        "msg": msg,
        "data": data if data is not None else {}
    })

@app.route('/startSession', methods=['POST'])
def start_session():
    user_id = request.json.get('user_id', None)
    
    if user_id is None:
        return make_response(API_CODE_BAD_REQUEST, ERROR_USER_ID_REQUIRED)
    
    try:
        result, session_id = create_session(user_id)
        if not result:
            return make_response(API_CODE_NOT_FOUND, ERROR_NO_PARAGRAPH)
            
        return make_response(data=result)
    except Exception as e:
        return make_response(API_CODE_SERVER_ERROR, str(e))

@app.route('/userAction', methods=['POST'])
def user_action():
    user_id = request.json.get('user_id')
    action_type = request.json.get('type')
    target = request.json.get('target')
    session_id = request.json.get('session_id')
    
    if not all([user_id, action_type, target, session_id]):
        return make_response(API_CODE_BAD_REQUEST, ERROR_MISSING_PARAMS)
    
    try:
        handle_user_action(user_id, action_type, target, session_id)
        return make_response(data={'message': 'Success'})
    except Exception as e:
        return make_response(API_CODE_SERVER_ERROR, str(e))

@app.route('/getUserActions', methods=['GET'])
def get_user_actions():
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')
    
    if not user_id or not session_id:
        return make_response(
            API_CODE_BAD_REQUEST, 
            'Both user_id and session_id are required'
        )
    
    try:
        results = get_user_actions(user_id, session_id)
        return make_response(data={
            'list': results,
            'total': len(results)
        })
    except Exception as e:
        return make_response(API_CODE_SERVER_ERROR, str(e))

@app.route('/userMessage', methods=['POST'])
def user_message():
    user_id = request.json.get('user_id')
    session_id = request.json.get('session_id')
    question = request.json.get('question')
    thread_id = request.json.get('thread_id')
    
    if not all([user_id, session_id, question]):
        return make_response(
            API_CODE_BAD_REQUEST, 
            'user_id, session_id, and question are required'
        )
    
    try:
        ai_result, new_thread_id = process_user_message(
            user_id, session_id, question, thread_id
        )
        
        return make_response(data={
            'content': ai_result,
            'thread_id': new_thread_id
        })
        
    except Exception as e:
        return make_response(API_CODE_SERVER_ERROR, str(e))

@app.route('/getMessages', methods=['GET'])
def get_messages():
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')
    
    if not user_id or not session_id:
        return make_response(
            API_CODE_BAD_REQUEST, 
            'Both user_id and session_id are required'
        )
    
    try:
        results = get_message_history(user_id, session_id)
        return make_response(data={
            'list': results,
            'total': len(results)
        })
    except Exception as e:
        return make_response(API_CODE_SERVER_ERROR, str(e))

if __name__ == '__main__':
    app.run(debug=True)
