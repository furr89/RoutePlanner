import math

# Indexes for accessing road values
g_index = 0
h_index = 1
f_index = 2
p_index = 3

def shortest_path(M, start, goal):

    # Check if inputs are valid
    if M == None or type(start) != int or type(goal) != int:
        return None

    current_road = start

    open_list = {}

    heuristic = get_distance(M, current_road, goal)
    open_list[current_road] = [0, heuristic, 0+heuristic]

    # Initialise the closed list with the start
    closed_list = []
    closed_list.append(start)

    visited_list = set()
    reverse_path_roads = set()

    while len(open_list) > 0:

        reverse_path_roads.clear()
    
        # If the goal has been reached
        if current_road == goal:
            return closed_list
            
        # For every neighbouring roads from the current
        for next in M.roads[current_road]:

            # Calculate the g and h score 
            actual_dist = get_distance(M, current_road, next) + open_list[current_road][g_index]
            heuristic = get_distance(M, next, goal)

            # check if it's a previous road
            if next in visited_list:
                continue

            if next not in open_list:

                # Save it in the open list with g, h, and f scores and its previous road
                open_list[next] = [actual_dist, heuristic, actual_dist+heuristic, current_road]

            # If already in the open list
            else:

                # If next and current road have the same previous road
                if open_list[next][p_index] == open_list[current_road][p_index]:
                    reverse_path_roads.add(next)

                # Update the next road if it's connected to another previous road, comparing the g score
                elif actual_dist < open_list[next][g_index]:
                    open_list[next] = [actual_dist, heuristic, actual_dist+heuristic, current_road]

        # Remove from open list and exclude from being searched again
        open_list.pop(current_road)
        visited_list.add(current_road)

        # Finds lowest road based on f score
        lcr = min(open_list.items(), key=lambda f: f[1][f_index])
        current_road = lcr[0]

        # If the lowest cost path is in a road previously seen 
        if current_road in reverse_path_roads:
            closed_list.pop()

        closed_list.append(current_road)
            
    # If no paths found
    return None


def get_distance(M, start, goal):
    """
    Finds the straight line distance between 2 points

    Args: 
        M(Map), start(index), goal(index)

    Returns:
        distance(float)
    """

    dx = abs(M.intersections[goal][0] - M.intersections[start][0])
    dy = abs(M.intersections[goal][1] - M.intersections[start][1])

    return dx + dy
