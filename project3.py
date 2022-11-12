#Minha Kim
#81343818

import classes

def run() -> str:
    """
    Reads the inputs.
    """
    try:
        center_coordinates = line1()
        range = int(line2())
        threshold = int(line3())
        max = int(line4())
        aqilist = line5(center_coordinates, range, threshold, max)
        reverse_locations = line6(aqilist)
        return print_output(center_coordinates, aqilist, reverse_locations).rstrip("\n")
    except Exception as e:
        print(e)
        return


def print_output(center: list, aqilist: list, locations: list) -> str:
    output_str = ''
    output_lat = ''
    output_lon = ''
    output_lat = lat_float_to_str(center[0])
    output_lon = lon_float_to_str(center[1])
    output_str += f"CENTER {output_lat} {output_lon}\n"
    for i in range(len(aqilist)):
        output_str += f"AQI {aqilist[i][-1]}\n"
        part_lat = lat_float_to_str(aqilist[i][27])
        part_lon = lon_float_to_str(aqilist[i][28])
        output_str += f"{part_lat} {part_lon}\n"
        output_str += f"{locations[i]}\n"
    return output_str


def lat_float_to_str(coord: float) -> str:
    if float(coord) < 0:
        return f"{abs(float(coord))}/S"
    else:
        return f"{abs(float(coord))}/N"

def lon_float_to_str(coord: float) -> str:
    if float(coord) < 0:
        return f"{abs(float(coord))}/W"
    else:
        return f"{abs(float(coord))}/E"


def line1() -> list:
    """
    Reads the first line of input. (center point)
    Returns list of [lat, lon]
    """
    centerinput = str(input())
    splitinput = centerinput.split()
    if splitinput[0] == "CENTER":
        indicator = splitinput[1]
        if indicator == "NOMINATIM":
            location = splitinput[2:]
            locationstr = ''
            for i in location:
                locationstr += f"{i} "
            locationstr.rstrip()
            api = classes.Center_from_name_with_api(locationstr)
            return api.get_coordinates()
        elif indicator == "FILE":
            path = classes.Center_from_name_with_file(splitinput[2])
            return path.get_coordinates()


def line2() -> int:
    """
    Reads the second line of input. (range in miles)
    """
    rangeinput = str(input())
    splitinput = rangeinput.split()
    return int(splitinput[1])


def line3() -> int:
    """
    Reads the third line of input. (aqi threshold)
    """
    threshinput = str(input())
    splitinput = threshinput.split()
    return int(splitinput[1])


def line4() -> list:
    """
    Reads the fourth line of input. (max number of locations)
    """
    maxinput = str(input())
    splitinput = maxinput.split()
    return int(splitinput[1])


def line5(coordinates: list, range: int, threshold: int, max: int) -> list[list]:
    """
    Reads the fifth line of input. (location to find aqi)
    """
    aqiinput = str(input())
    splitinput = aqiinput.split()
    indicator = splitinput[1]
    given_lat = float(coordinates[0])
    given_lon = float(coordinates[1])
    if indicator == "PURPLEAIR":
        aqi_list = classes.AQI_from_api(given_lat, given_lon, range, threshold, max)
        return aqi_list.get_list()
    elif indicator == "FILE":
        file_path = splitinput[2]
        aqi_list = classes.AQI_from_file(file_path, given_lat, given_lon, range, threshold, max)
        return aqi_list.get_list()



def line6(list_of_locations: list) -> list:
    """
    Reads the sixth line of input. (reverses coordinates to name and vice versa)
    """
    reverseinput = str(input())
    splitinput = reverseinput.split()
    indicator = splitinput[1]
    if indicator == "NOMINATIM":
        desc_list = []
        for location in list_of_locations:
            lat = float(location[27])
            lon = float(location[28])
            reverse = classes.Reverse_from_api()
            reversed_desc = reverse.reverse(lat, lon)
            if reversed_desc != None:
                desc_list.append(reversed_desc)
        return desc_list
    elif indicator == "FILES":
        file_list = splitinput[2:]
        desc_list = []
        for file in file_list:
            for location in list_of_locations:
                lat = float(location[27])
                lon = float(location[28])
                reverse = classes.Reverse_from_file(file)
                reversed_desc = reverse.reverse(lat, lon)
                if reversed_desc != None:
                    desc_list.append(reversed_desc)
        return desc_list
