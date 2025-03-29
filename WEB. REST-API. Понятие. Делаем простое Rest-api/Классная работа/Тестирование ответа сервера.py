from requests import get

print('Все работы')
print(get('http://localhost:5000/api/jobs').json())  # Получение всех работ
print('Работа номер 2')
print(get('http://localhost:5000/api/jobs/2').json())  # Работа номер 2
print('-------------------')
print(get('http://localhost:5000/api/jobs/999').json())  # Ошибка id
print('-------------------')
print(get('http://localhost:5000/api/jobs/id').json())  # Ошибка
