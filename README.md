# AI-project: AI Algorithms for Pathfinding, Game AI, and Reinforcement Learning  

## Overview  
This repository contains implementations of **AI algorithms** across three major domains:  

1. **Reinforcement Learning (RL) & Dynamic Programming (DP)** : Training a simulated **crawler robot** to move using policy iteration & Q-learning.  
2. **Game AI (Othello AI Players)** – Implementing **Minimax, Monte Carlo Tree Search (MCTS), and Random AI** to play Othello.  
3. **Pathfinding AI for Robot Navigation** – Finding **optimal paths in grid-based worlds** using BFS, DFS, A*, Beam Search, and Local Search.  

Each project demonstrates **core AI techniques** used in robotics, game AI, and heuristic search.  

---
## Implemented AI Projects  

### **1. Reinforcement Learning & Dynamic Programming - Crawler Robot**  
**Goal:** Train a **crawler robot** in a **Markov Decision Process (MDP)** environment to learn movement.  

**Algorithms Implemented:**  
1.**Policy Iteration (Dynamic Programming)** – Computes an optimal policy **offline** through iterative policy evaluation and extraction.  
2.**Q-Learning (Reinforcement Learning)** – Learns an optimal policy **online** using **ε-greedy exploration** and Q-value updates.  

**Technologies Used:** **Python**, **NumPy**, **MDP modeling**, **Policy Iteration**, **Q-Learning**  

**How to Run:**  
python crawler.py  
For q-learning method: python crawler.py -q  

### **2. Othello AI Players - Minimax, MCTS, and Random AI**
**Goal:** Develop several AI players that can play Othello using different decision-making strategies.  

**Algorithms Implemented:**  
1.**Minimax and Alpha-Beta Pruning:** Searches the game tree for the best possible move while reducing unnecessary exploration.  
2.**Monte Carlo Tree Search:** Uses random simulations & Upper Confidence Bounds (UCT) to make decisions.  
3.**Random Player:** Picks random valid moves (used as a baseline for comparison).  

**Technologies Used:** Python, Game AI, Tree Search (Minimax, MCTS)  

**How to Run:**  
python othello.py -p1 minimax -p2 random  # Minimax vs. Random AI  
python othello.py -p1 mcts -p2 random     # MCTS vs. Random AI  
python othello.py -p1 random -p2 random   # Random AI vs. Random AI  

### **3. Pathfinding AI - Robot Navigation in Grid Worlds**  
 **Goal:** Find a **valid path** for a **robot navigating different terrains** using search algorithms.  

**Algorithms Implemented:**  
1.**Depth-First Search (DFS):** Explores deep paths first (**not necessarily optimal**).  
2.**Breadth-First Search (BFS):** Finds the **shortest path in terms of steps**.   
3.**A-star Search:** Finds the **lowest-cost path** using `g + h` (cost + heuristic).  
4.**Beam Search:** Limits the number of nodes explored (may miss the best path).  
5.**Local Search (Hill Climbing-like approach)** Moves greedily toward the goal.  

**Supported Heuristics:**  
**Manhattan Distance** – `h = |x1 - x2| + |y1 - y2|`  
**Euclidean Distance** – `h = sqrt((x1 - x2)² + (y1 - y2)²)`

**Technologies Used:**  **Python**, **NumPy**, **Priority Queues**, **Graph Search Algorithms**  

**How to run:**  
python main.py worlds world_id -e heuristic -b beam_width -a animation_option  
Animation_option: 1 (Expanded nodes) 2 (Path)  
Heuristic option: 1,3 (Manhattan) 2,4 (Euclidean)  
If wants BFS/DFS path: python main.py worlds 1 -a 2 (only needs world_id and animation_option)  
example: python main.py worlds 1 -e 1 -b 50 -a 2
