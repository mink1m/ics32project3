import json
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
import calculations


class Center_from_name_with_file:
    """
    Name to coordinates given a file.
    """
    def __init__(self, pathstr: str) -> None:
        self._stringpath = pathstr
        self._path = Path(pathstr)
    def get_coordinates(self) -> list:
        try:
            p = self._path.open('r')
            filecontent = p.read()
            p.close()
            json_dict = json.loads(filecontent)[0]
            coordinates = []
            coordinates.append(json_dict['lat'])
            coordinates.append(json_dict['lon'])
            return coordinates
        except:
            print("FAILED")
            try:
                f = open(self._stringpath, 'r')
                print(self._stringpath)
                print("FORMAT")
            except:
                print(self._stringpath)
                print("MISSING")
            finally:
                raise ValueError


class Center_from_name_with_api:
    """
    Name to coordinates given location description.
    """
    def __init__(self, location: str) -> None:
        self._base = "https://nominatim.openstreetmap.org/search?"
        self._location = location
    def get_coordinates(self) -> None:
        try:
            q = urllib.parse.urlencode([('q', str(self._location)), ('format', 'json'), ('Referer', "https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/minhak6")])
            url = self._base + q
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')
            json_dict = json.loads(json_text)[0]
            coordinates = []
            coordinates.append(json_dict['lat'])
            coordinates.append(json_dict['lon'])
            return coordinates
        except urllib.error.HTTPError as err:
            print("FAILED")
            try:
                status_code = err.code
                print(f"{status_code} {url}")
                if str(status_code) == "200":
                    print("FORMAT")
                else:
                    print("NOT 200")
            except:
                print(url)
                print("NETWORK")
            finally:
                raise ValueError
        except:
            print('unexpected!!!')
            


class AQI_from_file:
    """
    Finds the AQI values given range, threshold, and max from a file.
    """
    def __init__(self, pathstr: str, latgiven: float, longiven: float, range: int, threshold: int, max: int) -> None:
        self._stringpath = pathstr
        self._path = Path(pathstr)
        self._range = range
        self._threshold = threshold
        self._max = max
        self._lat = latgiven
        self._lon = longiven
    def get_list(self) -> list:
        try:
            p = self._path.open('r')
            filecontent = p.read()
            p.close()
            json_dict = json.loads(filecontent)
            in_range = []
            for item in json_dict['data']:
                try:
                    pm = item[1]
                    age = item[4]
                    lat = item[27]
                    lon = item[28]
                    aqi = calculations.calculate_aqi(pm)
                    indooroutdoor = item[25]
                    distance = calculations.find_distance(self._lat, self._lon, lat, lon)
                    if distance <= float(self._range) and indooroutdoor == 0 and aqi >= self._threshold and age < 3600:
                        item.append(aqi)
                        in_range.append(item)
                except:
                    pass
            in_range.sort(key = lambda x:float(x[1]), reverse=True)
            range_with_max = in_range[:self._max]
            return range_with_max
        except:
            print("FAILED")
            try:
                f = open(self._stringpath, 'r')
                print(self._stringpath)
                print("FORMAT")
            except:
                print(self._stringpath)
                print("MISSING")
            finally:
                raise ValueError




class AQI_from_api:
    def __init__(self, latgiven: float, longiven: float, range: int, threshold: int, max: int) -> None:
        self._url = "https://www.purpleair.com/data.json"
        self._range = range
        self._threshold = threshold
        self._max = max
        self._lat = latgiven
        self._lon = longiven
    def get_list(self) -> list:
        try:
            request = urllib.request.Request(self._url)
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')
            json_dict = json.loads(json_text)
            in_range = []
            for item in json_dict['data']:
                try:
                    pm = item[1]
                    age = item[4]
                    lat = item[27]
                    lon = item[28]
                    aqi = calculations.calculate_aqi(pm)
                    indooroutdoor = item[25]
                    distance = calculations.find_distance(self._lat, self._lon, lat, lon)
                    if distance <= float(self._range) and indooroutdoor == 0 and aqi >= self._threshold and age < 3600:
                        item.append(aqi)
                        in_range.append(item)
                except:
                    pass
            in_range.sort(key = lambda x:float(x[1]), reverse=True)
            range_with_max = in_range[:self._max]
            return range_with_max
        except urllib.error.HTTPError as err:
            print("FAILED")
            try:
                status_code = err.code
                print(f"{status_code} {self._url}")
                if str(status_code) == "200":
                    print("FORMAT")
                else:
                    print("NOT 200")
            except:
                print(self._url)
                print("NETWORK")
            finally:
                raise ValueError
        except:
            print('unexpected!!!')         


class Reverse_from_file:
    def __init__(self, paths: str) -> None:
        self._stringpath = paths
        self._path = paths
    def reverse(self, lat: float, lon: float) -> str:
        try:
            path = Path(self._path)
            p = path.open('r')
            filecontent = p.read()
            p.close()
            json_dict = json.loads(filecontent)
            if abs(float(lat) - float(json_dict['lat'])) < .0005 and abs(float(lon) - float(json_dict['lon'])) <.0005:
                return json_dict['display_name']
        except:
            print("FAILED")
            try:
                f = open(self._stringpath, 'r')
                print(self._stringpath)
                print("FORMAT")
            except:
                print(self._stringpath)
                print("MISSING")
            finally:
                raise ValueError

class Reverse_from_api:
    def __init__(self) -> None:
        self._base = "https://nominatim.openstreetmap.org/reverse?"
    def reverse(self, lat:float, lon: float) -> str:
        try:
            q = urllib.parse.urlencode([('lat', str(lat)), ('lon', str(lon)), ('format', 'json'), ('Referer', "https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/minhak6")])
            url = self._base + q
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')
            json_dict = json.loads(json_text)
            if abs(float(lat) - float(json_dict['lat'])) < .0005 and abs(float(lon) - float(json_dict['lon'])) <.0005:
                return json_dict['display_name']
        except urllib.error.HTTPError as err:
            print("FAILED")
            try:
                status_code = err.code
                print(f"{status_code} {url}")
                if str(status_code) == "200":
                    print("FORMAT")
                else:
                    print("NOT 200")
            except:
                print(url)
                print("NETWORK")
            finally:
                raise ValueError
        except:
            print('unexpected!!!')        
