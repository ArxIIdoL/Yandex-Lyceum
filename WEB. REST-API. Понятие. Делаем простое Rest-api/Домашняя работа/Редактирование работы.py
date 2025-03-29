from requests import put

print(put('http://localhost:5000/api/jobs/5', json={
    'team_leader': 2,
    'job': 'Prepare food for module 1 and 2',
    'work_size': 15,
    'collaborators': '1, 3',
    'start_date': None,
    'end_date': None,
    'is_finished': True}).json())
