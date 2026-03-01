from queue import PriorityQueue
import pygame

def astarVisualizer(draw, grid, start, end, heuristic):
    """
    A* Search Implementation.
    Evaluates nodes based on actual path cost + heuristic distance.
    f(n) = g(n) + h(n)
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    
    open_set_hash = {start}

    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = heuristic(start.getPos(), end.getPos())
    
    nodes_expanded = 0
    
    while not open_set.empty():
        # Allow exiting during computation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, nodes_expanded
                
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        # Goal Check
        if current == end:
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = temp.parent
            return path[::-1], nodes_expanded
            
        # Explore neighbors
        for neighbor in current.neighbors:
            tentative_g_score = g_score[current] + 1
            
            # If we found a strictly shorter path to this neighbor
            if tentative_g_score < g_score[neighbor]:
                neighbor.parent = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor.getPos(), end.getPos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    
                    if neighbor != end and neighbor != start:
                        neighbor.makeOpen()
                        
        nodes_expanded += 1
        draw() 
        
        if current != start:
            current.makeClosed()

    return None, nodes_expanded