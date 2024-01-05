from model.post import Post
from model.user import User
from pprint import pprint

import json

from utilities.functions \
import compare_uuid, generate_uuid, encode_json_users, encode_json_posts, \
decode_json_users, decode_json_posts, user_to_str, post_to_str


users = []
posts = []

# тест добавление пользователей

# user1 = User(generate_uuid(), 'john1', 'qwerty321')
# user2 = User(generate_uuid(), 'bruh', 'qqqqq')
# user3 = User(generate_uuid(), 'tom', 'qwerty')

# users += [user1]
# users += [user2]
# users += [user3]

# encode_json_users(users)

# Тест удаление

# users = decode_json_users()

# for x in users:
#     print(user_to_str(x))

# print()

# for u in users:
#         if compare_uuid(u.uuid, 'a196271a-473f-44fa-b3fe-7939f42abc17'):
#             users.remove(u)

# for x in users:
#     print(user_to_str(x))

# encode_json_users(users)



# Тест изменение пользователя


users = decode_json_users()

for x in users:
    print(user_to_str(x))

print()

uuid = '3d980910-0462-40ff-98b3-cbc04f73bca6'
nickname = 'john1'
password = 'qwerty321'

for u in users:
    if compare_uuid(u.uuid, uuid):
        users.remove(u)
        users += [User(uuid, nickname, password)]
        print({'response':'user updated'})

for x in users:
    print(user_to_str(x))

encode_json_users(users)