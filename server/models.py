from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable = False)
    body = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, default = db.func.now(), nullable = False)
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    
    
    @validates('username', 'body')
    def validate_info(self, key, value): 
        if type(value) != str: 
            raise ValueError(f'{value} must be a string')
        if(key == 'username'): 
            if(len(value) < 1 or len(value) > 25): 
                raise ValueError(f'{value} must be 1 and 25 chars')
        if(key == 'body'): 
            if(len(value) < 1 or len(value) > 500): 
                raise ValueError(f'{value} must be 1 and 500')
            
        return value 
 









        
    
            