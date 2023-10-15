import csv
import re
import math

new_list1 = []
list_for_rko = []
list_for_kep = []

input_lat = 55.7522  
input_lon = 37.6156 

with open('offices.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        new_list1.append(row['latitude'])
        new_list1.append(row['longitude'])
        
        list_for_rko.append(row['rko'])
        
        list_for_kep.append(row['kep'])
        
#print(list_for_rko)       
#print(list_for_kep) 
        

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
#print(len(tuple_list))
tuple_list1 = []
for i in tuple_list:
    tuple_list1.append(i)
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



sorted_coordinates = sort_coordinates(input_lat, input_lon, tuple_list)
#print(sorted_coordinates)

######
list_for_rko = list(filter(None, list_for_rko))
#print(len(list_for_rko))

list_for_kep = list(filter(None, list_for_kep))
#print(len(list_for_kep))


def remove_elements(first_list, second_list, value):
    indices_to_remove = [i for i, element in enumerate(second_list) if element == value]
    for index in reversed(indices_to_remove):
        del first_list[index]
    return first_list

first_list = tuple_list
second_list = list_for_rko
value_to_remove = 'нет РКО'

new_list = remove_elements(first_list, second_list, value_to_remove)

sorted_coordinates_rko = sort_coordinates(input_lat, input_lon, new_list)
print(len(sorted_coordinates_rko))

######

def remove_elements1(first_list, second_list, value, value1):
    indices_to_remove = [i for i, element in enumerate(second_list) if element == value or element == value1]
    for index in reversed(indices_to_remove):
        del first_list[index]
    return first_list

first_list = tuple_list1
second_list = list_for_kep
value_to_remove = 'null'
value_to_remove1 = 'False'

new_list = remove_elements1(first_list, second_list, value_to_remove, value_to_remove1)

sorted_coordinates_kep = sort_coordinates(input_lat, input_lon, new_list)

print(len(sorted_coordinates_kep))


