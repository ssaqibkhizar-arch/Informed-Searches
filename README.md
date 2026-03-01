# Dynamic Pathfinding Agent - Informed Searches

**Author:** Saqib Ali  
**Roll Number:** 24P-0726  
**Repository Link:** [https://github.com/ssaqibkhizar-arch/Informed-Searches](https://github.com/ssaqibkhizar-arch/Informed-Searches)

## Project Overview
This project is a Python-based interactive GUI application built with Pygame. It visualizes and simulates a **Dynamic Pathfinding Agent** navigating a grid-based environment using **Informed Search Algorithms**. 

The agent is capable of finding the optimal or sub-optimal path to a target and includes a **Dynamic Mode**, where random obstacles can spawn in real-time while the agent is moving. If the path is blocked, the agent immediately detects the collision and recalculates a new path from its current position.

### Features
- **Algorithms Implemented:**
  - Greedy Best-First Search (GBFS)
  - A* Search (A-Star)
- **Heuristics:** Manhattan Distance & Euclidean Distance
- **Dynamic Re-planning:** Real-time obstacle spawning and path recalculation
- **Random Map Generation:** Instantly generate mazes with a 30% wall density
- **Customizable Grid:** Define your own grid dimensions via the terminal before launching the GUI
- **Live Metrics Dashboard:** Tracks Nodes Expanded, Path Cost, and Execution Time (in milliseconds)

---

## Requirements and Dependencies

- Python 3.x
- `pygame` library

### Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ssaqibkhizar-arch/Informed-Searches.git