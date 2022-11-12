from cmath import cos, sqrt
from math import pi

def find_distance(latx: float, lonx: float, laty: float, lony: float) -> float:
    """
    Finds the distance between two points x and y.
    """
        
    dlat = abs((latx - laty) * pi / 180)
    dlon = abs((lonx - lony) * pi / 180)
    alat = abs((latx + laty) / 2 * pi / 180)
    x = dlon * cos(alat)
    d = sqrt((x ** 2) + (dlat ** 2)) * 3958.8
    return d.real


def calculate_aqi(pm: float) -> int:
    """
    Calculates the AQI given the value of PM2.5.
    """
    if 0.0 <= pm < 12.1:
        percentage = pm / 12
        aqi = round(percentage * 50)
        return int(aqi)
    elif 12.1 <= pm < 35.5:
        percentage = (pm - 12.1) / 23.3
        aqi = round(percentage * 49) + 51
        return int(aqi)
    elif 35.5 <= pm < 55.5:
        percentage = (pm - 35.5) / 19.9
        aqi = round(percentage * 49) + 101
        return int(aqi)
    elif 55.5 <= pm < 150.5:
        percentage = (pm - 55.5) / 94.9
        aqi = round(percentage * 49) + 151
        return int(aqi)
    elif 150.5 <= pm < 250.5:
        percentage = (pm - 150.5) / 99.9
        aqi = round(percentage * 99) + 201
        return int(aqi)
    elif 250.5 <= pm < 350.5:
        percentage = (pm - 250.5) / 99.9
        aqi = round(percentage * 99) + 301
        return int(aqi)
    elif 350.5 <= pm < 500.5:
        percentage = (pm - 350.5) / 149.9
        aqi = round(percentage * 99) + 401
        return int(aqi)
    elif 500.5 <= pm:
        return 501
