from flask import Flask, request, jsonify
from database import Database
app = Flask(__name__)

# Rota de GET com parâmetros de filtro
@app.route('/', methods=['GET', 'POST'])
def root():
    return response(True, 'Welcome!')

# Rota de GET com parâmetros de filtro
@app.route('/news', methods=['GET'])
def get_news():
    db = Database()
    fill = request.args.to_dict()
    status, data = db.get_news(fill)

    return response(status, data)

def response(success, data):
    if(success):
        return jsonify({'success': True, 'data': data, 'statusCode': 200})
    else:
        return jsonify({'success': False, 'error': data, 'statusCode': 500})

if __name__ == '__main__':
    app.run(debug=False)

''''
FLASK_APP=app.py && flask run --reload
'''