
def trade():
    pass

def roll():
    pass

def construct_building():
    pass

def end_turn():
    pass

def mortgage_property():
    pass

def turn():
    end_flag = False
    while end_flag is False:
        print("1: Trade with others")
        print("2: Roll dices")
        print("3: Construct building")
        print("4: Mortgage property")
        print("5: End turn")
        choice = input("Please enter the number of your decision:")
        if choice == 1:
            trade()
        elif choice == 2:
            roll()
        elif choice == 3:
            construct_building()
        elif choice == 4:
            mortgage_property()
        elif choice == 5:
            end_turn()
        else:
            print("Invalid choice")