import numpy as numpy
from queue import PriorityQueue
from utils.utils import PathPlanMode, Heuristic, cost, expand, visualize_expanded, visualize_path
import numpy as np

def compute_heuristic(node, goal, heuristic: Heuristic):
    """ Computes an admissible heuristic value of node relative to goal.

    Args:
        node (tuple): The cell whose heuristic value we want to compute.
        goal (tuple): The goal cell.
        heuristic (Heuristic): The heuristic to use. Must
        specify either Heuristic.MANHATTAN or Heuristic.EUCLIDEAN.

    Returns:
        h (float): The heuristic value.

    """
    # TODO:
    
    
    # Using Manhattan distance
    
    x=abs(node[0]-goal[0])
    y=abs(node[1]-goal[1])
    if heuristic==Heuristic.MANHATTAN:
        scaling_factor = 0.5
        h=(x+y)*scaling_factor
    elif heuristic ==Heuristic.EUCLIDEAN:
        scaling_factor=0.5/(2**0.5)
        h=((x**2+y**2)**0.5)*scaling_factor

    return h


def uninformed_search(grid, start, goal, mode: PathPlanMode):
    """ Find a path from start to goal in the gridworld using 
    BFS or DFS.

    Args:
        grid (numpy): NxN numpy array representing the world,
        with terrain features encoded as integers.
        start (tuple): The starting cell of the path.
        goal (tuple): The ending cell of the path.
        mode (PathPlanMode): The search strategy to use. Must
        specify either PathPlanMode.DFS or PathPlanMode.BFS.

    Returns:
        path (list): A list of cells from start to goal.
        expanded (list): A list of expanded cells.
        frontier_size (list): A list of integers containing
        the size of the frontier at each iteration.
    """

    frontier = [start]
    frontier_sizes = []
    expanded = []
    reached = {start: None}

    # TODO:
    path = []
    while frontier:
        frontier_sizes.append(len(frontier))
        if mode==PathPlanMode.DFS:
            current=frontier.pop()
        else:
            current=frontier.pop(0)
        if current in expanded:
            continue
        expanded.append(current)
        if current==goal:
            break
        for neighbor in expand(grid, current):
            if neighbor not in reached:
                reached[neighbor] = current
                frontier.append(neighbor)

    if goal not in reached:
        return [], expanded, frontier_sizes

    node = goal
    while node is not None:
        path.insert(0, node)
        node = reached[node]
    return path, expanded, frontier_sizes


def a_star(grid, start, goal, mode: PathPlanMode, heuristic: Heuristic, width):
    """ Performs A* search or beam search to find the
    shortest path from start to goal in the gridworld.

    Args:
        grid (numpy): NxN numpy array representing the world,
        with terrain features encoded as integers.
        start (tuple): The starting cell of the path.
        goal (tuple): The ending cell of the path.
        mode (PathPlanMode): The search strategy to use. Must
        specify either PathPlanMode.A_STAR or
        PathPlanMode.BEAM_SEARCH.
        heuristic (Heuristic): The heuristic to use. Must
        specify either Heuristic.MANHATTAN or Heuristic.EUCLIDEAN.
        width (int): The width of the beam search. This should
        only be used if mode is PathPlanMode.BEAM_SEARCH.

    Returns:
        path (list): A list of cells from start to goal.
        expanded (list): A list of expanded cells.
        frontier_size (list): A list of integers containing
        the size of the frontier at each iteration.
    """

    frontier = PriorityQueue()
    frontier.put((0, start))
    frontier_sizes = []
    expanded = []
    reached = {start: {"cost": cost(grid, start), "parent": None}}

    # TODO:
    path = []
    while not frontier.empty():
        if mode == PathPlanMode.BEAM_SEARCH: #check if it is BeamSearch
            list2 = []
            while not frontier.empty():
                list2.append(frontier.get())
            list2 = sorted(list2)
            for i in range(min(len(list2), width)):
                frontier.put(list2[i])

        frontier_sizes.append(frontier.qsize())
        
        x, current = frontier.get()
        expanded.append(current)
        
        if current ==goal:
            break
        
        for next in expand(grid, current):
            g = reached[current]["cost"] + cost(grid, next)
            h = compute_heuristic(next, goal, heuristic)
            f_value = g+ h
            if next not in reached or g < reached[next]["cost"]:
                reached[next] = {"cost": g, "parent": current}
                frontier.put((f_value, next))

        
    node = goal
    while node is not None:
        path.insert(0, node)
        node = reached[node]["parent"]
    return path, expanded, frontier_sizes


def local_search(grid, start, goal, heuristic: Heuristic):
    """ Find a path from start to goal in the gridworld using
    local search.

    Args:
        grid (numpy): NxN numpy array representing the world,
        with terrain features encoded as integers.
        start (tuple): The starting cell of the path.
        goal (tuple): The ending cell of the path.
        heuristic (Heuristic): The heuristic to use. Must
        specify either Heuristic.MANHATTAN or Heuristic.EUCLIDEAN.

    Returns:
        path (list): A list of cells from start to goal.
    """

    path = [start]

    # TODO:
    while True: 
        current = path[len(path) - 1]
        if current == goal:
            break
        neighbor=expand(grid,current)
        
        h= compute_heuristic(current, goal, heuristic)
        optimal_node = current
        optimal_h = h
        for n in neighbor:
            h_next = compute_heuristic(n, goal, heuristic)
            if h_next<optimal_h:
                optimal_h=h_next
                optimal_node=n
        if optimal_node == current:
            return []
        path.append(optimal_node)

    return path


def test_world(world_id, start, goal, h, width, animate, world_dir):
    print(f"Testing world {world_id}")
    grid = np.load(f"{world_dir}/world_{world_id}.npy")

    if h == 0:
        modes = [
            PathPlanMode.DFS,
            PathPlanMode.BFS
        ]
        print("Modes: 1. DFS, 2. BFS")
    elif h == 1 or h == 2:
        modes = [
            PathPlanMode.A_STAR,
            PathPlanMode.BEAM_SEARCH
        ]
        if h == 1:
            print("Modes: 1. A_STAR, 2. BEAM_A_STAR")
            print("Using Manhattan heuristic")
        else:
            print("Modes: 1. A_STAR, 2. BEAM_A_STAR")
            print("Using Euclidean heuristic")
    elif h == 3 or h == 4:
        h -= 2
        modes = [
            PathPlanMode.LOCAL_SEARCH
        ]
        if h == 1:
            print("Mode: LOCAL_SEARCH")
            print("Using Manhattan heuristic")
        else:
            print("Mode: LOCAL_SEARCH")
            print("Using Euclidean heuristic")

    for mode in modes:

        search_type, path, expanded, frontier_size = None, [], [], []
        if mode == PathPlanMode.DFS:
            path, expanded, frontier_size = uninformed_search(grid, start, goal, mode)
            search_type = "DFS"
        elif mode == PathPlanMode.BFS:
            path, expanded, frontier_size = uninformed_search(grid, start, goal, mode)
            search_type = "BFS"
        elif mode == PathPlanMode.A_STAR:
            path, expanded, frontier_size = a_star(grid, start, goal, mode, h, 0)
            search_type = "A_STAR"
        elif mode == PathPlanMode.BEAM_SEARCH:
            path, expanded, frontier_size = a_star(grid, start, goal, mode, h, width)
            search_type = "BEAM_A_STAR"
        elif mode == PathPlanMode.LOCAL_SEARCH:
            path = local_search(grid, start, goal, h)
            search_type = "LOCAL_SEARCH"

        if search_type:
            print(f"Mode: {search_type}")
            path_cost = 0
            for c in path:
                path_cost += cost(grid, c)
            print(f"Path length: {len(path)}")
            print(f"Path cost: {path_cost}")
            if frontier_size:
                print(f"Number of expanded states: {len(frontier_size)}")
                print(f"Max frontier size: {max(frontier_size)}\n")
            if animate == 0 or animate == 1:
                visualize_expanded(grid, start, goal, expanded, path, animation=animate)
            else:
                visualize_path(grid, start, goal, path)