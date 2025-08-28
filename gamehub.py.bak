import random
import os
import curses
import time

# --- Global scoreboard ---
scoreboard = {
    "calculator_uses": 0,
    "guessing_wins": 0,
    "rps_wins": 0,
    "rps_losses": 0,
    "rps_draws": 0,
    "ttt_wins": 0,
    "ttt_losses": 0,
    "ttt_draws": 0,
    "snake_highscore": 0
}

SCORE_FILE = "scores.txt"

# --- Load scores ---
def load_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                scoreboard[key] = int(value)

# --- Save scores ---
def save_scores():
    with open(SCORE_FILE, "w") as f:
        for key, value in scoreboard.items():
            f.write(f"{key}={value}\n")

# --- Calculator ---
def calculator():
    print("\n--- Calculator ---")
    print("Type 'exit' to return.\n")
    while True:
        op = input("Choose operation (+, -, *, /): ")
        if op.lower() == "exit":
            break
        try:
            a = float(input("First number: "))
            b = float(input("Second number: "))
        except ValueError:
            print("❌ Invalid numbers!")
            continue
        if op == "+":
            print("Result:", a + b)
        elif op == "-":
            print("Result:", a - b)
        elif op == "*":
            print("Result:", a * b)
        elif op == "/":
            print("Result:", a / b if b != 0 else "Error: Division by zero")
        else:
            print("❌ Invalid operation!")
        scoreboard["calculator_uses"] += 1
        save_scores()

# --- Number Guessing ---
def guessing_game():
    print("\n--- Number Guessing ---")
    secret = random.randint(1, 50)
    attempts = 0
    while True:
        try:
            guess = int(input("Guess (1-50, 0 to quit): "))
        except ValueError:
            print("❌ Not a number.")
            continue
        if guess == 0:
            break
        attempts += 1
        if guess == secret:
            print(f"🎉 Correct in {attempts} tries!\n")
            scoreboard["guessing_wins"] += 1
            save_scores()
            break
        elif guess < secret:
            print("Too low.")
        else:
            print("Too high.")

# --- Rock–Paper–Scissors ---
def rock_paper_scissors():
    print("\n--- Rock–Paper–Scissors ---")
    choices = ["rock", "paper", "scissors"]
    while True:
        user = input("Choose rock, paper, or scissors (or exit): ").lower()
        if user == "exit":
            break
        if user not in choices:
            print("❌ Invalid choice!")
            continue
        comp = random.choice(choices)
        print(f"Computer: {comp}")
        if user == comp:
            print("Draw!\n")
            scoreboard["rps_draws"] += 1
        elif (user == "rock" and comp == "scissors") or \
             (user == "paper" and comp == "rock") or \
             (user == "scissors" and comp == "paper"):
            print("🎉 You win!\n")
            scoreboard["rps_wins"] += 1
        else:
            print("😅 You lose!\n")
            scoreboard["rps_losses"] += 1
        save_scores()

# --- Tic-Tac-Toe ---
def tic_tac_toe():
    print("\n--- Tic-Tac-Toe ---")
    board = [" "] * 9
    def print_board():
        print(f"\n {board[0]} | {board[1]} | {board[2]} ")
        print("---+---+---")
        print(f" {board[3]} | {board[4]} | {board[5]} ")
        print("---+---+---")
        print(f" {board[6]} | {board[7]} | {board[8]} \n")
    def check_winner(p):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(board[a]==board[b]==board[c]==p for a,b,c in wins)
    def full():
        return all(s != " " for s in board)
    print_board()
    while True:
        try:
            move = int(input("Your move (1-9): ")) - 1
        except ValueError:
            continue
        if move<0 or move>8 or board[move]!=" ":
            print("❌ Invalid move.")
            continue
        board[move] = "X"; print_board()
        if check_winner("X"):
            print("🎉 You win!\n"); scoreboard["ttt_wins"]+=1; save_scores(); return
        if full(): print("Draw!\n"); scoreboard["ttt_draws"]+=1; save_scores(); return
        comp = random.choice([i for i in range(9) if board[i]==" "])
        board[comp]="O"; print("Computer moves:"); print_board()
        if check_winner("O"):
            print("😅 Computer wins!\n"); scoreboard["ttt_losses"]+=1; save_scores(); return
        if full(): print("Draw!\n"); scoreboard["ttt_draws"]+=1; save_scores(); return

# --- Snake ---
def snake_game():
    print("\nLaunching Snake..."); time.sleep(1)
    curses.wrapper(play_snake)

def play_snake(stdscr):
    curses.curs_set(0); stdscr.nodelay(1); stdscr.timeout(150)
    sh, sw = stdscr.getmaxyx()
    box = [[3,3],[sh-3,sw-3]]
    for y in range(box[0][0], box[1][0]):
        try: stdscr.addstr(y, box[0][1], "|"); stdscr.addstr(y, box[1][1]-1, "|")
        except: pass
    for x in range(box[0][1], box[1][1]):
        try: stdscr.addstr(box[0][0], x, "-"); stdscr.addstr(box[1][0]-1, x, "-")
        except: pass
    snake=[[sh//2, sw//2+i] for i in range(3)]; direction=curses.KEY_LEFT
    food=[sh//2, sw//2-5]; stdscr.addstr(food[0], food[1], "*")
    score=0
    while True:
        key=stdscr.getch()
        if key in [curses.KEY_UP,curses.KEY_DOWN,curses.KEY_LEFT,curses.KEY_RIGHT]:
            direction=key
        head=[snake[0][0],snake[0][1]]
        if direction==curses.KEY_UP: head[0]-=1
        elif direction==curses.KEY_DOWN: head[0]+=1
        elif direction==curses.KEY_LEFT: head[1]-=1
        elif direction==curses.KEY_RIGHT: head[1]+=1
        snake.insert(0,head)
        if snake[0]==food:
            score+=1
            food=[random.randint(box[0][0]+1, box[1][0]-2),random.randint(box[0][1]+1, box[1][1]-2)]
            try: stdscr.addstr(food[0], food[1], "*")
            except: pass
        else:
            tail=snake.pop()
            try: stdscr.addstr(tail[0], tail[1], " ")
            except: pass
        try: stdscr.addstr(snake[0][0], snake[0][1], "#")
        except: pass
        if (snake[0][0] in [box[0][0], box[1][0]-1] or
            snake[0][1] in [box[0][1], box[1][1]-1] or
            snake[0] in snake[1:]):
            msg=f"💀 GAME OVER! Score: {score}"
            try: stdscr.addstr(sh//2, sw//2-len(msg)//2, msg)
            except: pass
            stdscr.refresh(); time.sleep(2)
            scoreboard["snake_highscore"]=max(scoreboard["snake_highscore"],score)
            save_scores(); break
        stdscr.refresh()

# --- Show Scoreboard ---
def show_scoreboard():
    print("\n===============================")
    print(" 🏆 VICKY'S GAME HUB SCOREBOARD 🏆")
    print("===============================\n")
    print(f"Calculator used       : {scoreboard['calculator_uses']} times")
    print(f"Number Guessing wins  : {scoreboard['guessing_wins']}")
    total_rps=scoreboard['rps_wins']+scoreboard['rps_losses']+scoreboard['rps_draws']
    rps_rate=(scoreboard['rps_wins']/total_rps*100) if total_rps>0 else 0
    print("\nRock–Paper–Scissors:")
    print(f"   Wins   : {scoreboard['rps_wins']}")
    print(f"   Losses : {scoreboard['rps_losses']}")
    print(f"   Draws  : {scoreboard['rps_draws']}")
    print(f"   Win %  : {rps_rate:.2f}%")
    total_ttt=scoreboard['ttt_wins']+scoreboard['ttt_losses']+scoreboard['ttt_draws']
    ttt_rate=(scoreboard['ttt_wins']/total_ttt*100) if total_ttt>0 else 0
    print("\nTic-Tac-Toe:")
    print(f"   Wins   : {scoreboard['ttt_wins']}")
    print(f"   Losses : {scoreboard['ttt_losses']}")
    print(f"   Draws  : {scoreboard['ttt_draws']}")
    print(f"   Win %  : {ttt_rate:.2f}%")
    print(f"\nSnake High Score      : {scoreboard['snake_highscore']}")
    print("\n===============================\n")

# --- Main Menu ---
def main_menu():
    while True:
        print("\n=== Vicky's Game Hub ===")
        print("1. Calculator")
        print("2. Number Guessing")
        print("3. Rock–Paper–Scissors")
        print("4. Tic-Tac-Toe")
        print("5. Snake")
        print("6. Show Scoreboard")
        print("7. Exit")
        choice=input("Choose (1-7): ")
        if choice=="1": calculator()
        elif choice=="2": guessing_game()
        elif choice=="3": rock_paper_scissors()
        elif choice=="4": tic_tac_toe()
        elif choice=="5": snake_game()
        elif choice=="6": show_scoreboard()
        elif choice=="7":
            print("\nFinal Scores:"); show_scoreboard()
            print("Scores saved in scores.txt ✅\nThanks for playing Vicky 👋"); break
        else: print("❌ Invalid choice.")

# --- Run ---
load_scores()
main_menu()