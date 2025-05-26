import math, re, sys
from numpy import *

# usage: python TSPwP-verifier.py inputfilename solutionfilename

def main(instancefile, solutionfile):
    penalty,cities = readinstance(instancefile)
    solution = readsolution(solutionfile)
    checksolution(cities,penalty,solution)


def distance(a, b):
    # a and b are integer pairs (each representing a point in a 2D, integer grid)
    # Euclidean distance rounded to the nearest integer:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return (round(math.sqrt(dx * dx + dy * dy)))


def readinstance(filename):
    #The first line specifies the fixed penalty for not visiting a city, which applies equally to all cities.
    # each subsequent line of input file represents a city given by three integers:
    # identifier x-coordinate y-coordinate (space separated)
    # city identifiers are always consecutive integers starting with 0
 
    with open(filename, 'r') as f:
        # read the fixed penalty 
        penalty = int(f.readline().strip())

        cities = []
        line = f.readline()
        while len(line.strip()) > 0:
            lineparse = re.findall(r'[^,;\s]+', line)
            cities.append([int(lineparse[1]), int(lineparse[2])])
            line = f.readline()

    return [penalty,cities]


def readsolution(filename):
    # The first line should contain two values: 
    # the total length of the tour plus penalties, and the number of cities visited,
    # The next lines must list the city IDs in the order they are visited in the tour.
    # The final line of the output file should be left blank.
    # each city is listed once
    # cities are identified by integers from 0 to n-1
 
    with open(filename, 'r') as file:
        # Read the first line and extract the total tour length and number of cities
        first_line = file.readline().strip()  
        parts = first_line.split()  
        # The first line should contain two numbers
        if len(parts) == 2:
            tot_tour_length_plus_penalty = int(parts[0]) # First value: total tour length
            city_count = int(parts[1])  # Second value: number of cities
        else:
            print("Invalid data format: The first line must contain two numbers.")
            quit()

        # Read the city visit order
        cityorder = []
        for line in file:
            line = line.strip()  
            if line: 
                cityorder.append(int(line)) # Add city IDs to the list

    return [tot_tour_length_plus_penalty,city_count,cityorder]

def checkduplicate(cityorder):
    if len(cityorder) != len(set(cityorder)):
        print('ERROR: Invalid tour – duplicate city indices found')
        exit()

def checkinvalid(n,cityorder):
    if not set(cityorder).issubset(set(range(n))):
        print('ERROR: Invalid tour – contains invalid city indices')
        exit()

def checktourInfo(cities, penalty,tour_length_wP,citycount,cityorder):

    # calculate the length of the tour given by the salesman:
    tot_tour_length = 0
    for i in range(len(cityorder)):
        tot_tour_length = tot_tour_length + distance(cities[cityorder[i]], cities[cityorder[i - 1]])
   
    #unvisited city num
    unvisited_citynum = len(cities) - len(cityorder)
    #total tour length plus penalties
    computed_tour_length_wP = tot_tour_length + unvisited_citynum*penalty
    #visited city num
    computed_citycount = len(cityorder)
    
    #check solution
    if(computed_tour_length_wP == tour_length_wP and computed_citycount == citycount):
        print('Your solution is VERIFIED. ')
    
    else:
        #check total tour length plus penalties penalty
        if(computed_tour_length_wP != tour_length_wP):
            print('Your solution is NOT VERIFIED.')
            print('The total tour length  is given as ', tour_length_wP)
            print('but computed as ', computed_tour_length_wP)
        if(computed_citycount != citycount):
            print('Your solution is NOT VERIFIED.')
            print('The city count is given as ', citycount)
            print('but computed as ', computed_citycount)
        exit()


def checksolution(cities,penalty,solution):
    #total city num
    n = len(cities)
    #tour legnth with penalty
    tour_length_wP = solution[0]
    #city_count in the tour
    citycount = solution[1]
    #city order
    cityorder = solution[2]


    # check total city num
    if (len(cityorder) > n):
        print('ERROR: Total city num does not match')
        exit();
    else:
        checkinvalid(n,cityorder)
        checkduplicate(cityorder)
        checktourInfo(cities, penalty,tour_length_wP,citycount,cityorder)
    
main(sys.argv[1], sys.argv[2])
#main('example-input-3.txt', 'example-output-3.txt')
