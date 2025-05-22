import math

def euclidean_distance(a, b):
    return math.hypot(a[1] - b[1], a[2] - b[2])

def total_distance(route):
    return sum(euclidean_distance(route[i], route[i+1]) for i in range(len(route) - 1)) + euclidean_distance(route[-1], route[0])

def two_opt(route):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue  # skip adjacent
                new_route = best[:i] + best[i:j][::-1] + best[j:]
                if total_distance(new_route) < total_distance(best):
                    best = new_route
                    improved = True
        route = best
    return best

def tsp_2opt(cities):
    unvisited = cities[:]
    current = unvisited.pop(0)
    route = [current]
    while unvisited:
        next_city = min(unvisited, key=lambda city: euclidean_distance(current, city))
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    improved_route = two_opt(route)
    return improved_route
