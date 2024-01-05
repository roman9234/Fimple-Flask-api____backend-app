from flask import Flask, jsonify, request
import uuid
from random import randint
import functools

from model.post import Post
from model.user import User

from utilities.functions import compare_uuid, generate_uuid, encode_json_users, encode_json_posts, decode_json_users, decode_json_posts

# декоратор - отлов ошибок
def exception_handle(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({'response':'unknown exception: ' + str(e)})
    return wrapper

app = Flask(__name__)

# CRUD:
# CREATE - создание сущности на сервере - POST
# RETRIEVE - чтение сущности с сервера - GET
# UPDATE - обновление/изменение сущности - PUT
# DELETE - удаление сущности - DELETE

# регистрация
# пример тела запроса:
{
    "nickname": "user_5",
    "password": "qwerty123"
}

@app.route('/sign_up', methods=['POST'])
@exception_handle
def sign_up():

    users = decode_json_users()
    data = request.get_json()
    nickname = data['nickname']
    password = data['password']

    user = User(generate_uuid(), nickname, password)
    users += [user]
    encode_json_users(users)

    return jsonify({'response':'success'})

# вход в аккаунт
# пример тела запроса:
{
    "nickname": "user_1",
    "password": "qwerty123"
}

@app.route('/sign_in', methods=['GET'])
@exception_handle
def sign_in():

    users = decode_json_users()
    data = request.get_json()
    nickname = data['nickname']
    password = data['password']

    for x in users:
        if(x.nickname == nickname and x.password == password):
            return jsonify({'response':'signed_in', 'token': randint(0, 10)})

    return jsonify({'response':'failed to sign in'})

    
# изменение аккаунта (не изменяется uuid)
# пример тела запроса:
{
    "uuid": "68889f94-daf7-4a9b-9ff2-5c9bfa2264cf",
    "nickname": "user_3", 
    "password": "qwerty1111"
}

@app.route('/user', methods=['PUT'])
@exception_handle
def update_user():

    users = decode_json_users()
    data = request.get_json()
    uuid = data['uuid']
    nickname = data['nickname']
    password = data['password']

    success = False

    for u in users:
        if compare_uuid(u.uuid, uuid):
            users.remove(u)
            success = True

    if(success):
        users += [User(uuid, nickname, password)]
        encode_json_users(users)
        return jsonify({'response':'user updated'})

    return jsonify({'response':'no such account'})

# удаление аккаунта
# пример тела запроса:
{
    "uuid": "1993a02c-9179-4add-b892-b09580674a12"
}

@app.route('/user', methods=['DELETE'])
@exception_handle
def delete_user():

    users = decode_json_users()
    data = request.get_json()
    uuid = data['uuid']

    success = False

    for u in users:
        if compare_uuid(u.uuid, uuid):
            users.remove(u)
            success = True

    if success:
        encode_json_users(users)
        return jsonify({'response':'user deleted'})

    return jsonify({'response':'no such account'})


# функции отвечающие за запросы к публикациям
############################################################################


# добаление публикации
# пример тела запроса:
{
    "header":"damn Italy is nice place",
    "text": "shrimp pizza is awful tho"
}

@app.route('/post', methods=['POST'])
@exception_handle
def add_post():

    posts = decode_json_posts()
    data = request.get_json()
    header = data['header']
    text = data['text']

    post = Post(generate_uuid(), header, text)
    posts += [post]
    encode_json_posts(posts)

    return jsonify({'response':'success'})

# получение публикации
# пример тела запроса:
@app.route('/post', methods=['GET'])
@exception_handle
def get_post():

    posts = decode_json_posts()
    data = request.get_json()
    uuid = data['uuid']
    
    for p in posts:
        if(compare_uuid(p.uuid, uuid)):
            return jsonify({'uuid':p.uuid, 'header': p.header, 'text': p.text})

    return jsonify({'response':'post not found'})


# получение всех публикаций

@app.route('/all_posts', methods=['GET'])
@exception_handle
def all_posts():

    posts = decode_json_posts()
    data = []
    for p in posts:
        data += [{'uuid': p.uuid, 'header': p.header, 'text': p.text}]

    return jsonify(data)

    
# изменение публикации
# пример тела запроса (uuid вставить какой сгенерировался, когда создали пост):
{
    "uuid": "a8325b2a-2fa7-4d93-a179-4d3394471a80", 
    "header": "damn Italy is nice place", 
    "text": "shrimp pizza is awful tho UPD banana pizza too"
}

@app.route('/post', methods=['PUT'])
@exception_handle
def update_post():

    posts = decode_json_posts()
    data = request.get_json()
    uuid = data['uuid']
    header = data['header']
    text = data['text']

    success = False

    for p in posts:
        if compare_uuid(p.uuid, uuid):
            posts.remove(p)
            success = True

    if(success):
        posts += [Post(uuid, header, text)]
        encode_json_posts(posts)
        return jsonify({'response':'post updated'})

    return jsonify({'response':'no such post'})


# удаление публикации
# пример тела запроса (uuid вставить какой сгенерировался, когда создали пост):
{
    "uuid": "a8325b2a-2fa7-4d93-a179-4d3394471a80"
}

@app.route('/post', methods=['DELETE'])
@exception_handle
def delete_post():

    posts = decode_json_posts()
    data = request.get_json()
    uuid = data['uuid']

    success = False

    for p in posts:
        if compare_uuid(p.uuid, uuid):
            posts.remove(p)
            success = True

    if success:
        encode_json_posts(posts)
        return jsonify({'response':'post deleted'})

    return jsonify({'response':'no such post'})


# пинг
@app.route('/ping', methods=['GET'])
@exception_handle
def ping():
    return jsonify({'response':'pong'})


if __name__ == '__main__':

    app.run(debug=True)



