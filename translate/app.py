from flask import Flask, request, jsonify
import databaseUtil
import service
from constants import *

app = Flask(__name__)

@app.route('/startSession', methods=['POST'])
def start_session():
    user_id = request.json.get('user_id', None)
    
    if user_id is None:
        return jsonify({'error': ERROR_USER_ID_REQUIRED}), HTTP_BAD_REQUEST
    
    try:
        result, session_id = service.create_session(user_id, databaseUtil)
        if not result:
            return jsonify({'error': ERROR_NO_PARAGRAPH}), HTTP_NOT_FOUND
            
        return jsonify(result), HTTP_OK
    except Exception as e:
        return jsonify({'error': ERROR_SERVER, 'message': str(e)}), HTTP_SERVER_ERROR

@app.route('/userAction', methods=['POST'])
def user_action():
    user_id = request.json.get('user_id')
    action_type = request.json.get('type')
    target = request.json.get('target')
    session_id = request.json.get('session_id')
    
    if not all([user_id, action_type, target, session_id]):
        return jsonify({'error': ERROR_MISSING_PARAMS}), HTTP_BAD_REQUEST
    
    try:
        service.handle_user_action(user_id, action_type, target, session_id, databaseUtil)
        return jsonify({'message': 'Success'}), HTTP_OK
    except Exception as e:
        return jsonify({'error': ERROR_SERVER, 'message': str(e)}), HTTP_SERVER_ERROR

@app.route('/getUserActions', methods=['GET'])
def get_user_actions():
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')
    
    if not user_id or not session_id:
        return jsonify({
            'error': ERROR_MISSING_PARAMS,
            'message': 'Both user_id and session_id are required'
        }), HTTP_BAD_REQUEST
    
    try:
        results = service.get_user_actions(user_id, session_id, databaseUtil)
        return jsonify({
            'success': True,
            'data': results,
            'total': len(results)
        }), HTTP_OK
    except Exception as e:
        return jsonify({
            'error': ERROR_DATABASE,
            'message': str(e)
        }), HTTP_SERVER_ERROR

@app.route('/userMessage', methods=['POST'])
def user_message():
    user_id = request.json.get('user_id')
    session_id = request.json.get('session_id')
    question = request.json.get('question')
    thread_id = request.json.get('thread_id')
    
    if not all([user_id, session_id, question]):
        return jsonify({
            'error': ERROR_MISSING_PARAMS,
            'message': 'user_id, session_id, and question are required'
        }), HTTP_BAD_REQUEST
    
    try:
        ai_result, new_thread_id = service.process_user_message(
            user_id, session_id, question, thread_id, databaseUtil
        )
        
        return jsonify({
            'success': True,
            'data': ai_result,
            'thread_id': new_thread_id
        }), HTTP_OK
        
    except Exception as e:
        return jsonify({
            'error': ERROR_SERVER,
            'message': str(e)
        }), HTTP_SERVER_ERROR

@app.route('/getMessages', methods=['GET'])
def get_messages():
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')
    
    if not user_id or not session_id:
        return jsonify({
            'error': ERROR_MISSING_PARAMS,
            'message': 'Both user_id and session_id are required'
        }), HTTP_BAD_REQUEST
    
    try:
        results = service.get_message_history(user_id, session_id, databaseUtil)
        return jsonify({
            'success': True,
            'data': results,
            'total': len(results)
        }), HTTP_OK
    except Exception as e:
        return jsonify({
            'error': ERROR_DATABASE,
            'message': str(e)
        }), HTTP_SERVER_ERROR

if __name__ == '__main__':
    app.run(debug=True)
