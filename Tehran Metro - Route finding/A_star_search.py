import math

import pandas as pd


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def isEmpty(self):
        return len(self.queue) == 0

    def push(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    # priority is based on the MINIMUM of distances = MIN(heuristic)
    def pop(self):
        try:
            minIndex = 0
            for i in range(len(self.queue)):
                if self.queue[i].f_cost < self.queue[minIndex].f_cost:
                    minIndex = i
            item = self.queue[minIndex]
            del self.queue[minIndex]
            return item
        except IndexError:
            print()
            exit()


class Station:
    def __init__(self, name, adjacent, h, parent, total_dist_from_root):
        self.name = name
        self.adjacent = adjacent
        self.heuristic = h
        self.parent = parent
        self.total_dist_from_root = total_dist_from_root
        self.f_cost = total_dist_from_root + h

    def __str__(self):
        return "Name: {}\t Parent:{} \t Heuristic:{}\t Adjacent: {}\t tot_dist: {}".format(self.name, self.parent,
                                                                                           self.heuristic,
                                                                                           self.adjacent,
                                                                                           self.total_dist_from_root)


distanceData = pd.read_csv('lat_long.csv', index_col='NAME')
metroStationsData = pd.read_csv('metro(1).csv', index_col=0)


def calcEucDist(root, goal):
    rootX = distanceData.loc[root.name, 'X']
    rootY = distanceData.loc[root.name, 'Y']
    goalX = distanceData.loc[goal.name, 'X']
    goalY = distanceData.loc[goal.name, 'Y']

    return math.sqrt((rootX - goalX) ** 2 + (rootY - goalY) ** 2)


def calcEucDist_byName(root_name, goal_name):
    rootX = distanceData.loc[root_name, 'X']
    rootY = distanceData.loc[root_name, 'Y']
    goalX = distanceData.loc[goal_name, 'X']
    goalY = distanceData.loc[goal_name, 'Y']

    return math.sqrt((rootX - goalX) ** 2 + (rootY - goalY) ** 2)


def calcChebDist(root, goal):
    rootX = distanceData.loc[root.name, 'X']
    rootY = distanceData.loc[root.name, 'Y']
    goalX = distanceData.loc[goal.name, 'X']
    goalY = distanceData.loc[goal.name, 'Y']

    return max(abs(rootX - goalX), abs(rootY - goalY))


def calcChebDist_byName(root_name, goal_name):
    rootX = distanceData.loc[root_name, 'X']
    rootY = distanceData.loc[root_name, 'Y']
    goalX = distanceData.loc[goal_name, 'X']
    goalY = distanceData.loc[goal_name, 'Y']

    return max(abs(rootX - goalX), abs(rootY - goalY))


root_name = input('Enter starting station name: ')
goal_name = input('Enter goal station name: ')

seen = []
myQueue = PriorityQueue()

mask = metroStationsData[root_name].notnull()
CurrentStation = Station(name=root_name, adjacent=metroStationsData.loc[root_name, mask].to_dict(),
                         h=calcEucDist_byName(root_name, goal_name), parent='null', total_dist_from_root=0)

seen.append(CurrentStation.name)
while CurrentStation.name != goal_name:

    for eachAdj_name, distance in CurrentStation.adjacent.items():
        if eachAdj_name not in seen:
            seen.append(eachAdj_name)
            mask = metroStationsData[eachAdj_name].notnull()
            adjS = Station(name=eachAdj_name, adjacent=metroStationsData.loc[eachAdj_name, mask].to_dict(),
                           h=calcEucDist_byName(eachAdj_name, goal_name), parent=CurrentStation,
                           total_dist_from_root=CurrentStation.total_dist_from_root + distance)
            myQueue.push(adjS)
    CurrentStation = myQueue.pop()

print('Reached!')
total_cost = CurrentStation.total_dist_from_root
while CurrentStation.name != root_name:
    print(CurrentStation.name, end=' <- ')
    CurrentStation = CurrentStation.parent
print(CurrentStation.name)
print('Total Cost of the route: ', total_cost)
print('Heuristic = Euc')
