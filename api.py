import requests

url = "https://api.geoapify.com/v1/geocode/search?text=38%20Upper%20Montagu%20Street%2C%20London%20W1H%201LJ%2C%20United%20Kingdom&format=json&apiKey=50ad96accad1408592932b5061e1bc1e"
          
response = requests.get(url)
print(response.json())
