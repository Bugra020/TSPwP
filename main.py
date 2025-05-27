import random
import sys
import solver

# if no matplotlib library then fallback to no graph mode
graph_mode = True
try:
    import matplotlib.pyplot as plt
except:
    graph_mode = False

# usage: python main inputFilePath outputFilePath

def generate_input(number_of_cities):
    # generates random city data and writes to input.txt
    inputs = []
    for city_id in range(number_of_cities):
        penalty = random.randint(1, number_of_cities // 10)
        x = random.randint(-number_of_cities, number_of_cities)
        y = random.randint(-number_of_cities, number_of_cities)
        inputs.append([city_id, x, y, penalty])

    with open("io_files\input.txt", "w") as file:
        for city in inputs:
            file.write(f"{city[0]} {city[1]} {city[2]} {city[3]}\n")

    return inputs


def read_input(path):
    # reads input.txt and returns the list of cities
    cities = []
    with open(path, "r") as file:
        lines = file.readlines()

    penalty = lines[0]  # first line is fixed penalty
    lines.pop(0)

    for line in lines:
        parts = list(map(int, line.strip().split()))
        parts.append(int(penalty))  # append global penalty to city info
        parts.append(0)  # unused field for potential metadata
        cities.append(parts)

    return cities


def write_output(route, cost, path):
    # writes the output cost and city order to output.txt
    visited = [city for city in route if city[0] != -1]

    with open(path, "w") as file:
        file.write(f"{cost} {len(visited) - 1}\n")  # exclude repeated last city
        for city in visited[:-1]:  # write route without final loop-back
            file.write(f"{city[0]}\n")


def graph(cities, route, cost):
    # visualizes the tour using matplotlib
    x_all = [city[1] for city in cities]
    y_all = [city[2] for city in cities]

    x_route = [city[1] for city in route if city[0] != -1]
    y_route = [city[2] for city in route if city[0] != -1]

    plt.plot(x_route, y_route, "-", color="blue")  # draw the path

    scatter = plt.scatter(x_all, y_all, c=[city[3] for city in cities], cmap="inferno")
    cbar = plt.colorbar(scatter)
    cbar.set_label("penalty")

    skipped = sum(1 for city in route if city[0] == -1)
    plt.title(f"cost: {cost}, visited cities: {len(route) - skipped - 1}")
    plt.show()


def main(plotlib):
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # cities = generate_input(1000)
    cities = read_input(input_path)
    route, cost = solver.solve(cities)
    write_output(route, cost, output_path)
    if plotlib:
        graph(cities, route, cost)

if __name__ == "__main__":
    main(graph_mode)