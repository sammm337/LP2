import heapq

# Define an Object class to represent rectangles/squares
class Object:
    def __init__(self, name, width, height):
        self.name = name
        self.w = width
        self.h = height

# Define a State class to represent the arrangement state
class State:
    def __init__(self, placed, remaining, room, cost):
        self.placed = placed        # Dictionary: object name -> (x, y, w, h)
        self.remaining = remaining  # List of unplaced Object instances
        self.room = room            # 2D grid representing room occupancy
        self.cost = cost            # g(n): area used so far

    def __lt__(self, other):
        # Needed for priority queue (heapq)
        return self.cost < other.cost

# Heuristic function h(n): how much estimated area is left to be filled
def heuristic(state, room_w, room_h):
    used = sum(w * h for _, (_, _, w, h) in state.placed.items())
    remaining = sum(obj.w * obj.h for obj in state.remaining)
    return (room_w * room_h - used - remaining)

# Check if placing object at (x, y) with dimensions (w, h) is valid (no overlap, fits in room)
def is_valid_placement(room, x, y, w, h):
    if x + w > len(room[0]) or y + h > len(room):
        return False
    for i in range(y, y + h):
        for j in range(x, x + w):
            if room[i][j] != 0:
                return False
    return True

# Place the object in the room grid (used to simulate placing it)
def place_object(room, x, y, w, h, val):
    for i in range(y, y + h):
        for j in range(x, x + w):
            room[i][j] = val

# A* Search algorithm
def a_star(objects, room_w, room_h):
    # Initialize empty room
    initial_room = [[0 for _ in range(room_w)] for _ in range(room_h)]
    initial_state = State({}, objects, initial_room, 0)

    open_set = []
    heapq.heappush(open_set, (0, initial_state))  # (f(n), state)

    while open_set:
        _, curr = heapq.heappop(open_set)

        # Goal: all objects placed
        if not curr.remaining:
            return curr.placed

        # Take the next unplaced object
        next_obj = curr.remaining[0]

        # Try placing it at all positions with both orientations (if rectangle)
        for y in range(room_h):
            for x in range(room_w):
                for (w, h) in [(next_obj.w, next_obj.h), (next_obj.h, next_obj.w)]:
                    if is_valid_placement(curr.room, x, y, w, h):
                        # Clone room and place the object
                        new_room = [row[:] for row in curr.room]
                        place_object(new_room, x, y, w, h, 1)

                        # Update placed and remaining objects
                        new_placed = curr.placed.copy()
                        new_placed[next_obj.name] = (x, y, w, h)
                        new_state = State(
                            new_placed,
                            curr.remaining[1:],  # remove current object from list
                            new_room,
                            curr.cost + (w * h)
                        )

                        # f(n) = g(n) + h(n)
                        f_score = new_state.cost + heuristic(new_state, room_w, room_h)
                        heapq.heappush(open_set, (f_score, new_state))

    return None  # No solution found

# Main function to run the placement
if __name__ == "__main__":
    # Define 5 rectangular and 4 square objects with names and dimensions
    objects = [
        Object("R1", 4, 2), Object("R2", 3, 2),
        Object("R3", 2, 5), Object("R4", 3, 3),
        Object("R5", 5, 1),
        Object("S1", 2, 2), Object("S2", 2, 2),
        Object("S3", 2, 2), Object("S4", 2, 2),
    ]

    room_width = 10
    room_height = 10

    result = a_star(objects, room_width, room_height)

    if result:
        print("Objects placed at the following positions (x, y, width, height):\n")
        for name, (x, y, w, h) in result.items():
            print(f"{name}: Position ({x}, {y}), Size ({w}x{h})")
    else:
        print("No valid arrangement found.")
