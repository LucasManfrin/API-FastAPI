import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzU4NDE3MDgwfQ.HvsPDEgL8dyEWK16uQ5qUQ_k8YkZwAJsAb-WNVKCpMc"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())