# ECE 122 Project 1: Mystery Deduction Game
# Students run THIS file. Students submit ONLY mystery_game.py.
#
# This file is the "runner": it handles user input/output and the game loop.
# Your job (in mystery_game.py) is to write the functions that main.py calls.

import random              # used to randomly pick the hidden solution each run
import mystery_game as mg  # student-written file: contains build_game + game helper functions


def get_valid_int(prompt):
    """Keep asking until the user types an integer.

    Why this exists:
    - input() returns a STRING
    - we need an integer choice from the player
    - this function repeatedly asks until the input looks like an integer
    """
    s = input(prompt)
    # lstrip("-") allows negative numbers like "-3" to still count as digits
    while not s.lstrip("-").isdigit():
        print("Please enter an integer.")
        s = input(prompt)
    return int(s)


def get_valid_choice(prompt, low, high):
    """Keep asking until the user types an integer in [low, high].

    This is used for menu selections like 1-3, or choosing suspect 1-7, etc.
    """
    x = get_valid_int(prompt)
    while x < low or x > high:
        print("Invalid choice. Enter a number from", low, "to", high)
        x = get_valid_int(prompt)
    return x


def count_true(pos_list):
    """Count how many True values are in a boolean list.

    We store possibilities as boolean lists, e.g.:
      sus_poss[i] == True  means suspect i is STILL possible
      sus_poss[i] == False means suspect i has been eliminated

    This function is just a helper for printing stats like:
      "Remaining possibilities: Suspects = 4"
    """
    c = 0
    i = 0
    while i < len(pos_list):
        if pos_list[i]:
            c += 1
        i += 1
    return c


def print_hint(best_cat):
    """Optional hint based on best_clue_category.

    best_cat is an integer category label:
      0 -> suspects
      1 -> locations
      2 -> items
    """
    if best_cat == 0:
        print("Hint: SUSPECTS has the most possibilities left.")
    elif best_cat == 1:
        print("Hint: LOCATIONS has the most possibilities left.")
    else:
        print("Hint: ITEMS has the most possibilities left.")


def main():
    print("ECE 122: Mystery Deduction Game\n")

    # -------------------------
    # 1) Build the game "data"
    # -------------------------
    # This comes from student code (mystery_game.py).
    # build_game should return:
    #   - suspects: list of strings
    #   - locations: list of strings
    #   - items: list of strings
    #   - max_attempts: int
    #   - clue_tokens: int
    #
    # NOTE: There are NO fixed "cases" anymore — your build_game should just
    #       create and return these lists/values.
    suspects, locations, items, max_attempts, clue_tokens = mg.build_game()

    # -----------------------------------------
    # 2) Create the hidden solution ("envelope")
    # -----------------------------------------
    # We store the solution as INDEXES, not strings.
    # Example: solution_idxs = [2, 0, 4] means:
    #   suspects[2] is the culprit
    #   locations[0] is the crime scene
    #   items[4] is the item
    #
    # Randomized each time the game is run:
    solution_idxs = [
        random.randint(0, len(suspects) - 1),
        random.randint(0, len(locations) - 1),
        random.randint(0, len(items) - 1)
    ]

    # ----------------------------------------
    # 3) Initialize the player's "notebook"
    # ----------------------------------------
    # These boolean lists track what is still possible.
    # Start with everything possible (all True).
    sus_poss = [True] * len(suspects)
    loc_poss = [True] * len(locations)
    item_poss = [True] * len(items)

    # guess_history stores previous guesses (as index triples)
    # so we can detect duplicates and apply a penalty.
    guess_history = []

    # attempts counts down toward losing
    attempts = max_attempts

    # tokens is how many clue tokens you can spend to eliminate an option
    tokens = clue_tokens

    # -------------------------
    # 4) Main game loop
    # -------------------------
    # Continues until player wins, quits, or runs out of attempts.
    while True:
        # ---------- Lose check ----------
        if attempts <= 0:
            print("\nYou are out of attempts.")
            print("The envelope was:")
            print("  ", suspects[solution_idxs[0]], "in the", locations[solution_idxs[1]], "with the", items[solution_idxs[2]])
            break

        # -----------------------------------------
        # Show current game state (student function)
        # -----------------------------------------
        # display_game_state should print:
        #  - suspects/locations/items with numbering (1..N)
        #  - which ones are eliminated (False) vs still possible (True)
        #  - attempts remaining and clue tokens remaining
        mg.display_game_state(
            suspects, locations, items,
            sus_poss, loc_poss, item_poss,
            attempts, tokens
        )

        # -------------------------------------------------------
        # Strategy suggestion: which category has most left?
        # -------------------------------------------------------
        # best_clue_category returns 0/1/2.
        # This is optional "helper logic" to guide the player.
        best_cat = mg.best_clue_category(sus_poss, loc_poss, item_poss)
        print_hint(best_cat)
        print()

        # -------------------------
        # Action menu
        # -------------------------
        print("Actions:")
        print("  1) Make a suggestion")
        print("  2) Use a clue token")
        print("  3) Quit")
        action = get_valid_choice("Choose 1-3: ", 1, 3)

        # Quit option
        if action == 3:
            print("\nGoodbye!")
            break

        # =====================================================
        # Action 1: Make a suggestion (a guess)
        # =====================================================
        if action == 1:
            # Ask for suspect/location/item by number (1..N),
            # then convert to 0-based index by subtracting 1.
            s_idx = get_valid_choice("Choose suspect (1-" + str(len(suspects)) + "): ", 1, len(suspects)) - 1
            l_idx = get_valid_choice("Choose location (1-" + str(len(locations)) + "): ", 1, len(locations)) - 1
            i_idx = get_valid_choice("Choose item (1-" + str(len(items)) + "): ", 1, len(items)) - 1

            # Package guess as indexes to pass into student functions
            guess_idxs = [s_idx, l_idx, i_idx]

            # ---------------------------------------------
            # Duplicate penalty (student function)
            # ---------------------------------------------
            # check_and_record_guess should:
            #  - check if guess_idxs was guessed before (in guess_history)
            #  - record it in guess_history (if needed)
            #  - return the penalty (int) to subtract from attempts
            #
            # Typical policy used here:
            #   1 attempt cost for a new guess
            #   2 attempt cost for repeating a previous guess
            penalty = mg.check_and_record_guess(guess_history, guess_idxs)
            attempts -= penalty

            # ---------------------------------------------
            # Evaluate guess against the hidden envelope
            # ---------------------------------------------
            # evaluate_guess should return a list of 3 booleans:
            #   [suspect_correct, location_correct, item_correct]
            result_list = mg.evaluate_guess(guess_idxs, solution_idxs)

            # ---------------------------------------------
            # Print feedback to the player
            # ---------------------------------------------
            # Count how many of the 3 categories were correct.
            correct = 0
            if result_list[0]:
                correct += 1
            if result_list[1]:
                correct += 1
            if result_list[2]:
                correct += 1

            print("\nYour suggestion:")
            print("  It was", suspects[s_idx], "in the", locations[l_idx], "with the", items[i_idx])
            print("Result:", correct, "out of 3 correct.")
            print("Duplicate penalty:", penalty, "(attempts reduced by this amount)")
            print()

            # -------------------------
            # Win check (student function)
            # -------------------------
            # is_win should return True if all 3 entries in result_list are True.
            if mg.is_win(result_list):
                print("You solved the mystery! Congrats!")
                print("Attempts remaining:", attempts)
                break

            # ---------------------------------------------------
            # Update notebook (NO witness reveal in this version)
            # ---------------------------------------------------
            # update_all_notebooks should eliminate possibilities based on:
            #  - what the user guessed (guess_idxs)
            #  - which parts were correct/incorrect (result_list)
            #
            # Example idea:
            #  - if suspect was incorrect, mark that suspect as False in sus_poss
            #  - if suspect was correct, mark ALL other suspects as False
            mg.update_all_notebooks(sus_poss, loc_poss, item_poss, guess_idxs, result_list)

            print()

        # =====================================================
        # Action 2: Use a clue token to eliminate an option
        # =====================================================
        else:
            # If no tokens left, do nothing.
            if tokens <= 0:
                print("\nNo clue tokens left.\n")
            else:
                # Let the player choose which category to apply the token to.
                # 3 means "use the suggested category" (best_cat).
                print("\nUse a clue token on:")
                print("  0) Suspects")
                print("  1) Locations")
                print("  2) Items")
                print("  3) Use the suggested category")
                cat = get_valid_choice("Choose 0-3: ", 0, 3)

                if cat == 3:
                    cat = best_cat

                # -------------------------------------------------
                # use_clue_token (student function)
                # -------------------------------------------------
                # This should eliminate ONE incorrect option in that category,
                # but should NOT eliminate the correct solution.
                #
                # It returns True if something was eliminated, else False.
                eliminated = False
                if cat == 0:
                    eliminated = mg.use_clue_token(sus_poss, solution_idxs[0])
                elif cat == 1:
                    eliminated = mg.use_clue_token(loc_poss, solution_idxs[1])
                else:
                    eliminated = mg.use_clue_token(item_poss, solution_idxs[2])

                # If elimination happened, spend a token.
                if eliminated:
                    tokens -= 1
                    print("A clue token eliminated one incorrect option.")
                else:
                    print("No option could be eliminated (maybe only the correct one remains).")

                # Print updated resource counts and remaining possibilities.
                print("Clue tokens remaining:", tokens)
                print("Remaining possibilities:",
                      "Suspects =", count_true(sus_poss),
                      "| Locations =", count_true(loc_poss),
                      "| Items =", count_true(item_poss))
                print()


if __name__ == "__main__":
    main()
