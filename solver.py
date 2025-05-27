import math
import random
from typing import List, Tuple

City = Tuple[int, int, int, int]
Route = List[City]


def distance(a :City, b: City) -> int:
    dx = a[1] - b[1]
    dy = a[2] - b[2]
    return (round(math.sqrt(dx * dx + dy * dy)))


def greedy_tour(cities: Route) -> Route:
    # selcets a random city to start
    # forms the path to the shortest city
    # creates a TSP path not improve later (not TSPwP)

    start_city = random.choice(cities)
    city_dict = {city[0]: city for city in cities}
    unvisited = set(city[0] for city in cities if city[0] != start_city[0])

    tour = [start_city]
    current = start_city
    while unvisited:
        next_id = min(unvisited, key=lambda cid: distance(current, city_dict[cid]))
        current = city_dict[next_id]
        tour.append(current)
        unvisited.remove(next_id)

    tour.append(tour[0])
    return tour


def calc_cost(route: Route) -> int:
    total_cost = 0
    real_route = [city for city in route[:] if city[0] != -1]

    total_cost += sum(city[3] for city in route if city[0] == -1)

    for i in range(len(real_route) - 1):
        total_cost += distance(real_route[i], real_route[i + 1])

    if len(real_route) > 1:
        total_cost += distance(real_route[-1], real_route[0])
    return total_cost


def penalty_improve(route: Route, window: int) -> Route:
    # iterates over the route and checks whether skipping (window - 2) cities
    # and connecting endpoints is shorter than visiting them
    # considering the penalties

    i = 0
    while i <= len(route) - window:
        real_indices = []
        j = i
        while len(real_indices) < window and j < len(route):
            if route[j][0] != -1:
                real_indices.append(j)
            j += 1

        if len(real_indices) < window:
            break

        ci = real_indices

        # calculate the distance of the full part (visiting all)
        part_dist = sum(distance(route[ci[t]], route[ci[t + 1]]) for t in range(window - 1))
        # calculate direct shortcut distance from first to last
        direct_dist = distance(route[ci[0]], route[ci[-1]])
        # sum the penalties for skipped cities
        penalty_sum = sum(route[ci[t]][3] for t in range(1, window - 1))

        if part_dist > direct_dist + penalty_sum:
            for t in range(1, window - 1):
                route[ci[t]] = (-1, 0, 0, route[ci[t]][3])

        i = real_indices[0] + 1

    return route


def swap_improve(route: Route) -> Route:
    # improves the route by applying random swaps
    # avoids modifying skipped cities
    # tries n / log(n) * 10 iterations

    best = route[:]
    best_cost = calc_cost(best)
    n = len(best)
    tries = int(n / math.log10(n) * 10)

    for _ in range(tries):
        i, k = sorted(random.sample(range(1, n - 2), 2))

        if best[i][0] == -1 or best[k][0] == -1:
            continue

        new_route = best[:i] + best[i : k + 1][::-1] + best[k + 1 :]
        new_cost = calc_cost(new_route)

        if new_cost < best_cost:
            best = new_route
            best_cost = new_cost

    return best


def solve(cities: Route) -> Tuple[Route, int]:
    route = greedy_tour(cities)
    route = swap_improve(route)

    for _ in range(5):
        route = penalty_improve(route, 3)
        route = penalty_improve(route, 5)
        route = swap_improve(route)

    return route, calc_cost(route)
