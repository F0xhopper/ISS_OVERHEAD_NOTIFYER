import requests
from datetime import datetime
import smtplib
import time
MY_LAT = 51.507351 
MY_LONG = -0.127758 
MY_EMAIL = 'your email'
MY_PASSWORD = 'your email app pass'




parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

def check_conditions_and_send_email():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])
    if MY_LAT >= iss_latitude + 5 and MY_LAT <= iss_latitude - 5 and MY_LONG >= iss_longitude + 5 and MY_LONG <= iss_longitude - 5:
        sunrise_sunset_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        sunrise_sunset_response.raise_for_status()
        sunrise_sunset_data = sunrise_sunset_response.json()
        sunrise = int(sunrise_sunset_data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(sunrise_sunset_data["results"]["sunset"].split("T")[1].split(":")[0])
        current_hour = datetime.now().hour
        if current_hour >= sunset or current_hour <= sunrise:
              with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL,password=MY_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,to_addrs=MY_EMAIL,msg=f'Subject:Look up\n\nQuick look up the ISS is overhead!!!')
      
        
            



while True:
    check_conditions_and_send_email()
    time.sleep(60) 

