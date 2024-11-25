# 数据库配置
DB_CONFIG = {
    'host': '47.95.36.122',
    'port': 3307,
    'username': 'root',
    'password': 'root',
    'db': 'aihuiyi'
}

# AI接口配置
AI_BASE_URL = "https://agentapi.baidu.com/assistant/getAnswer"
AI_APP_ID = "vtUzKD9XI7AQrFlkctsYIBzgYnYxVwKd"
AI_SECRET_KEY = "Mz5PHn9cL0d024vKc07kXIDumTcYd5WI"
AI_SOURCE = "vtUzKD9XI7AQrFlkctsYIBzgYnYxVwKd"
AI_FROM = "openapi"
AI_OPEN_ID = "aihuiyi"

# HTTP状态码
HTTP_OK = 0
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 500

# 错误消息
ERROR_USER_ID_REQUIRED = 'User ID is required'
ERROR_MISSING_PARAMS = 'Missing required parameters'
ERROR_NO_PARAGRAPH = 'No paragraph data available'
ERROR_AI_SERVICE = 'AI service error'
ERROR_SERVER = 'Server error'
ERROR_DATABASE = 'Database error' 