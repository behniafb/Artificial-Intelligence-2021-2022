# Name: Behnia Farahbod
# Student number: 982023020
# 1400/08/10

import pandas as pd


class Station:
    def __init__(self, name, adjacent):
        self.name = name
        self.adjacent = adjacent

    def __str__(self):
        return "Name: {}\t Adjacent: {}".format(self.name, self.adjacent)


seen = []


def dfs(current_node, total_cost):
    if current_node == goal:
        print("Answer: ", current_node, end=" - ")
        return total_cost

    mask = metroStationsData[current_node].notnull()
    s = Station(current_node, metroStationsData.loc[current_node, mask].to_dict())

    for eachAdj, distance in s.adjacent.items():
        if eachAdj not in seen:
            seen.append(eachAdj)
            ans = dfs(eachAdj, total_cost + distance)
            if ans is None:
                continue
            print(current_node, end=" - ")
            return ans
    return None


metroStationsData = pd.read_csv('metro_stations_sparse_matrix_distoriented.csv', index_col=0)

root = input('Enter starting station name: ')
goal = input('Enter goal station name: ')

seen.append(root)
answer = dfs(root, 0)

if answer is None:
    print("There is no route from {} to {}.".format(root, goal))
else:
    print("\nTotal cost = ", answer)
