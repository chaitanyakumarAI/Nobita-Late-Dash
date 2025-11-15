# 🎮 Nobita's Late Dash - A* Pathfinding Game

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

An educational game demonstrating **A* pathfinding algorithm** with **heuristic optimization** using gadgets from the popular anime *Doraemon*. Help Nobita reach school on time while avoiding Gian and using gadgets strategically!

---

## 📋 Table of Contents
- [Features](#features)
- [Core Concepts](#core-concepts)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Mechanics](#game-mechanics)
- [Controls](#controls)
- [Project Structure](#project-structure)
- [Technical Implementation](#technical-implementation)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## ✨ Features

- **A* Pathfinding Algorithm** - Real-time optimal path calculation
- **Gadgets as Heuristics** - Bamboo Copter and Anywhere Door modify pathfinding costs
- **Intelligent AI** - Gian switches between patrol and chase modes
- **3 Progressive Levels** - Increasing difficulty with complex mazes
- **Move Limit System** - Strategic resource management
- **Star Rating** - Performance-based scoring (1-3 stars)
- **Polished UI** - Smooth animations, gradients, and visual feedback
- **Visual A* Exploration** - See the algorithm work in real-time

---

## 🧠 Core Concepts

### A* Algorithm Implementation
The game demonstrates A* pathfinding where:
- **g(n)** = Actual cost from start to node n
- **h(n)** = Heuristic estimate from n to goal
- **f(n) = g(n) + h(n)** = Total estimated cost

### Gadgets as Heuristics

#### 🚁 Bamboo Copter
- **Effect:** Reduces move cost by 50% (each step costs 0.5 moves instead of 1.0)
- **Implementation:** Modifies the cost function in A*
- **Strategy:** Collect early to maximize efficiency

#### 🚪 Anywhere Door
- **Effect:** Creates teleportation edges in the graph
- **Implementation:** Adds new neighbors to nodes in pathfinding
- **Strategy:** Use to skip maze sections and save moves

### Intelligent Enemy AI
Gian's behavior:
- **Patrol Mode:** Follows predefined waypoints when far from player
- **Chase Mode:** Actively pursues Nobita when within 8 cells
- **Wall Avoidance:** Smart pathfinding that respects obstacles

---

## 🚀 Installation

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
```

### Setup
1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/nobitas-late-dash.git
cd nobitas-late-dash
```

2. **Install dependencies:**
```bash
pip install pygame
```

3. **Run the game:**
```bash
python main.py
```

---

## 🎮 How to Play

### Objective
Help Nobita reach school (green target) within the move limit while avoiding Gian (red enemy).

### Getting Started
1. Press **ENTER** on the main menu to start Level 1
2. Use **SPACE** to calculate the optimal path using A*
3. Use **Arrow Keys** for manual movement or **A** for auto-move
4. Collect gadgets to enhance your pathfinding capabilities
5. Complete all 3 levels with the best score!

---

## 🎯 Game Mechanics

### Move System
- **Move Limit:** Each level has a maximum number of moves
- **Optimal Moves:** Target number for 3-star rating
- **Fractional Moves:** With Bamboo Copter active, moves are counted in decimals (e.g., 0.5, 1.5, 2.0)

### Star Rating
- **⭐⭐⭐ (3 Stars):** Complete within optimal moves
- **⭐⭐ (2 Stars):** Complete within optimal + 5 moves
- **⭐ (1 Star):** Complete within move limit

### Gadget Collection
1. **Walk over yellow square** to collect Bamboo Copter
2. **Walk onto purple square** to teleport via Anywhere Door (automatic)
3. **Press B** to toggle Bamboo Copter ON/OFF after collecting

---

## 🎛️ Controls

| Key | Action |
|-----|--------|
| **SPACE** | Calculate optimal path with A* |
| **A** | Auto-move along calculated path |
| **B** | Toggle Bamboo Copter ON/OFF |
| **Arrow Keys** | Manual movement (↑↓←→) |
| **R** | Reset current level |
| **N** | Next level (after winning) |
| **ESC** | Return to main menu |

### Button Controls
- **Find Path** - Calculate A* path
- **Auto Move** - Execute automatic movement
- **Bamboo ON/OFF** - Toggle gadget effect
- **Reset** - Restart level

---

## 📁 Project Structure

```
nobitas-late-dash/
├── main.py                          # Main game loop and logic
├── astar.py                         # A* pathfinding implementation
├── grid.py                          # Grid management and rendering
├── entities.py                      # Game entities (Nobita, Gian, etc.)
├── constants.py                     # Game constants and configurations
├── README.md                        # This file
└── assets/                          # (Optional) Game assets
    └── screenshots/                 # Game screenshots
```

### File Descriptions

**main.py**
- Game initialization and main loop
- Event handling (keyboard/mouse)
- UI rendering and game state management
- Level loading and progression

**astar.py**
- A* pathfinding algorithm
- Heuristic calculations
- Door teleportation graph edges
- Cost function modifications (Bamboo effect)

**grid.py**
- Grid data structure
- Cell type management
- Path visualization
- Map loading from strings

**entities.py**
- Nobita (player) class
- School (goal) class
- Gian (enemy) with AI
- Gadget classes (BambooCopter, AnywhereDoor)

**constants.py**
- Screen dimensions
- Colors
- Cell types
- Game parameters

---

## 🔧 Technical Implementation

### A* Pathfinding
```python
def find_path(start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while not frontier.empty():
        current = frontier.get()[1]
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        for next_node in get_neighbors(current):
            new_cost = cost_so_far[current] + get_cost(current, next_node)
            
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, goal)
                frontier.put((priority, next_node))
                came_from[next_node] = current
    
    return None
```

### Gadget Integration

**Bamboo Copter Cost Modification:**
```python
def get_movement_cost(from_pos, to_pos):
    base_cost = 1.0
    if bamboo_collected:
        base_cost = 0.5  # 50% reduction!
    return base_cost
```

**Anywhere Door Graph Addition:**
```python
def get_neighbors_with_doors(row, col):
    neighbors = get_regular_neighbors(row, col)
    
    # Add teleportation edges
    for door1, door2 in door_pairs:
        if (row, col) == door1:
            neighbors.append((door2[0], door2[1], 1.0))
        elif (row, col) == door2:
            neighbors.append((door1[0], door1[1], 1.0))
    
    return neighbors
```

### Gian AI with Wall Collision
```python
def move_toward_target(target, grid):
    # Calculate preferred directions
    directions = []
    if self.row < target[0]:
        directions.append((1, 0))  # Down
    elif self.row > target[0]:
        directions.append((-1, 0))  # Up
    
    # Try each direction with wall checking
    for dr, dc in directions:
        new_row, new_col = self.row + dr, self.col + dc
        if grid.is_walkable(new_row, new_col):
            self.row, self.col = new_row, new_col
            return
```

---

## 📸 Screenshots

### Main Menu
![Main Menu](assets/screenshots/menu.png)

### Gameplay - Level 1
![Level 1](assets/screenshots/level1.png)

### A* Pathfinding Visualization
![Pathfinding](assets/screenshots/pathfinding.png)

### Victory Screen
![Victory](assets/screenshots/victory.png)

---

## 🎨 Customization

### Changing Gadget Positions
Edit the level map in `main.py`:
```python
"map": [
    "####################",
    "#N.................#",
    "#.###.........G....#",
    "#.#.#.............S#",
    "#.#.#.....B........#",  # B = Bamboo position
    "#..................#",
    "#....D.....D.......#",  # D = Door positions
]
```

### Adjusting Difficulty
Modify in level definitions:
```python
"max_moves": 40,        # Move limit
"optimal_moves": 20,    # Target for 3 stars
"gian_speed": 1.5,      # Gian movement speed
```

### Door Pairs
```python
"door_pairs": [((7, 5), (7, 11))]  # (row, col) pairs
```

---

## 🚀 Future Enhancements

- [ ] More levels with increasing complexity
- [ ] Additional gadgets (Time Machine, Shrink Ray)
- [ ] Level editor for custom maps
- [ ] Leaderboard and time tracking
- [ ] Sound effects and background music
- [ ] Web deployment (HTML5/JavaScript version)
- [ ] Multiplayer mode
- [ ] Mobile controls support

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Add comments for complex algorithms
- Test all features before submitting
- Update README for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Chaitanya Kumar Ranga**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com
- Institution: Indian Institute of Technology Bhilai

---

## 🙏 Acknowledgments

- **Doraemon** franchise for character inspiration
- **IIT Bhilai** for academic guidance
- **Pygame** community for excellent documentation
- A* algorithm resources and tutorials

---

## 📊 Project Stats

- **Language:** Python
- **Framework:** Pygame
- **Lines of Code:** ~2000+
- **Development Time:** [Your timeline]
- **Levels:** 3
- **Features:** 10+

---

## 🎓 Educational Value

This project demonstrates:
- **Data Structures:** Priority queues, graphs, dictionaries
- **Algorithms:** A* pathfinding, heuristic search
- **Game Development:** Event loops, rendering, animation
- **AI:** State machines, pathfinding, behavior trees
- **Software Engineering:** Modular design, clean code practices

---

## 📞 Support

If you encounter any issues or have questions:
- Open an [Issue](https://github.com/yourusername/nobitas-late-dash/issues)
- Email: your.email@example.com
- Check existing [Discussions](https://github.com/yourusername/nobitas-late-dash/discussions)

---

## ⭐ Show Your Support

If you found this project helpful or interesting, please give it a star! ⭐

---

**Made with ❤️ by Chaitanya Kumar Ranga**

**"Help Nobita reach school on time!"** 🏃‍♂️💨
