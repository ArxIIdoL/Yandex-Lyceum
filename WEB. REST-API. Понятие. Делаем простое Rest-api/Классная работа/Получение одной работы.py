from requests import get

print('Работа номер 2')
print(get('http://localhost:5000/api/jobs/2').json())  # Получение одной работы
