import datetime, requests, json, config
from geopy.geocoders import Nominatim

def get_date():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y")

def get_coordinates(city):
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(city)
    return location.latitude, location.longitude

def get_timetable():
    lat, lon = get_coordinates(config.city)
    response = requests.get(f"http://api.aladhan.com/v1/timings/{get_date()}?latitude={lat}&longitude={lon}&method=3")
    data = response.json()
    if response.status_code == 200:
        return data
    return f"An error occurred: status code {response.status_code}"

def clock_emoji(time_str):
    hour = int(time_str.split(':')[0]) % 12
    minute = int(time_str.split(':')[1])

    if 15 <= minute < 45:
        return {
            0: "🕧", 1: "🕜", 2: "🕝", 3: "🕞", 4: "🕟", 5: "🕠",
            6: "🕡", 7: "🕢", 8: "🕣", 9: "🕤", 10: "🕥", 11: "🕦", 12: "🕧"
        }.get(hour if hour else 12, "🕛")
    return {
        0: "🕛", 1: "🕐", 2: "🕑", 3: "🕒", 4: "🕓", 5: "🕔",
        6: "🕕", 7: "🕖", 8: "🕗", 9: "🕘", 10: "🕙", 11: "🕚", 12: "🕛"
    }.get(hour if hour else 12, "🕛")


def format_time(label, time):
    return f"{clock_emoji(time)} {label}: {time}"


def parse_data():
    data = get_timetable()
    timings = data['data']['timings']
    date_gregorian = data['data']['date']['gregorian']
    date_hijri = data['data']['date']['hijri']

    g_day = date_gregorian['day']
    g_month = date_gregorian['month']['en']
    g_year = date_gregorian['year']

    h_day = date_hijri['day']
    h_month = date_hijri['month']['en']
    h_year = date_hijri['year']

    return (
        f"🇬🇧 **Prayer Times**\n"
        f"──────────────────────\n"
        f"🗓️ {g_day} {g_month} {g_year}\n"
        f"🕋 {h_day} {h_month} {h_year}\n\n"
        f"{format_time('Fajr', timings['Fajr'])}\n"
        f"{format_time('Sunrise', timings['Sunrise'])}\n"
        f"{format_time('Dhuhr', timings['Dhuhr'])}\n"
        f"{format_time('Asr', timings['Asr'])}\n"
        f"{format_time('Maghrib', timings['Maghrib'])}\n"
        f"{format_time('Isha', timings['Isha'])}\n"
        f"{format_time('Imsak', timings['Imsak'])}\n"
        f"{format_time('Midnight', timings['Midnight'])}"
    )

if __name__ == "__main__":
    print(parse_data())
