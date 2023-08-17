from fastapi import FastAPI, HTTPException
from schemas import User, Message
from db import users_table, messages_table

app = FastAPI()


@app.post('/users', response_model=User, status_code=201)
def create_user(user: User):
    user.id = len(users_table)
    users_table.append(user)
    return user


@app.get('/users', response_model=list[User], status_code=200)
def list_users():
    return users_table


@app.post('/messages/{user_id}', response_model=Message, status_code=201)
def create_message(user_id: int, message: Message):
    message.id = len(messages_table)
    if user_id > len(users_table):
        raise HTTPException(status_code=404, detail="User not found")
    message.user_id = user_id
    messages_table.append(message)
    return message


@app.get('/messages', response_model=list[Message], status_code=200)
def list_messages():
    return messages_table
