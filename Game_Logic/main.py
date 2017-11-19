import random
import board

# chess_board = board.board()
chess_board = None

def trade():
    pass

def roll(player):
    """
    Roll a dice
        :param player: The player who roll dices
    Returns:
        :int: The number of first dice
        :int: The number of second dice
        :bool: The station of end_flag
    """
    print("Rolling")
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    if a == b:
        end_flag = False
    else:
        end_flag = True
    print("Dice number is", a, b)
    step = a + b
    player.move(step)
    end_position = player.position
    current_block = chess_board.get_block(end_position)
    current_block.display()
    return a, b, end_flag

def construct_building():
    pass

def mortgage_property():
    pass

def turn(player):
    end_flag = False
    while True:
        print("1: Trade with others")
        print("2: Roll dices")
        print("3: Construct building")
        print("4: Mortgage property")
        print("5: End turn")
        choice = int(input("Please enter the number of your decision:"))
        print(choice)
        if choice == 1:
            trade()
        elif choice == 2:
            dice_a, dice_b, end_flag = roll(player)
        elif choice == 3:
            construct_building()
        elif choice == 4:
            mortgage_property()
        elif choice == 5:
            if end_flag is True:
                break
            else:
                print("Please roll a dice")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    turn(None)