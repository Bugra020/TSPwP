import random
import matplotlib.pyplot as plt
import sys
import solver_1


def generate_input(number_of_cities):
    inputs = []
    for id in range(0, number_of_cities):
        penalty = random.randint(1, number_of_cities / 10)
        rand_x, rand_y = random.randint(
            -number_of_cities, number_of_cities
        ), random.randint(-number_of_cities, number_of_cities)
        inputs.append([id, rand_x, rand_y, penalty])

    with open("input.txt", "w") as file:
        for city in inputs:
            line = f"{city[0]} {city[1]} {city[2]} {city[3]}\n"
            file.write(line)

    return inputs


def graph(cities, route, cost):
    x_axis = [city[1] for city in cities]
    y_axis = [city[2] for city in cities]
    x_axis1 = []
    y_axis1 = []
    for city in route:
        if city[0] != -1:
            x_axis1.append(city[1])
            y_axis1.append(city[2])
    # x_axis1 = [city[1] for city in route]
    # y_axis1 = [city[2] for city in route]

    # plt.plot(x_axis, y_axis, "+", color="purple")
    plt.plot(x_axis1, y_axis1, "-", color="blue")

    scatter = plt.scatter(
        x_axis, y_axis, c=[city[3] for city in cities], cmap="inferno"
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label("penalty")

    skipped = 0
    for city in route:
        if city[0] == -1:
            skipped += 1

    plt.title(f"cost:{cost}, visited cities:{len(route)-skipped-1}")

    plt.show()


def read_input():
    cities = []
    with open("input.txt", "r") as file:
        lines = file.readlines()
        min_x, min_y = sys.maxsize, sys.maxsize
        for line in lines:
            city = list(map(int, line.strip().split()))
            city.append(0)
            cities.append(city)

            if city[1] < min_x:
                min_x = city[1]
            if city[2] < min_y:
                min_y = city[2]

        for city in cities:
            city[1] -= min_x
            city[2] -= min_y

    return cities


def write_output(route, cost):
    skipped = 0
    for city in route:
        if city[0] == -1:
            skipped += 1

    with open("output.txt", "w") as file:
        file.write(f"{cost} {len(route)-skipped-1}\n")
        for city in route:
            if city[0] != -1:
                file.write(f"{city[0]}\n")


def main():
    cities, route = [], []
    generate_input(1000)
    cities = read_input()
    route, cost = solver_1.solve(cities)
    write_output(route, cost)
    #graph(cities, route, cost)


if __name__ == "__main__":
    main()
