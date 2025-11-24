"""
🌀 MAZE ADVENTURE 🌀

Hey there, adventurer! You're stuck in a twisty maze and need to find your way out.

HOW TO PLAY:
- Use W (up), S (down), A (left), D (right) to move around
- Look for the exit marked with 'E'
- Feeling lost? Just type 'solve' and I'll light up the quickest way out
- Type 'q' whenever you want to bail

Let's do this! 🚀
"""

from collections import deque
import os

# The maze map - feel free to design your own!
MAZE_MAP = [
    "###############",
    "#S   #  #     E#",
    "# ### ### #####",
    "#  # #   #  #  ",
    "### # ##### # #",
    "#   #      # # #",
    "# ##### # # # #",
    "#       #  # # ",
    "###############",
]

WALL = "#"
START = "S"
EXIT = "E"
YOU = "P"
BREADCRUMBS = "*"


def refresh_screen():
    """Clear the terminal for a cleaner look"""
    os.system("cls" if os.name == "nt" else "clear")


def setup_maze():
    """Get the maze ready and find where you start and where you need to go"""
    maze = [list(row) for row in MAZE_MAP]
    your_start = None
    the_exit = None

    for row_num, row in enumerate(maze):
        for col_num, spot in enumerate(row):
            if spot == START:
                your_start = (row_num, col_num)
            elif spot == EXIT:
                the_exit = (row_num, col_num)

    if not your_start or not the_exit:
        raise ValueError("Oops! The maze needs a starting point 'S' and an exit 'E'")

    return maze, your_start, the_exit


def show_maze(maze, where_you_are=None, hint_path=None):
    """Draw the maze on screen with your position and any hints"""
    hint_path = hint_path or set()

    for row_num, row in enumerate(maze):
        display = []
        for col_num, spot in enumerate(row):
            current_spot = (row_num, col_num)

            if where_you_are and current_spot == where_you_are:
                display.append(YOU)
            elif current_spot in hint_path and spot not in (START, EXIT):
                display.append(BREADCRUMBS)
            else:
                display.append(spot)
        print("".join(display))
    print("-" * max(len(r) for r in maze))


def find_way_out(maze, from_here, to_there):
    """Figure out the shortest path using some smart searching (BFS)"""
    spots_to_check = deque([from_here])
    how_we_got_here = {from_here: None}

    # Check in all four directions: right, up, down, left
    ways_to_go = [(0, 1), (-1, 0), (1, 0), (0, -1)]

    while spots_to_check:
        row, col = spots_to_check.popleft()
        current_spot = (row, col)

        # Found it!
        if current_spot == to_there:
            path = []
            backtrack = current_spot
            while backtrack:
                path.append(backtrack)
                backtrack = how_we_got_here[backtrack]
            return list(reversed(path))

        # Try moving in each direction
        for row_change, col_change in ways_to_go:
            new_row = row + row_change
            new_col = col + col_change
            next_spot = (new_row, new_col)

            # First check row in bounds
            if not (0 <= new_row < len(maze)):
                continue

            # Now check column within that specific row's length
            if not (0 <= new_col < len(maze[new_row])):
                continue

            # Can't go through walls or places we've been
            if next_spot in how_we_got_here or maze[new_row][new_col] == WALL:
                continue

            how_we_got_here[next_spot] = current_spot
            spots_to_check.append(next_spot)

    return None


def try_to_move(maze, current_pos, key_pressed):
    """Attempt to move based on what key you pressed"""
    controls = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}

    if key_pressed not in controls:
        return current_pos

    row_change, col_change = controls[key_pressed]
    new_row = current_pos[0] + row_change
    new_col = current_pos[1] + col_change

    # Check row bounds
    if not (0 <= new_row < len(maze)):
        return current_pos

    # Check column bounds for that row
    if not (0 <= new_col < len(maze[new_row])):
        return current_pos

    # Check if the move hits a wall
    if maze[new_row][new_col] == WALL:
        return current_pos

    return (new_row, new_col)


def play_game():
    """Main game - let's get lost in this maze!"""
    maze, starting_spot, exit_spot = setup_maze()
    where_you_are = starting_spot

    print("🌀 Welcome to Maze Adventure! 🌀")
    print("Loading your maze...")
    input("Press Enter when you're ready to start...")

    while True:
        refresh_screen()
        print("╔═══════════════════════════╗")
        print("║   🌀 MAZE ADVENTURE 🌀    ║")
        print("╚═══════════════════════════╝")
        print("Find the exit 'E' to escape!")
        print("Commands: W↑ S↓ A← D→ | 'solve' for help | 'q' to quit\n")

        show_maze(maze, where_you_are)

        # Did you make it out?
        if where_you_are == exit_spot:
            print("\n🎉 CONGRATULATIONS! You escaped the maze! 🎉")
            print("You're free! Well done, adventurer!")

            play_again = input("\nWant to try again? (y/n): ").lower().strip()
            if play_again == "y":
                maze, starting_spot, exit_spot = setup_maze()
                where_you_are = starting_spot
                continue
            else:
                print("\nThanks for playing! Come back anytime! 👋")
                break

        what_to_do = input("\nWhat's your move? ").lower().strip()

        if what_to_do == "q":
            print("\nLeaving so soon? See you next time! 👋")
            break

        elif what_to_do == "solve":
            refresh_screen()
            print("🤔 Let me think... finding the best route for you...\n")

            the_path = find_way_out(maze, where_you_are, exit_spot)

            if the_path:
                show_maze(maze, hint_path=set(the_path))
                steps = len(the_path) - 1
                print(f"\n✨ Found it! The shortest path is {steps} step{'s' if steps != 1 else ''} long.")
                print("Follow the asterisks (*) to find your way out!")
            else:
                print("😰 Uh oh... looks like there's no way out from here!")
                print("You might be trapped!")

            input("\nPress Enter to keep playing...")

        else:
            new_position = try_to_move(maze, where_you_are, what_to_do)

            # Bonked into a wall?
            if new_position == where_you_are and what_to_do in "wasd":
                print("\n💥 Ouch! You walked right into a wall!")
                print("Try a different direction.")
                input("Press Enter to continue...")

            where_you_are = new_position


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted! Thanks for playing! 👋")
    except Exception as e:
        print(f"\n😵 Oops! Something went wrong: {e}")
        print("Try running the game again!")