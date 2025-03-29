from requests import post, get

# коректный запрос
print('Коректный запрос')
print(post('http://localhost:5000/api/jobs', json={
    'team_leader': 3,
    'job': 'Prepare food for module 1 and 2',
    'work_size': 6,
    'collaborators': '3, 4',
    'start_date': None,
    'end_date': None,
    'is_finished': False}).json())
print('Некоректные запросы')
print(post('http://localhost:5000/api/jobs', json={}).json())  # пустой json
print(post('http://localhost:5000/api/jobs', json={'team_leader': 3}).json())  # не заполнены все нужные поля json
print(post('http://localhost:5000/api/jobs', json={
    'team_leader': 3,
    'job': 'Prepare food for module 1 and 2',
    'work_sizeees': 6,
    'collaborators': '3, 4',
    'start_date': None,
    'end_date': None,
    'is_finished': False}).json())  # Неправильное название колонки work_size
print('Работы после изменений')
print(get('http://localhost:5000/api/jobs').json())