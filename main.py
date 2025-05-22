import random
import matplotlib.pyplot as plt
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


def graph(cities, route):
    x_axis = [city[1] for city in cities]
    y_axis = [city[2] for city in cities]
    x_axis1 = [city[1] for city in route]
    y_axis1 = [city[2] for city in route]

    # plt.plot(x_axis, y_axis, "+", color="purple")
    plt.plot(x_axis1, y_axis1, "-", color="blue")

    scatter = plt.scatter(
        x_axis, y_axis, c=[city[3] for city in cities], cmap="inferno"
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label("Penalty Value")

    plt.show()


def read_input():
    cities = []
    with open("input.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            city = list(map(int, line.strip().split()))
            cities.append(city)
    return cities


def write_output(cost, n_v, route):
    with open("output.txt", "w") as file:
        file.write(f"{cost} {n_v}\n")
        for city in route:
            file.write(f"{city[0]}\n")


def main():
    cities, route = [], []
    generate_input(1000)
    cities = read_input()
    route = solver_1.solve(cities)
    graph(cities, route)


if __name__ == "__main__":
    main()
