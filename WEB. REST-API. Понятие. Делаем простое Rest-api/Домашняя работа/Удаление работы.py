from requests import delete

# коректный запрос
print(delete('http://localhost:5000/api/jobs/1').json())
