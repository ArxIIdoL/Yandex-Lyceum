from requests import post

print(post('http://localhost:5000/api/jobs', json={
    'team_leader': 1,
    'job': 'Prepare food for module 2 and 3',
    'work_size': 3,
    'collaborators': '2, 4',
    'start_date': None,
    'end_date': None,
    'is_finished': True}).json())
