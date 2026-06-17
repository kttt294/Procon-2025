from collections import deque

class Puzzle8:
    def __init__(self, goal_state, heuristic_type='h2'):
        self.goal = goal_state
        self.heuristic_type = heuristic_type # 'h1' (Misplaced) hoặc 'h2' (Manhattan)

    def get_neighbors(self, state):
        neighbors = []
        i = state.index(0)
        row, col = i // 3, i % 3
        
        moves = []
        if row > 0: moves.append(i - 3)
        if row < 2: moves.append(i + 3)
        if col > 0: moves.append(i - 1)
        if col < 2: moves.append(i + 1)
        
        for j in moves:
            new_state = list(state)
            new_state[i], new_state[j] = new_state[j], new_state[i]
            neighbors.append((tuple(new_state), 1))
            
        return neighbors

    def get_h(self, state):
        if self.heuristic_type == 'h1':
            return self._get_h1(state)
        return self._get_h2(state)

    def _get_h1(self, state):
        misplaced = 0
        for i, val in enumerate(state):
            if val != 0 and val != self.goal[i]:
                misplaced += 1
        return misplaced

    def _get_h2(self, state):
        distance = 0
        for i, val in enumerate(state):
            if val != 0:
                goal_idx = self.goal.index(val)
                distance += abs(i // 3 - goal_idx // 3) + abs(i % 3 - goal_idx % 3)
        return distance


def bfs(graph, start, goal, verbose=False):
    def reconstruct_path(parent, node):
        path = []
        while node is not None:
            path.append(node)
            node = parent[node]
        return path[::-1]

    if start == goal:
        return [start], [start]

    open_list = deque([start])
    open_set = {start}
    closed = set()
    closed_list = []
    parent = {start: None}
    step = 0

    while open_list:
        current = open_list.popleft()
        open_set.remove(current)
        step += 1

        if verbose:
            print(f"Bước {step}: Phát triển {current}, Open={list(open_list)}, Closed={closed_list + [current]}")

        closed.add(current)
        closed_list.append(current)

        if current == goal:
            return reconstruct_path(parent, current), closed_list

        neighbors = sorted(graph.get_neighbors(current), key=lambda x: x[0])
        
        for neighbor, edge_cost in neighbors:
            if neighbor not in closed and neighbor not in open_set:
                open_list.append(neighbor)
                open_set.add(neighbor)
                parent[neighbor] = current

    return None, closed_list


def dfs(graph, start, goal, verbose=False):
    def reconstruct_path(parent, node):
        path = []
        while node is not None:
            path.append(node)
            node = parent[node]
        return path[::-1]

    if start == goal:
        return [start], [start]

    stack = [start]
    stack_set = {start}
    closed = set()
    closed_list = []
    parent = {start: None}
    step = 0

    while stack:
        current = stack.pop()
        stack_set.remove(current)
        step += 1

        if verbose:
            print(f"Bước {step}: Phát triển {current}, Open={stack}, Closed={closed_list + [current]}")

        closed.add(current)
        closed_list.append(current)

        if current == goal:
            return reconstruct_path(parent, current), closed_list

        neighbors = sorted(graph.get_neighbors(current), key=lambda x: x[0], reverse=True)
        
        for neighbor, edge_cost in neighbors:
            if neighbor not in closed and neighbor not in stack_set:
                stack.append(neighbor)
                stack_set.add(neighbor)
                parent[neighbor] = current

    return None, closed_list

def ucs(graph, start, goal, verbose=False):
    open_list = [(0, start)]
    closed = set()
    closed_list = []
    cha = {start: None}
    g_score = {start: 0}
    step = 0

    while open_list:
        open_list.sort(key=lambda x: (x[0], x[1]))
        current_g, current = open_list.pop(0)
        step += 1

        if verbose:
            open_nodes = [n[1] for n in open_list]
            print(f"Bước {step}: Phát triển {current} (g={current_g}), Open={open_nodes}, Closed={closed_list + [current]}")

        if current in closed:
            continue

        closed.add(current)
        closed_list.append(current)

        if current == goal:
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = cha[temp]
            return path[::-1], g_score[goal]

        neighbors = sorted(graph.get_neighbors(current), key=lambda x: x[0])
        for neighbor, cost in neighbors:
            tentative_g = current_g + cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                cha[neighbor] = current
                g_score[neighbor] = tentative_g
                open_list.append((tentative_g, neighbor))

    return None, float('inf')


def ucs2(graph, start, goal):
  def reconstruct_path(parent, node):
    path = []
    while node is not None:
      path.append(node)
      node = parent[node]
    return path[::-1]
  
  open_list = [(0, start)]
  closed = set()
  parent = {start: None}
  g_score = {start: 0}
  
  while open_list:
    open_list.sort(key = lambda x: (x[0], x[1]), reverse=True)
    current_g, current = open_list.pop()
    
    if current in closed: continue
    closed.add(current)
    
    if current == goal:
      return reconstruct_path(parent, current), len(closed)
    
    neighbors = sorted(graph.get_neighbors(current), key=lambda x: x[0])
    
    for neighbor, cost in neighbors:
      tentative_g = current_g + cost
      if neighbor not in g_score or tentative_g < g_score[neighbor]:
        open_list.append((tentative_g, neighbor))
        g_score[neighbor] = tentative_g
        parent[neighbor] = current
  
  return None, len(closed)




def ids(graph, start, goal, max_depth=50, verbose=False):
    if start == goal:
        return [start], 0

    for limit in range(max_depth + 1):
        if verbose:
            print(f"\n--- VÒNG LẶP ĐỘ SÂU (LIMIT) = {limit} ---")
            
        stack = [(start, [start])]
        closed_list = []
        step = 0

        while stack:
            current, path = stack.pop()
            step += 1
            depth = len(path) - 1

            if verbose:
                open_nodes = [n[0] for n in stack]
                print(f"Bước {step}: Phát triển {current} (Depth={depth}), Open={open_nodes}, Closed={closed_list + [current]}")

            closed_list.append(current)

            if depth >= limit:
                continue

            neighbors = sorted(graph.get_neighbors(current), key=lambda x: x[0], reverse=True)
            for neighbor, edge_cost in neighbors:
                if neighbor == goal:
                    if verbose:
                        print(f"Bước {step+1}: Phát triển {neighbor} (Depth={depth+1}), ĐÃ TÌM THẤY ĐÍCH!")
                    return path + [neighbor], limit
                
                if neighbor not in path:
                    stack.append((neighbor, path + [neighbor]))

    return None, max_depth

def ids2(graph, start, goal, max_depth):
  if start == goal:
    return [start], 0

  for limit in range(max_depth+1):
    open_list = [(start, [start])]
    
    while open_list:
      current, path = open_list.pop()
      depth = len(path) - 1
      
      if depth >= limit:
        continue
      
      neighbors = sorted(graph.get_neighbors(current), key=lambda x: x[0], reverse=True)
      for neighbor, _ in neighbors:
        if neighbor == goal:
          return path + [neighbor], limit
        if neighbor not in path:
          open_list.append((neighbor, path + [neighbor]))
  
  return None, max_depth



def greedy_best_first_search(graph, start, goal, verbose=False):
    open_list = [(graph.get_h(start), start, [start], 0)]
    closed = set()
    closed_list = []
    step = 0

    while open_list:
        open_list.sort(key=lambda x: x[0])
        h, current, path, cost = open_list.pop(0)
        step += 1

        if verbose:
            open_nodes = [n[1] for n in open_list]
            print(f"Bước {step}: Phát triển {current} (h={h}), Open={open_nodes}, Closed={closed_list + [current]}")

        if current in closed:
            continue

        closed.add(current)
        closed_list.append(current)

        if current == goal:
            return path, cost

        for neighbor, edge_cost in graph.get_neighbors(current):
            if neighbor not in closed:
                open_list.append((graph.get_h(neighbor), neighbor, path + [neighbor], cost + edge_cost))

    return None, float('inf')


def hill_climbing_search(graph, start, goal, verbose=False):
    current = start
    path = [current]
    cost = 0
    step = 0

    if verbose:
        print(f"Bước {step}: Khởi đầu tại {current} (h={graph.get_h(current)})")

    if current == goal:
        return path, cost

    while True:
        step += 1
        neighbors = graph.get_neighbors(current)
        if not neighbors: 
            break

        best_neighbor = None
        best_h = float('inf')
        best_edge_cost = 0

        for neighbor, edge_cost in neighbors:
            h = graph.get_h(neighbor)
            if h < best_h:
                best_h = h
                best_neighbor = neighbor
                best_edge_cost = edge_cost

        if verbose:
            h_list = [(n, graph.get_h(n)) for n, c in neighbors]
            print(f"Bước {step}: Tại {current}, các kề {h_list}. Chọn {best_neighbor} (h={best_h})")

        if best_h < graph.get_h(current):
            current = best_neighbor
            path.append(best_neighbor)
            cost += best_edge_cost

            if current == goal: 
                break
        else:
            break

    return path, cost


def a_star_search(graph, start, goal, verbose=False):
    open_list = [(graph.get_h(start), 0, start)]
    closed = set()
    closed_list = []
    cha = {start: None}
    g_score = {start: 0}
    step = 0

    while open_list:
        open_list.sort(key=lambda x: x[0])
        current_f, current_g, current = open_list.pop(0)
        step += 1

        if verbose:
            open_nodes = [n[2] for n in open_list]
            print(f"Bước {step}: Phát triển {current} (g={current_g}, h={graph.get_h(current)}, f={current_f}), Open={open_nodes}, Closed={closed_list + [current]}")

        if current in closed:
            continue

        closed.add(current)
        closed_list.append(current)

        if current == goal:
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = cha[temp]
            return path[::-1], g_score[goal]

        for neighbor, cost in graph.get_neighbors(current):
            tentative_g = current_g + cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                cha[neighbor] = current
                g_score[neighbor] = tentative_g
                open_list.append((tentative_g + graph.get_h(neighbor), tentative_g, neighbor))

    return None, float('inf')


def idastar(graph, start, goal, alpha=2, verbose=False):
    i = 0
    while True:
        if verbose:
            print(f"\n--- VÒNG LẶP NGƯỠNG i = {i} ---")
            
        open_list = [(graph.get_h(start), 0, start, [start])]
        closed = []
        dung_lap = True
        step = 0

        while open_list:
            open_list.sort(key=lambda x: x[0], reverse=True)
            f_current, g_current, current, path = open_list.pop()
            step += 1

            if verbose:
                open_nodes = [n[2] for n in open_list]
                print(f"Bước {step}: Phát triển {current} (f={f_current}), Open={open_nodes}, Closed={closed + [current]}")

            if current == goal:
                return path, g_current

            closed.append(current)

            for neighbor, cost in graph.get_neighbors(current):
                if neighbor in path: 
                    continue

                g_neighbor = g_current + cost
                f_neighbor = g_neighbor + graph.get_h(neighbor)

                if f_neighbor <= i:
                    open_list.append((f_neighbor, g_neighbor, neighbor, path + [neighbor]))
                else:
                    dung_lap = False

        if dung_lap:
            return None, float('inf')

        i += alpha


def beam_search(graph, start, goal, width, verbose=False):
    current_level = [(start, [start], 0)]
    step = 0

    while current_level:
        step += 1
        
        if verbose:
            nodes = [n[0] for n in current_level]
            print(f"Bước {step}: Xét các đỉnh Open={nodes}")

        for node, path, cost in current_level:
            if node == goal:
                return path, cost

        next_candidates = []
        for node, path, cost in current_level:
            for neighbor, edge_cost in graph.get_neighbors(node):
                if neighbor not in path:
                    next_candidates.append((neighbor, path + [neighbor], cost + edge_cost))

        if not next_candidates:
            break

        next_candidates.sort(key=lambda x: graph.get_h(x[0]))
        current_level = next_candidates[:width]

    return None, float('inf')
  
  

if __name__ == "__main__":
    def print_path(path):
        if not path:
            print("Không tìm thấy đường đi.")
            return
        for step, state in enumerate(path):
            print(f"  Bước {step}: {state[:3]} | {state[3:6]} | {state[6:]}")
    
    start_state = (1,2,3,4,5,6,0,7,8)
    goal_state  = (1,2,3,4,5,6,7,8,0)
    
    puzzle = Puzzle8(goal_state)

    print("1. BREADTH-FIRST SEARCH (BFS)")
    path_bfs, _ = bfs(puzzle, start_state, goal_state, verbose=False)
    print("=> Lộ trình BFS:")
    print_path(path_bfs)
    print("-" * 50)

    print("2. DEPTH-FIRST SEARCH (DFS)")
    path_dfs, _ = dfs(puzzle, start_state, goal_state, verbose=False)
    print("=> Lộ trình DFS:")
    print_path(path_dfs)
    print("-" * 50)
    
    print("3. UNIFORM COST SEARCH (UCS)")
    path_ucs, cost_ucs = ucs(puzzle, start_state, goal_state, verbose=False)
    print(f"=> Lộ trình UCS (Chi phí: {cost_ucs}):")
    print_path(path_ucs)
    print("-" * 50)  
  
    print("4. ITERATIVE DEEPENING SEARCH (IDS)")
    path_ids, limit_reached = ids(puzzle, start_state, goal_state, max_depth=50, verbose=False)
    print(f"=> Lộ trình IDS (Tìm thấy tại Limit/Độ sâu: {limit_reached}):")
    print_path(path_ids)
    
    print("5. GREEDY BEST-FIRST SEARCH")
    path_greedy, cost_greedy = greedy_best_first_search(puzzle, start_state, goal_state, verbose=False)
    print(f"=> Lộ trình Greedy (Chi phí: {cost_greedy}):")
    print_path(path_greedy)
    print("-" * 50)

    print("6. BEAM SEARCH (Width = 2)")
    path_beam, cost_beam = beam_search(puzzle, start_state, goal_state, width=2, verbose=False)
    print(f"=> Lộ trình Beam Search (Chi phí: {cost_beam}):")
    print_path(path_beam)
    print("-" * 50)

    print("7. HILL CLIMBING SEARCH")
    path_hill, cost_hill = hill_climbing_search(puzzle, start_state, goal_state, verbose=False)
    print(f"=> Lộ trình Hill Climbing (Chi phí: {cost_hill}):")
    print_path(path_hill)
    print("-" * 50)

    print("8. A* SEARCH")
    path_astar, cost_astar = a_star_search(puzzle, start_state, goal_state, verbose=False)
    print(f"=> Lộ trình A* (Chi phí: {cost_astar}):")
    print_path(path_astar)
    print("-" * 50)

    print("9. IDA* SEARCH (Alpha = 2)")
    path_idastar, cost_idastar = idastar(puzzle, start_state, goal_state, alpha=2, verbose=False)
    print(f"=> Lộ trình IDA* (Chi phí: {cost_idastar}):")
    print_path(path_idastar)


