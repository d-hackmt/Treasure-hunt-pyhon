import streamlit as st
import pandas as pd

# Initialize the player's position and game state using session state variables
if "player_position" not in st.session_state:
    st.session_state["player_position"] = [0, 0]
if "game_over" not in st.session_state:
    st.session_state["game_over"] = False
    
from util import  set_background


set_background('bg.png')

# Define the map layout with clues and a treasure
map_layout = [
    ["Start", "Empty", "Clue"],
    ["Empty", "Clue", "Empty"],
    ["Empty", "Empty", "Treasure"]
]

# Display game instructions
def display_instructions():
    st.title("🏴‍☠️ Treasure Hunt Game!")
    st.write("Navigate through the grid to find the hidden treasure.")
    st.write("Use the navigation buttons below to move up, down, left, or right.")
    st.write("Your current position is marked with '🚶'.")
    st.write("Good luck!\n")

# Update player position based on the direction
def update_position(direction):
    if st.session_state["game_over"]:
        return

    x, y = st.session_state["player_position"]

    if direction == "Up" and x > 0:
        st.session_state["player_position"][0] -= 1
    elif direction == "Down" and x < len(map_layout) - 1:
        st.session_state["player_position"][0] += 1
    elif direction == "Left" and y > 0:
        st.session_state["player_position"][1] -= 1
    elif direction == "Right" and y < len(map_layout[0]) - 1:
        st.session_state["player_position"][1] += 1

    check_location()  # Check location after each move

# Check player's current location and give feedback
def check_location():
    x, y = st.session_state["player_position"]
    location = map_layout[x][y]
    if location == "Clue":
        st.success("You found a clue! Keep searching.")
    elif location == "Treasure":
        st.success("🎉 Congratulations! You found the treasure!")
        st.balloons()
        restart_game()  # Automatically restart after finding the treasure
    else:
        st.info("There's nothing here. Keep moving.")

# Reset the game state
def restart_game():
    st.session_state["player_position"] = [0, 0]
    st.session_state["game_over"] = False

# Display the grid as a table with player's position marked
def display_grid():
    grid_display = [["⬜" for _ in range(3)] for _ in range(3)]
    x, y = st.session_state["player_position"]
    grid_display[x][y] = "🚶"

    grid_df = pd.DataFrame(grid_display, columns=["Col 1", "Col 2", "Col 3"])
    
    # Set the table style for larger text
    st.markdown(
        grid_df.style.set_table_attributes('style="font-size: 30px; text-align: center; border: 2px solid black;"')
            .hide_index()
            .render(),
        unsafe_allow_html=True
    )

# Main game function
def start_game():
    display_instructions()
    display_grid()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.empty()
    with col2:
        st.button("⬆️ Up", on_click=update_position, args=("Up",))
    with col3:
        st.empty()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button("⬅️ Left", on_click=update_position, args=("Left",))
    with col2:
        st.button("🔄 Restart", on_click=restart_game)  # Restart button in the center
    with col3:
        st.button("➡️ Right", on_click=update_position, args=("Right",))

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.empty()
    with col2:
        st.button("⬇️ Down", on_click=update_position, args=("Down",))
    with col3:
        st.empty()

# Start the Streamlit app
if __name__ == "__main__":
    start_game()
