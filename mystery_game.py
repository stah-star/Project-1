"""
ECE 122 Project 1: Mystery Deduction Game (Grader / Reference Solution)

This file contains the functions that main.py EXPECTS to exist.
Students will implement these same functions in their own mystery_game.py.

Big picture (how main.py uses this file):
- main.py calls build_game() once to get the option names and starting resources.
- main.py randomly chooses the hidden solution (the “envelope”) using INDEXES
  into the suspects/locations/items options.
- During the loop, main.py calls the functions below to:
  * print the notebook (display_game_state)
  * score a guess vs. the envelope (evaluate_guess)
  * check for a win (is_win)
  * cross off impossible options (update_all_notebooks)
  * apply duplicate guess penalty (check_and_record_guess)
  * spend clue tokens to eliminate an option (use_clue_token)
  * suggest which category to use a token on (best_clue_category)

Important design notes:
- The hidden solution is stored as INDEXES (not strings) in main.py.
- The notebook stores “still possible?” as True/False values.
- This version has NO witness reveal and NO separate cases.
"""
"""
Student 1:
Spire Id:

Student 2: 
Spire Id:
"""
import random


def build_game():
    """
    Create and return the game data (no cases).

    This function sets up the game configuration:
    - suspects/locations/items: the options the player can choose from
    - max_attempts: how many attempts the player starts with in main.py
    - clue_tokens: how many clue tokens the player starts with in main.py

    Returns:
        suspects: all suspect name options shown in the menu
        locations: all location name options shown in the menu
        items: all item name options shown in the menu
        max_attempts: starting number of attempts (main.py copies this into attempts)
        clue_tokens: starting number of clue tokens (main.py copies this into tokens)
    """
    # --- Core game data ---
    # suspects/locations/items should be filled with the full set of names.
    # main.py will later choose the secret envelope by picking an INDEX into each set.
    pass

    # Randomize displayed order each run.
    # This makes the menu look different each time the program is run.
    # main.py chooses the envelope AFTER calling build_game(), so shuffling here is safe:
    # the indices still match the names for the entire run.
    random.shuffle(suspects)
    random.shuffle(locations)
    random.shuffle(items)

    # Per spec: player gets 4 attempts total.
    # main.py copies this into its variable "attempts".
    # max_attempts = 4
    pass
    
    # Randomize starting clue tokens (resource system).
    # main.py copies this into its variable "tokens".
    # Adjust this range if you want tokens to be more/less common.
    clue_tokens = random.randint(1, 2)
    pass


def display_game_state(suspects, locations, items, pos_suspect, pos_location, pos_item, attempts, tokens):
    """
    Print the player's current notebook and remaining resources.

    Parameters (all are passed in from main.py each loop):
        suspects: the suspect names (used to print the numbered suspect menu)
        locations: the location names (used to print the numbered location menu)
        items: the item names (used to print the numbered item menu)

        pos_suspect: tracks which suspect options are still possible.
            main.py updates this over time as the player learns information.

        pos_location: tracks which location options are still possible.
            main.py updates this over time as the player learns information.

        pos_item: tracks which item options are still possible.
            main.py updates this over time as the player learns information.

        attempts: how many attempts the player has left right now.
            main.py decreases this after each suggestion (and duplicates may cost extra).

        tokens: how many clue tokens the player has left right now.
            main.py decreases this when a clue token successfully eliminates an option.

    Output:
        None (prints to the console)
    """
    # Only print options that are still marked as possible in the notebook.
    # NOTE: We display with numbering starting at 1 for user friendliness,
    # even though the internal indexes start at 0.
    pass


def evaluate_guess(guess_idx, solution_idx):
    """
    Compare a guess (indexes) to the hidden solution (indexes).

    Parameters:
        guess_idx: the player's guess as three indexes chosen in main.py:
            - guess_idx[0] is the suspect index they chose
            - guess_idx[1] is the location index they chose
            - guess_idx[2] is the item index they chose

        solution_idx: the secret envelope indexes created in main.py at startup:
            - solution_idx[0] is the correct suspect index
            - solution_idx[1] is the correct location index
            - solution_idx[2] is the correct item index

    Returns:
        result_list: three True/False values telling main.py what matched:
            - result_list[0] True if suspect index matches the envelope
            - result_list[1] True if location index matches the envelope
            - result_list[2] True if item index matches the envelope

    Example:
        guess_idx    = [1, 4, 0]
        solution_idx = [1, 2, 3]
        returns      = [True, False, False]
    """
    # We always compare 3 categories in this order:
    # 0 = suspect, 1 = location, 2 = item
    pass


def is_win(result_list):
    """
    Determine whether the player has solved the mystery.

    Parameters:
        result_list: the True/False match results returned by evaluate_guess().
            main.py calls is_win right after evaluate_guess().

    Returns:
        True only if all three parts of the guess were correct.
    """
    pass


def update_all_notebooks(pos_suspect, pos_location, pos_item, guess_idx, result_list):
    """
    Update the deduction notebook using ONLY correctness feedback.
    (No witness reveals in this version.)

    What this function is for:
    - main.py calls this after a non-winning guess.
    - It updates the notebook trackers so the next screen shows fewer possibilities.

    Notebook rule used here:
    - If a category was WRONG, cross off the guessed option for that category.
    - If a category was RIGHT, we do NOT automatically cross off other options here.
      (Some versions do, but this keeps updates minimal: only remove what you know is wrong.)

    Parameters (all come from main.py):
        pos_suspect: the notebook tracker for suspects (modified in place)
        pos_location: the notebook tracker for locations (modified in place)
        pos_item: the notebook tracker for items (modified in place)

        guess_idx: the player's most recent guess indexes (chosen in main.py)

        result_list: which parts were correct/incorrect (returned by evaluate_guess)

    Returns:
        None (the notebook trackers are updated in place)
    """
    # If the suspect part was incorrect, that specific suspect cannot be in the envelope,
    # so cross it off in the suspect notebook.

    # If the location part was incorrect, that specific location cannot be in the envelope,
    # so cross it off in the location notebook.

    # If the item part was incorrect, that specific item cannot be in the envelope,
    # so cross it off in the item notebook.
    pass


def check_and_record_guess(guess_history, guess_idx):
    """
    Check whether a guess is a duplicate, then record it in history.

    Why main.py uses this:
    - main.py discourages repeating the exact same suggestion.
    - It charges more attempts if the guess was already made.

    Duplicate penalty policy used by main.py:
    - New guess: costs 1 attempt
    - Duplicate guess: costs 2 attempts

    Parameters (both come from main.py):
        guess_history: the running record of all prior guesses this game.
            main.py keeps this across turns and passes it back in each time.

        guess_idx: the current guess triple (suspect/location/item indexes)
            that main.py just collected from the user.

    Returns:
        penalty: the number main.py should subtract from attempts for this guess
                 (2 if duplicate, otherwise 1)
    """
    # Search through history to see if the exact same triple was guessed before.
    # A "duplicate" means same suspect index AND same location index AND same item index.

    # Record the guess so future turns can detect duplicates.
    # Important: store the three index values, not a reference that might change later.

    # Return the attempt penalty amount so main.py can subtract it from attempts.
    pass


def use_clue_token(possible_list, solution_index):
    """
    Use a clue token to eliminate ONE incorrect option in a category.

    How main.py uses this:
    - When the player spends a clue token, main.py chooses a category and passes in
      that category’s notebook tracker (for suspects OR locations OR items).
    - main.py also passes the correct envelope index for that category so we do NOT
      eliminate the true answer.

    Behavior in this reference solution:
    - Scan from low index to high index.
    - Find the first option that is still possible AND is not the correct one.
    - Eliminate it and report success.

    Parameters:
        possible_list: the notebook tracker for ONE category (passed in from main.py)
        solution_index: the correct envelope index for THIS category (passed in from main.py)

    Returns:
        eliminated: True if we eliminated something, False if we could not
                   (usually because only the correct option remains possible)
    """
    # Only eliminate an option if it is still possible
    # and it is not the solution_index (never eliminate the correct answer).

    # If we reach the end without eliminating anything, we couldn't use the token
    # to remove an incorrect option (often because only the correct one remains).
    pass


def best_clue_category(pos_suspect, pos_location, pos_item):
    """
    Choose which category is "best" to spend a clue token on.

    How main.py uses this:
    - main.py calls best_clue_category each loop and shows a hint to the player.
    - main.py also allows the player to choose "use suggested category" and then
      uses this return value.

    Strategy used:
    - Count how many options remain possible in each category.
    - Return the category with the largest count (most uncertainty).
    - If there is a tie, break ties consistently:
        suspects first, then locations, then items.

    Parameters (all are passed in from main.py):
        pos_suspect: notebook tracker for which suspects are still possible
        pos_location: notebook tracker for which locations are still possible
        pos_item: notebook tracker for which items are still possible

    Returns:
        category:
            0 means "suspects"
            1 means "locations"
            2 means "items"
    """
    # Count how many suspects are still possible.

    # Count how many locations are still possible.

    # Count how many items are still possible.

    # Return the category number with the most remaining possibilities.
    pass
