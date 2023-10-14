import csv
import re
import math

new_list1 = []

with open('offices.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        new_list1.append(row['latitude'])
        new_list1.append(row['longitude'])
        

def remove_empty_values(lst):
    new_list = [value for value in lst if re.search(r'\d', value)]
    return new_list
lst = new_list1
new_lst = remove_empty_values(lst)
#print(new_lst)

new_lst = list(map(float, new_lst))
#print(new_lst)
    

def split_list(lst):
    tuple_list = [(lst[i], lst[i+1]) for i in range(0, len(lst), 2)]
    return tuple_list

tuple_list = split_list(new_lst)
#print((tuple_list))

######

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6378.1
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance


def sort_coordinates(input_lat, input_lon, coordinates):
    sorted_coordinates = sorted(coordinates, key=lambda coord: calculate_distance(input_lat, input_lon, coord[0], coord[1]))
    return sorted_coordinates


input_lat = 55.7522  
input_lon = 37.6156 

sorted_coordinates = sort_coordinates(input_lat, input_lon, tuple_list)
print(sorted_coordinates)
