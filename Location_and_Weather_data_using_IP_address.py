import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

def get_public_ip():
    try:
        # Query an external service to get the public IP
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()  # Raise an error for HTTP issues
        ip_data = response.json()
        return ip_data["ip"]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

public_ip = get_public_ip()
print(f"Your computer public IP address is: {public_ip}")

def locate():
    
    url = f"http://ip-api.com/json/{public_ip}?fields=city,lat,lon"

    responce = requests.get(url)
    located_list = responce.json()
    print (located_list)
    return located_list
located_list =locate()

def get_weather():
    url = f"https://www.timeanddate.com/weather/pakistan/{located_list['city']}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    #print(soup.prettify())

    weather_date = soup.find('table',class_ = 'table table--left table--inner-borders-rows')
    if weather_date:
        rows = weather_date.find_all("tr")
        weather_data = []
        for row in rows:
            cols = row.find_all(['th' , 'td'])
            weather_data.append([col.get_text(strip=True)for col in cols])
        print (tabulate(weather_data, headers="firstrow", tablefmt="grid"))

    else:
        print("sorry")


get_weather()

