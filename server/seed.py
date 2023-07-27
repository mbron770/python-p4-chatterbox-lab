#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, Message
import time

fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():

    Message.query.delete()
    
    messages = []

    for i in range(20):
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        ) 
        print(f'loading - {20 - i} seconds left')
        messages.append(message)
        db.session.add(message)
        db.session.commit()
        time.sleep(1)
    print('messages loaded!')
        

    # db.session.add_all(messages)
    # db.session.commit()        

if __name__ == '__main__':
    with app.app_context():
        make_messages()
