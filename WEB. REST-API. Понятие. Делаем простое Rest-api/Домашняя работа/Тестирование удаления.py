from requests import delete

# коректный запрос
print(delete('http://localhost:5000/api/jobs/2').json())
# некоректный запрос
print(delete('http://localhost:5000/api/jobs/999999999').json())
# некоректный запрос
print(delete('http://localhost:5000/api/jobs/uuuuuu').json())
