from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/4').json())
print(get('http://localhost:5000/api/v2/users/999').json())  # Ошибочные запросы
print(get('http://localhost:5000/api/v2/users/WWWWWW').json())  # Ошибочные запросы
print(post('http://localhost:5000/api/v2/users', json={}).json())  # Ошибочные запросы
print(post('http://localhost:5000/api/v2/users', json={'title': 'Заголовок'}).json())  # Ошибочные запросы
print(post('http://localhost:5000/api/v2/users', json={
    'surname': "Ivanov",
    'name': "Ivan",
    'age': 30,
    'position': "Software Developer",
    'speciality': "Software Development",
    'address': "module_2",
    'email': "ivanov@example.com",
    'password': "IVQnovSoftware"
}).json())
print(delete('http://localhost:5000/api/v2/users/6').json())
print(delete('http://localhost:5000/api/v2/users/999').json())  # Ошибочные запросы
print(delete('http://localhost:5000/api/v2/users/WWWW').json())  # Ошибочные запросы
print(get('http://localhost:5000/api/v2/users').json())
