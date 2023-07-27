from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if(request.method == 'GET'):
        all_messages = Message.query.all()
        messages = []
        for message in all_messages: 
            messages.append(message.to_dict())
        return messages
    elif(request.method == 'POST'):
        data = request.json
        message = Message()
        try:
            for attr in data: 
                setattr(message, attr, data[attr])
            db.session.add(message)
            db.session.commit()
            return message.to_dict(), 201
        except (IntegrityError, ValueError) as ie:
            return {'error': ie.args}, 422
    
    
@app.route('/messages/<int:id>', )
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555)
