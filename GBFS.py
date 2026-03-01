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
    # Queue stores: (f_score, insertion_count, node)
    # The count ensures we have a tie-breaker if two nodes have the same f_score,
    # preventing Python from trying to compare two Node objects directly.
    open_set.put((0, count, start))
    
    open_set_hash = {start}  # For fast lookup of what's in the priority queue
    closed_set = set()       # To keep track of visited nodes and prevent cycles
    
    nodes_expanded = 0
    
    while not open_set.empty():
        # Allow the user to quit the window even while the algorithm is computing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, nodes_expanded
                
        # Pop the node with the lowest heuristic score
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        # Goal Check
        if current == end:
            # Path found! Reconstruct it by following the parent pointers
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = temp.parent
            # The path is constructed backwards (end to start), so we reverse it
            return path[::-1], nodes_expanded
            
        closed_set.add(current)
        
        # Explore neighbors
        for neighbor in current.neighbors:
            # Skip if we've already visited this node fully
            if neighbor in closed_set:
                continue
                
            # If it's a new frontier node, evaluate and add it
            if neighbor not in open_set_hash:
                neighbor.parent = current  # Set parent for path reconstruction
                count += 1
                
                # GBFS logic: f(n) = h(n)
                h_score = heuristic(neighbor.getPos(), end.getPos())
                
                open_set.put((h_score, count, neighbor))
                open_set_hash.add(neighbor)
                
                # Visually mark as a frontier (Open) node
                if neighbor != end and neighbor != start:
                    neighbor.makeOpen()
                    
        nodes_expanded += 1
        draw() # Update the Pygame display
        
        # Visually mark as an explored (Closed) node
        if current != start:
            current.makeClosed()
            
    # If the queue empties and no path is found
    return None, nodes_expanded