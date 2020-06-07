#go to openweathermap's official website and register for free for your own appid and then put it after the 'appid='
import requests

weatherApiAddress = 'https://api.openweathermap.org/data/2.5/weather?appid=070f601ac897b008a3ae6d4c310e1244&q='

cityName = input('enter city : ')
url = weatherApiAddress + cityName
jsonData = requests.get(url).json()

print(jsonData)
print('for {},we can see {} and the temperature is {} degree celsius'.format(cityName,jsonData['weather'][0]['description'],int(jsonData['main']['temp'] - 273.15)))
