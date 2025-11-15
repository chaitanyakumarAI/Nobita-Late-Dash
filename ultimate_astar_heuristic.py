"""
ULTIMATE A* Implementation with Gadgets as Heuristics
Bamboo Copter = reduces path length
Anywhere Door = teleportation nodes in graph
"""

import heapq
import math
from constants import *


class UltimateAStar:
    """
    Advanced A* with gadgets integrated as heuristics
    - Bamboo Copter: Reduces move cost (not animation)
    - Anywhere Door: Graph node that enables teleportation
    - Dynamic replanning based on Gian position
    """

    def __init__(self, grid):
        self.grid = grid
        self.bamboo_collected = False
        self.door_positions = []  # List of door pairs

    def heuristic(self, pos1, pos2):
        """
        Enhanced Manhattan distance
        Considers potential shortcuts via doors
        """
        row1, col1 = pos1
        row2, col2 = pos2

        # Base Manhattan distance
        base_dist = abs(row1 - row2) + abs(col1 - col2)

        # Check if using a door would be shorter
        if self.door_positions:
            min_door_dist = base_dist

            for door1, door2 in self.door_positions:
                # Distance to door1 + teleport + door2 to goal
                dist_via_door1 = (abs(row1 - door1[0]) + abs(col1 - door1[1]) + 
                                 abs(door2[0] - row2) + abs(door2[1] - col2) + 1)

                # Distance to door2 + teleport + door1 to goal  
                dist_via_door2 = (abs(row1 - door2[0]) + abs(col1 - door2[1]) + 
                                 abs(door1[0] - row2) + abs(door1[1] - col2) + 1)

                min_door_dist = min(min_door_dist, dist_via_door1, dist_via_door2)

            return min_door_dist

        return base_dist

    def get_movement_cost(self, from_pos, to_pos):
        """
        Calculate actual movement cost
        Bamboo Copter reduces MOVE COUNT, not just animation speed
        """
        base_cost = 1.0

        # If Bamboo Copter collected, moves cost LESS
        # This means path will be "shorter" in terms of moves!
        if self.bamboo_collected:
            base_cost = 0.5  # Each move counts as 0.5 moves!

        # Penalty for being near Gian
        if self.grid.gian_pos:
            gian_row, gian_col = self.grid.gian_pos
            to_row, to_col = to_pos

            distance_to_gian = abs(to_row - gian_row) + abs(to_col - gian_col)

            if distance_to_gian <= GIAN_DANGER_RADIUS:
                # Add cost to discourage going near Gian
                base_cost += GIAN_PROXIMITY_COST * (GIAN_DANGER_RADIUS - distance_to_gian + 1)

        return base_cost

    def get_neighbors_with_doors(self, row, col):
        """
        Get neighbors INCLUDING teleportation via doors
        This makes doors part of the graph structure!
        """
        neighbors = []

        # Regular neighbors (4 cardinal directions)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if self.grid.is_walkable(new_row, new_col):
                cost = self.get_movement_cost((row, col), (new_row, new_col))
                neighbors.append((new_row, new_col, cost))

        # TELEPORTATION: If standing on a door, can teleport!
        for door1, door2 in self.door_positions:
            if (row, col) == door1:
                # Can teleport to door2 for cost of 1 move
                teleport_cost = 1.0 if not self.bamboo_collected else 0.5
                neighbors.append((door2[0], door2[1], teleport_cost))
                print(f"🚪 Teleport available: {door1} → {door2}")
            elif (row, col) == door2:
                # Can teleport to door1
                teleport_cost = 1.0 if not self.bamboo_collected else 0.5
                neighbors.append((door1[0], door1[1], teleport_cost))
                print(f"🚪 Teleport available: {door2} → {door1}")

        return neighbors

    def find_path(self, start, goal, record_exploration=True):
        """
        Enhanced A* with door teleportation and gadget heuristics
        """
        if not self.grid.in_bounds(*start) or not self.grid.in_bounds(*goal):
            return None

        if not self.grid.is_walkable(*goal):
            return None

        # Priority queue: (f_cost, counter, position)
        counter = 0
        frontier = []
        heapq.heappush(frontier, (0, counter, start))

        came_from = {start: None}
        cost_so_far = {start: 0}
        explored_set = set()

        nodes_explored = 0

        while frontier:
            current_f, _, current = heapq.heappop(frontier)
            nodes_explored += 1

            if record_exploration:
                explored_set.add(current)

            # Goal reached
            if current == goal:
                if record_exploration:
                    self.grid.explored = explored_set

                path = self._reconstruct_path(came_from, start, goal)

                # Calculate actual move count
                actual_moves = self._calculate_actual_moves(path)

                print(f"✓ A* Stats:")
                print(f"  Nodes explored: {nodes_explored}")
                print(f"  Path length: {len(path)-1} steps")
                print(f"  Actual moves: {actual_moves}")
                print(f"  Bamboo active: {self.bamboo_collected}")

                return path

            # Explore neighbors WITH door teleportation
            for neighbor_row, neighbor_col, move_cost in self.get_neighbors_with_doors(*current):
                neighbor = (neighbor_row, neighbor_col)

                new_cost = cost_so_far[current] + move_cost

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    counter += 1
                    heapq.heappush(frontier, (priority, counter, neighbor))
                    came_from[neighbor] = current

        # No path found
        if record_exploration:
            self.grid.explored = explored_set

        print(f"✗ No path found! Explored {nodes_explored} nodes.")
        return None

    def _reconstruct_path(self, came_from, start, goal):
        """Reconstruct path from came_from dictionary"""
        path = []
        current = goal

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path

    def _calculate_actual_moves(self, path):
        """
        Calculate how many moves this path costs
        With bamboo, each step costs 0.5 moves
        """
        if not path:
            return 0

        if self.bamboo_collected:
            # Each step costs 0.5 moves
            return (len(path) - 1) * 0.5
        else:
            return len(path) - 1

    def set_bamboo_collected(self, collected):
        """
        Mark bamboo as collected
        This changes pathfinding costs!
        """
        self.bamboo_collected = collected
        if collected:
            print("🚁 A* now uses Bamboo heuristic: 0.5x move cost!")

    def add_door_pair(self, pos1, pos2):
        """Add teleportation door pair"""
        if (pos1, pos2) not in self.door_positions and (pos2, pos1) not in self.door_positions:
            self.door_positions.append((pos1, pos2))
            print(f"🚪 Door pair added: {pos1} ↔ {pos2}")

    def reset_gadgets(self):
        """Reset gadget states"""
        self.bamboo_collected = False
        self.door_positions = []
