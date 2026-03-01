import pygame
import random
import math
import time

# Placeholders for the algorithms we will write next
from gbfs import gbfsVisualizer
from astar import astarVisualizer

WIDTH = 600
HEIGHT = 800 # Increased height to make room for the expanded metrics dashboard
ROWS = 20
UI_HEIGHT = 200

pygame.font.init()
STAT_FONT = pygame.font.SysFont('arial', 20, bold=True)
LEGEND_FONT = pygame.font.SysFont('arial', 14)
TITLE_FONT = pygame.font.SysFont('arial', 16, bold=True)
METRIC_FONT = pygame.font.SysFont('arial', 14, bold=True)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("INFORMED SEARCHES & DYNAMIC PATHFINDING")

# Colors
RED = (255, 65, 54)
GREEN = (46, 204, 64)
BLUE = (0, 116, 217)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
TURQUOISE = (64, 224, 208)
GREY = (128, 128, 128)
PURPLE = (177, 13, 201)
ORANGE = (255, 133, 27) # For the moving agent

class Node:
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.parent = None 
        self.neighbors = []
        self.totalRows = totalRows

    def getPos(self): return self.row, self.col
    def isWall(self): return self.color == BLACK
    
    def reset(self): 
        self.color = WHITE
        self.parent = None
        
    def makeStart(self): self.color = TURQUOISE
    def makeWall(self): self.color = BLACK
    def makeEnd(self): self.color = YELLOW
    def makeClosed(self): self.color = RED
    def makeOpen(self): self.color = GREEN
    def makePath(self): self.color = BLUE
    def makeAgent(self): self.color = ORANGE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        self.neighbors = []
        # UP, RIGHT, DOWN, LEFT
        if self.row > 0 and not grid[self.row - 1][self.col].isWall():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isWall():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isWall():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].isWall():
            self.neighbors.append(grid[self.row][self.col - 1])

# --- HEURISTICS ---
def h_manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def h_euclidean(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def drawGrid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def drawUI(win, width, statusText, algoName, heuristicName, dynamicMode, metrics):
    uiBgColor = (235, 235, 235) 
    pygame.draw.rect(win, uiBgColor, (0, width, width, UI_HEIGHT))
    pygame.draw.line(win, (50, 50, 50), (0, width), (width, width), 2) 

    # Left Column: Status & Setup
    algoSurface = STAT_FONT.render(f"Algo: {algoName} | H: {heuristicName}", True, (0, 50, 150)) 
    win.blit(algoSurface, (15, width + 15))
    
    dynColor = GREEN if dynamicMode else RED
    dynText = STAT_FONT.render(f"Dynamic Mode: {'ON' if dynamicMode else 'OFF'}", True, dynColor)
    win.blit(dynText, (15, width + 45))

    statusSurface = LEGEND_FONT.render(f"Status: {statusText}", True, BLACK)
    win.blit(statusSurface, (15, width + 75))

    # Middle Column: Controls
    pygame.draw.line(win, (180, 180, 180), (300, width + 10), (300, width + 190), 2) 
    ctrlTitle = TITLE_FONT.render("Controls", True, (50, 50, 50))
    win.blit(ctrlTitle, (315, width + 10))
    
    controls = [
        "1: GBFS  |  2: A* Search",
        "M: Manhattan | E: Euclidean",
        "R: Random Maze (30% Walls)",
        "D: Toggle Dynamic Mode",
        "Space: Start / Re-plan",
        "C: Clear Board"
    ]
    for i, ctrl in enumerate(controls):
        text = LEGEND_FONT.render(ctrl, True, BLACK)
        win.blit(text, (315, width + 35 + (i * 20)))

    # Right Column: Metrics & Legend
    pygame.draw.line(win, (180, 180, 180), (480, width + 10), (480, width + 190), 2) 
    metTitle = TITLE_FONT.render("Metrics", True, (50, 50, 50))
    win.blit(metTitle, (490, width + 10))
    
    nodesTxt = METRIC_FONT.render(f"Nodes: {metrics['nodes']}", True, PURPLE)
    costTxt = METRIC_FONT.render(f"Cost: {metrics['cost']}", True, BLUE)
    timeTxt = METRIC_FONT.render(f"Time: {metrics['time']:.2f} ms", True, (0, 100, 0))
    
    win.blit(nodesTxt, (490, width + 35))
    win.blit(costTxt, (490, width + 55))
    win.blit(timeTxt, (490, width + 75))

def draw(win, grid, rows, width, status, algoName, heuristicName, dynamicMode, metrics):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    drawGrid(win, rows, width)
    drawUI(win, width, status, algoName, heuristicName, dynamicMode, metrics)
    pygame.display.update()

def getClickedPos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def clearSearch(grid):
    for row in grid:
        for node in row:
            if node.color in {RED, GREEN, BLUE, ORANGE}:
                node.reset()
            node.parent = None

def generateRandomMaze(grid, start, end, density=0.3):
    for row in grid:
        for node in row:
            if node != start and node != end:
                node.reset()
                if random.random() < density:
                    node.makeWall()

def spawnDynamicObstacle(grid, start, end):
    # Try to spawn an obstacle in an empty spot
    empty_nodes = [n for row in grid for n in row if n.color == WHITE and n != start and n != end]
    if empty_nodes:
        new_wall = random.choice(empty_nodes)
        new_wall.makeWall()
        return new_wall
    return None

def drawPath(path_nodes, drawFunc):
    for node in path_nodes:
        if node.color != TURQUOISE and node.color != YELLOW:
            node.makePath()
            drawFunc()

def main(win, width):
    grid = makeGrid(ROWS, width)
    start = None
    end = None
    run = True
    
    currentAlgo = None
    algoName = "Select (1/2)"
    currentHeuristic = h_manhattan
    heuristicName = "Manhattan"
    dynamicMode = False
    statusText = "Setup Board -> Select Algo -> Press Space"
    
    metrics = {"nodes": 0, "cost": 0, "time": 0.0}

    while run:
        draw(win, grid, ROWS, width, statusText, algoName, heuristicName, dynamicMode, metrics)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT CLICK
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    row, col = getClickedPos(pos, ROWS, width)
                    node = grid[row][col]
                    if not start and node != end and not node.isWall():
                        start = node
                        start.makeStart()
                    elif not end and node != start and not node.isWall():
                        end = node
                        end.makeEnd()
                    elif node != start and node != end:
                        node.makeWall()

            elif pygame.mouse.get_pressed()[2]: # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    row, col = getClickedPos(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start: start = None
                    elif node == end: end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    currentAlgo = gbfsVisualizer
                    algoName = "GBFS"
                elif event.key == pygame.K_2:
                    currentAlgo = astarVisualizer
                    algoName = "A* Search"
                elif event.key == pygame.K_m:
                    currentHeuristic = h_manhattan
                    heuristicName = "Manhattan"
                elif event.key == pygame.K_e:
                    currentHeuristic = h_euclidean
                    heuristicName = "Euclidean"
                elif event.key == pygame.K_d:
                    dynamicMode = not dynamicMode
                elif event.key == pygame.K_r:
                    generateRandomMaze(grid, start, end)
                    statusText = "Random Maze Generated."
                
                if event.key == pygame.K_SPACE and start and end and currentAlgo:
                    agent_pos = start
                    path_found = False
                    
                    # Core Loop for Pathfinding & Agent Movement
                    while agent_pos != end:
                        for row in grid:
                            for node in row:
                                node.updateNeighbors(grid)

                        clearSearch(grid)
                        updateDisplay = lambda: draw(win, grid, ROWS, width, "Searching...", algoName, heuristicName, dynamicMode, metrics)
                        
                        start_time = time.perf_counter()
                        # Expecting algorithms to return a tuple: (list_of_path_nodes, int_nodes_expanded)
                        path_nodes, expanded = currentAlgo(updateDisplay, grid, agent_pos, end, currentHeuristic)
                        end_time = time.perf_counter()
                        
                        if path_nodes:
                            metrics["time"] = (end_time - start_time) * 1000
                            metrics["nodes"] = expanded
                            metrics["cost"] = len(path_nodes) - 1
                            drawPath(path_nodes, updateDisplay)
                            statusText = "Path Found. Agent moving..."
                            
                            # Agent Movement Simulation
                            interrupted = False
                            for step_node in path_nodes[1:]: # Skip current agent pos
                                pygame.time.delay(200) # Agent movement speed
                                
                                # Move agent visually
                                agent_pos.makePath() # leave trail
                                agent_pos = step_node
                                agent_pos.makeAgent()
                                draw(win, grid, ROWS, width, statusText, algoName, heuristicName, dynamicMode, metrics)
                                
                                # Dynamic Obstacle Logic
                                if dynamicMode and random.random() < 0.15: # 15% chance per step
                                    new_wall = spawnDynamicObstacle(grid, start, end)
                                    if new_wall:
                                        # Check if obstacle blocked our current calculated path
                                        if new_wall in path_nodes:
                                            statusText = "Path Blocked! Re-planning..."
                                            draw(win, grid, ROWS, width, statusText, algoName, heuristicName, dynamicMode, metrics)
                                            pygame.time.delay(500)
                                            interrupted = True
                                            break # Break movement loop, goes back to outer while loop to search again
                            
                            if not interrupted:
                                agent_pos = end # Reached target
                                statusText = "Success! Target Reached."
                                break
                        else:
                            statusText = "Failed. No Path Exists."
                            break

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = makeGrid(ROWS, width)
                    metrics = {"nodes": 0, "cost": 0, "time": 0.0}
                    statusText = "Board Cleared."

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)