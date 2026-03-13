import math

def carCalculator(distance, speed, fuel_efficiency, tank_size):
    time = distance / speed
    fuel_used = distance / fuel_efficiency
    if fuel_used <= tank_size:
        stops = 0
    else:
        stops = math.ceil(fuel_used / tank_size) - 1
    return time, fuel_used, stops

def main():
    print('lets plan your trip!')
    distance = float(input("Please enter the distance of your destination in miles: "))
    speed = int(input("Please enter your estimated average speed in mph: "))
    fuel_efficiency = float(input("Please enter your vehicle's fuel efficiency in mpg: "))
    tank_size = float(input("Please enter your gas tank size in gallons: "))
    
    time, fuel_used, stops = carCalculator(distance, speed, fuel_efficiency, tank_size)
    
    print("Estimated travel time:", time, "hours")
    print("Estimated fuel needed:", fuel_used, "gallons")
    print("Estimated fuel stops needed:", stops)

if __name__ == "__main__":
    main()




