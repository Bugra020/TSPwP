import math
import random


def distance(a, b):
    dx = a[1] - b[1]
    dy = a[2] - b[2]
    return math.floor(math.hypot(dx, dy))


def greedy_tour(cities):
    unvisited = set(range(1, len(cities)))
    tour = [cities[0]]
    current = cities[0]

    city_dict = {city[0]: city for city in cities}

    while unvisited:
        min_dist = float("inf")
        next_id = None
        for i in unvisited:
            dist = distance(current, city_dict[i])
            if dist < min_dist:
                min_dist = dist
                next_id = i

        current = city_dict[next_id]
        tour.append(current)
        unvisited.remove(next_id)

    tour.append(tour[0])
    return tour


def calc_cost(route):
    total_cost = 0
    n = len(route)
    for i in range(n):
        if route[i][0] == -1:
            total_cost += route[i][3]
            continue
        if i == n - 1:
            total_cost += distance(route[0], route[i])
        else:
            total_cost += distance(route[i], route[i + 1])

    return total_cost


def check_penalty(route):
    for i in range(0, len(route) - 3):
        if (
            distance(route[i], route[i + 1]) + distance(route[i + 1], route[i + 2])
        ) > distance(route[i], route[i + 2]) + route[i + 1][3]:
            route[i + 1][0] = -1

    return route

def check_penalty2(route):
    for i in range(0,len(route)-5):
        if( 
            distance(route[i],route[i+1]) + distance(route[i+1],route[i+2]) + distance(route[i+2],route[i+3])+distance(route[i+3],route[i+4])
        ) > distance(route[i],route[i+4]) + route[i+1][3] + route[i+2][3] + route[i+3][3]:
            route[i+1][0] = -1
            route[i+2][0] = -1
            route[i+3][0] = -1

    return route

def new_route(route):
    new_route = []
    for city in route:
        if city[0] != -1:
            new_route.append(city)

    return new_route


def swap_improve(route):
    best = route[:]
    best_cost = calc_cost(best)
    n = len(best)

    for _ in range(int(math.pow(len(route), 2) / 50)):
        i = random.randint(1, n - 3)
        k = random.randint(i + 1, n - 2)

        if best[i][0] == -1 or best[k][0] == -1:
            continue

        new_route = best[:i] + best[i : k + 1][::-1] + best[k + 1 :]
        new_cost = calc_cost(new_route)

        if new_cost < best_cost:
            best = new_route
            best_cost = new_cost
    
    return best


def solve(cities):
    route = greedy_tour(cities)
    route = swap_improve(route)
    for _ in range(0, 3):
        route = check_penalty(route)
        route = check_penalty2(route)
        route = new_route(route)
        route = swap_improve(route)

    return route, calc_cost(route)
