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
        next_id = min(unvisited, key=lambda i: distance(current, city_dict[i]))
        current = city_dict[next_id]
        tour.append(current)
        unvisited.remove(next_id)

    tour.append(tour[0])
    return tour


def calc_cost(route):
    total_cost = 0
    n = len(route)
    for i in range(n):
        if i == n - 1:
            total_cost += distance(route[0], route[i])
        else:
            total_cost += distance(route[i], route[i + 1])

    return total_cost


def solve(cities):
    route = greedy_tour(cities)
    return route, calc_cost(route)
