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
        all = Message.query.order_by(Message.created_at).all()
        messages = []
        for message in all: 
            messages.append(message.to_dict())
        return messages 
    else: 
        data = request.json 
        message = Message()
        try: 
            for attr in data: 
                setattr(message, attr, data[attr])
                
            db.session.add(message)
            db.session.commit()
            return message.to_dict(), 201
        except(IntegrityError, ValueError) as ie: 
            return {'error': ie.args}, 422
        
@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id): 
    message = Message.query.filter(Message.id == id).first()
    
    if not message: 
        return {}, 404
    if(request.method == 'GET'): 
        return message.to_dict() 
    elif(request.method == 'PATCH'): 
        data = request.json
        try: 
            for attr in data: 
                setattr(message, attr, data[attr])
            db.session.commit()
            return message.to_dict(), 200
        except(IntegrityError, ValueError) as ie: 
            return {'error': ie.args}, 422
        
    db.session.delete(message)
    db.session.commit()
    
    return {}, 204
    

    
if __name__ == '__main__':
    app.run(port=5555)
