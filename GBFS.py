from queue import PriorityQueue
import pygame

def gbfsVisualizer(draw, grid, start, end, heuristic):
    """
    Greedy Best-First Search Implementation.
    Evaluates nodes purely based on their heuristic distance to the goal.
    f(n) = h(n)
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    
    open_set_hash = {start} 
    closed_set = set()    
    nodes_expanded = 0
    
    while not open_set.empty():
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
            
        closed_set.add(current)
        
        # Explore neighbors
        for neighbor in current.neighbors:
            if neighbor in closed_set:
                continue

            if neighbor not in open_set_hash:
                neighbor.parent = current
                count += 1
                
                # GBFS logic: f(n) = h(n)
                h_score = heuristic(neighbor.getPos(), end.getPos())
                
                open_set.put((h_score, count, neighbor))
                open_set_hash.add(neighbor)
                
                # Visually mark as a frontier (Open) node
                if neighbor != end and neighbor != start:
                    neighbor.makeOpen()
                    
        nodes_expanded += 1
        draw()

        if current != start:
            current.makeClosed()
    return None, nodes_expanded