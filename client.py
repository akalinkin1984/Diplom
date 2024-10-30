import requests

# загрузка товаров
# файл https://raw.githubusercontent.com/netology-code/python-final-diplom/master/data/shop1.yaml
response = requests.post("http://localhost:8000/api/v1/partner/update",
                          headers={'Authorization': 'Token 1d052b082ffe4afa189471863729938292ae2fe7',
                                   'Content-Type': 'application/x-www-form-urlencoded'},
                          data={
                              'url': 'https://raw.githubusercontent.com/netology-code/python-final-diplom/master/data/shop1.yaml'
                                }
                          )

print(response.status_code)
print(response.json())