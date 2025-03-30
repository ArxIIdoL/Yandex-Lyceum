from requests import get, post, put, delete

print("All users")
print(get('http://localhost:5000/api/users').json())
print("User id == 2")
print(get('http://localhost:5000/api/users/2').json())
print('New user id')
print(post('http://localhost:5000/api/users', json={
    'surname': "Ivanov",
    'name': "Ivan",
    'age': 30,
    'position': "Software Developer",
    'speciality': "Software Development",
    'address': "module_2",
    'email': "ivanov@example.com",
    'password': "IVQnovSoftware"
}).json())
print("All users + Ivan")
print(get('http://localhost:5000/api/users').json())
print(put('http://localhost:5000/api/users/6', json={
    'surname': "Ivanovich",
    'name': "Ben",
    'age': 40,
    'position': "Software Developer!!!",
    'speciality': "Software Development",
    'address': "Moscow",
    'email': "bivanov@example.com",
    'password': "BIVanovSoftware"}).json())
print("All users + edit Ivan")
print(get('http://localhost:5000/api/users').json())
print("Delete Ivan")
print(delete(f'http://localhost:5000/api/users/6').json())
