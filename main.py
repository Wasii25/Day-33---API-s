import time

import requests
from datetime import datetime
import smtplib

my_lat = 13.024182
my_lon = 77.714661

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json#")
    response.raise_for_status()
    data = response.json()

    iss_lat = float(data["iss_position"]["latitude"])
    iss_lon = float(data["iss_position"]["longitude"])
    if my_lat - 5 <= iss_lat <= my_lat + 5 and my_lon - 5 <= iss_lon <= my_lon + 5:
        return True


def is_night():
    parameters = {
        "lat": my_lat,
        "long": my_lon,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split('T')[1].split(":"))
    sunset = int(data["results"]["sunset"].split('T')[1].split(":"))

    time_now = datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


my_email = input("Enter your email:")
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            result = connection.login(my_email, "mdnl ciaz gbvh mrre")
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg="Subject: Look Up!\n\n The ISS is above you in the sky.",
            )