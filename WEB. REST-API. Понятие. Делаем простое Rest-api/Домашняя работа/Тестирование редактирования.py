from requests import put, get

# коректный запрос
print(put('http://localhost:5000/api/jobs/2', json={
    'team_leader': 3,
    'job': 'Prepare food and bag for module 1 and 4',
    'work_size': 1,
    'collaborators': '1, 4',
    'start_date': None,
    'end_date': None,
    'is_finished': False}).json())
# некоректный запрос
print(put('http://localhost:5000/api/jobs/2', json={
    'team_leader': 3,
    'job': 'Prepare food and bag for module 1 and 4',
    'work_sizeeeesssssssssssssssssss': 1,
    'collaborators': '1, 4',
    'start_date': None,
    'end_date': None,
    'is_finished': False}).json())
# некоректный запрос
print(put('http://localhost:5000/api/jobs/999999999999', json={
    'team_leader': 3,
    'job': 'Prepare food and bag for module 1 and 4',
    'work_size': 1,
    'collaborators': '1, 4',
    'start_date': None,
    'end_date': None,
    'is_finished': False}).json())
# некоректный запрос
print(put('http://localhost:5000/api/jobs/2', json={
    'team_leader': 3,
    'job': 'Prepare food and bag for module 1 and 4',
}).json())
print('Все работы')
print(get('http://localhost:5000/api/jobs').json())
