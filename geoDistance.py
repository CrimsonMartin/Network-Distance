import socket
from math import acos, cos, sin, fabs

#places we're testing
target_file = "targets.txt"
#the public ip from case
case_ip = '129.22.12.21'

def main():
    global target_file
    targets = open(target_file, 'r')

    for line in targets:
        host_name = line.split()[0]

        compute_geo_distance(host_name)
        print("")

    targets.close()

#gets the latitude and longitude of the input ip address
# learned this from https://pypi.org/project/geoip2/
def get_geo_coordinates(ip):
    import geoip2.database
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    lat = lon = 99
    try:
        lat = reader.city(ip).location.latitude
        lon = reader.city(ip).location.longitude
    except geoip2.errors.AddressNotFoundError:
        print("address %s not found in db" % ip)
    finally:
        reader.close()
    return lat,lon

#copied from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
#asks for my ip from google's DNS server
def my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    num = s.getsockname()[0]
    s.close()
    return num

#taken from https://www.w3resource.com/python-exercises/math/python-math-exercise-27.php
#not sure how it works
def haversine(lat, lon, dest_lat, dest_lon):
    lat_int = int(lat)
    lon_int = int(lon)
    dest_lat_int = int(dest_lat)
    dest_lon_int = int(dest_lon)

    return 6371.01 * acos(sin(lat_int)*sin(dest_lat_int) + cos(lat_int)*cos(dest_lat_int)*cos(lon_int - dest_lon_int))


def compute_geo_distance(host_name):
    host_ip = socket.gethostbyname(host_name)
    global case_ip
    direct_ip = my_ip()

    print("dest host name: [%s] dest ip: [%s]" % (host_name, host_ip))

    dest_lat, dest_lon = get_geo_coordinates(host_ip)
    direct_lat, direct_lon = get_geo_coordinates(direct_ip)
    indirect_lat, indirect_lon = get_geo_coordinates(case_ip)

    print("Cle: (%s, %s) dest: (%s, %s) me: (%s, %s)" % (indirect_lat, indirect_lon, dest_lat, dest_lon, direct_lat, direct_lon))

    if direct_lat == 99 and direct_lon == 99:
        print ("direct distance not computed")

    else:
        dist = haversine(direct_lat, direct_lon, dest_lat, dest_lon)
        print("direct distance: %.2fkm." % dist)

    in_dist =  haversine(indirect_lat, indirect_lon, dest_lat, dest_lon)
    print("indirect distance: %.2fkm." % in_dist)

#calls main function
if __name__ == "__main__":
    main()
