from requests import get, post, delete, put

print(get('http://localhost:5000/api/v2/jobs').json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs/999').json())  # Ошибочные запросы
print(get('http://localhost:5000/api/v2/jobs/WWWWWW').json())  # Ошибочные запросы
print(post('http://localhost:5000/api/v2/jobs', json={}).json())  # Ошибочные запросы
print(post('http://localhost:5000/api/v2/jobs', json={'title': 'Заголовок'}).json())  # Ошибочные запросы
print(post('http://localhost:5000/api/v2/jobs', json={
    'team_leader': 1,
    'job': 'Разработка программного обеспечения марсохода',
    'work_size': 20,
    'collaborators': '2, 4',
    'is_finished': False
}).json())
print(delete('http://localhost:5000/api/v2/jobs/6').json())
print(delete('http://localhost:5000/api/v2/jobs/999').json())  # Ошибочные запросы
print(delete('http://localhost:5000/api/v2/jobs/WWWW').json())  # Ошибочные запросы
print(get('http://localhost:5000/api/v2/jobs').json())


print(put('http://localhost:5000/api/v2/jobs/2', json={
    'team_leader': 3,
    'job': 'Разработка обеспечения марсохода',
    'work_size': 20,
    'collaborators': '2',
    'is_finished': True
}).json())
