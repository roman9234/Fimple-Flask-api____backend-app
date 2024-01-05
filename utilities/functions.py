import uuid, json
from model.post import Post
from model.user import User

def compare_uuid(uuid1, uuid2):
    return uuid1 == uuid2

def generate_uuid():
    return str(uuid.uuid4())

def user_to_str(user : User):
    return user.uuid +' '+ user.nickname +' '+ user.password

def post_to_str(post : Post):
    return post.uuid +' '+ post.header +' '+ post.text

def encode_json_users(users):
    data = []
    for u in users:
        user = {
            'uuid':u.uuid,
            'nickname':u.nickname,
            'password':u.password
        }
        data += [user]
    with open("data/users.json", "w") as users_file:
        json.dump(data, users_file)

def encode_json_posts(posts):
    data = []
    for p in posts:
        post = {
            'uuid':p.uuid,
            'header':p.header,
            'text':p.text
        }
        data += [post]
    with open("data/posts.json", "w") as posts_file:
        json.dump(data, posts_file)

def decode_json_users():
    with open("data/users.json") as users_file:
        data = json.load(users_file)
        output = []
        for x in data:
            u = User(x['uuid'], x['nickname'], x['password'])
            output += [u]
        return output

def decode_json_posts():
    with open("data/posts.json") as posts_file:
        data = json.load(posts_file)
        output = []
        for x in data:
            p = Post(x['uuid'], x['header'], x['text'])
            output += [p]
        return output


        