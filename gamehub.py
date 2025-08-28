#!/usr/bin/env python3
import os
import json
import random
import time
import curses
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# -------------------------
# Config
# -------------------------
SCORE_FILE = "scores.json"
DEFAULT_SCOREBOARD = {
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

# -------------------------
# Score persistence
# -------------------------
scoreboard = DEFAULT_SCOREBOARD.copy()

def load_scores():
    global scoreboard
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
            # ensure all keys exist
            for k, v in DEFAULT_SCOREBOARD.items():
                scoreboard[k] = int(data.get(k, v))
        except Exception:
            console.print("[yellow]Warning: scores.json is invalid. Resetting scores.[/yellow]")
            scoreboard = DEFAULT_SCOREBOARD.copy()
            save_scores()
    else:
        save_scores()

def save_scores():
    try:
        with open(SCORE_FILE, "w") as f:
            json.dump(scoreboard, f, indent=2)
    except Exception as e:
        console.print(f"[red]Error saving scores:[/red] {e}")

# -------------------------
# Utility: safe input
# -------------------------
def safe_input(prompt_text):
    try:
        return input(prompt_text)
    except (KeyboardInterrupt, EOFError):
        console.print("")  # newline
        return "exit"

# -------------------------
# Games
# -------------------------
def calculator():
    console.print(Panel.fit("[bold cyan]Calculator[/bold cyan]\nType 'exit' to return to menu."))
    while True:
        op = safe_input("Operation (+ - * /) or 'exit': ").strip()
        if op.lower() == "exit":
            break
        if op not in {"+", "-", "*", "/"}:
            console.print("[red]Invalid operation.[/red]")
            continue
        try:
            a = float(safe_input("First number: "))
            b = float(safe_input("Second number: "))
        except ValueError:
            console.print("[red]Please enter valid numbers.[/red]")
            continue
        result = None
        if op == "+": result = a + b
        elif op == "-": result = a - b
        elif op == "*": result = a * b
        elif op == "/":
            if b == 0:
                console.print("[red]Error: Division by zero.[/red]")
                continue
            result = a / b
        console.print(f"[green]Result:[/green] {result}")
        scoreboard["calculator_uses"] += 1
        save_scores()

def guessing_game():
    console.print(Panel.fit("[bold magenta]Number Guessing[/bold magenta]\nGuess the number between 1 and 50. Enter 0 to quit."))
    secret = random.randint(1, 50)
    attempts = 0
    while True:
        try:
            guess = int(safe_input("Your guess (1-50, 0 to quit): "))
        except ValueError:
            console.print("[red]That was not a number.[/red]")
            continue
        if guess == 0:
            break
        attempts += 1
        if guess == secret:
            console.print(f"[bold green]🎉 Correct! You guessed in {attempts} tries.[/bold green]")
            scoreboard["guessing_wins"] += 1
            save_scores()
            break
        elif guess < secret:
            console.print("Too low.")
        else:
            console.print("Too high.")

def rock_paper_scissors():
    console.print(Panel.fit("[bold yellow]Rock–Paper–Scissors[/bold yellow]\nType 'exit' to return."))
    choices = ["rock", "paper", "scissors"]
    while True:
        user = safe_input("Choose rock/paper/scissors (or exit): ").strip().lower()
        if user == "exit":
            break
        if user not in choices:
            console.print("[red]Invalid choice.[/red]")
            continue
        comp = random.choice(choices)
        console.print(f"Computer: [cyan]{comp}[/cyan]")
        if user == comp:
            console.print("[cyan]Draw![/cyan]")
            scoreboard["rps_draws"] += 1
        elif (user == "rock" and comp == "scissors") or \
             (user == "paper" and comp == "rock") or \
             (user == "scissors" and comp == "paper"):
            console.print("[green]🎉 You win![/green]")
            scoreboard["rps_wins"] += 1
        else:
            console.print("[red]😅 You lose![/red]")
            scoreboard["rps_losses"] += 1
        save_scores()

def tic_tac_toe():
    console.print(Panel.fit("[bold blue]Tic-Tac-Toe[/bold blue]\nYou are X; computer is O."))
    board = [" "] * 9
    def print_board():
        console.print(f"\n {board[0]} | {board[1]} | {board[2]} ")
        console.print("---+---+---")
        console.print(f" {board[3]} | {board[4]} | {board[5]} ")
        console.print("---+---+---")
        console.print(f" {board[6]} | {board[7]} | {board[8]} \n")
    def check_winner(p):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(board[a]==board[b]==board[c]==p for a,b,c in wins)
    def full():
        return all(s != " " for s in board)
    print_board()
    while True:
        try:
            move = int(safe_input("Your move (1-9) or 0 to exit: ")) - 1
        except ValueError:
            console.print("[red]Invalid input.[/red]")
            continue
        if move == -1:
            console.print("Exiting Tic-Tac-Toe.")
            return
        if move < 0 or move > 8 or board[move] != " ":
            console.print("[red]Invalid move.[/red]")
            continue
        board[move] = "X"
        print_board()
        if check_winner("X"):
            console.print("[green]🎉 You win![/green]")
            scoreboard["ttt_wins"] += 1
            save_scores()
            return
        if full():
            console.print("[cyan]It's a draw![/cyan]")
            scoreboard["ttt_draws"] += 1
            save_scores()
            return
        # computer move
        available = [i for i in range(9) if board[i] == " "]
        comp_move = random.choice(available)
        board[comp_move] = "O"
        console.print("Computer moves:")
        print_board()
        if check_winner("O"):
            console.print("[red]😅 Computer wins![/red]")
            scoreboard["ttt_losses"] += 1
            save_scores()
            return
        if full():
            console.print("[cyan]It's a draw![/cyan]")
            scoreboard["ttt_draws"] += 1
            save_scores()
            return

# -------------------------
# Snake (uses curses) - ASCII only
# -------------------------
def snake_game():
    console.print(Panel.fit("[bold green]Snake[/bold green]\nLaunching Snake… Use arrow keys."))
    time.sleep(0.8)
    try:
        curses.wrapper(play_snake)
    except Exception as e:
        console.print(f"[red]Snake error:[/red] {e}")

def play_snake(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(150)
    sh, sw = stdscr.getmaxyx()
    box = [[3,3],[sh-3,sw-3]]

    for y in range(box[0][0], box[1][0]):
        try:
            stdscr.addstr(y, box[0][1], "|")
            stdscr.addstr(y, box[1][1]-1, "|")
        except curses.error:
            pass
    for x in range(box[0][1], box[1][1]):
        try:
            stdscr.addstr(box[0][0], x, "-")
            stdscr.addstr(box[1][0]-1, x, "-")
        except curses.error:
            pass

    snake = [[sh//2, sw//2 + i] for i in range(3)]
    direction = curses.KEY_LEFT
    food = [sh//2, sw//2 - 5]
    try:
        stdscr.addstr(food[0], food[1], "*")
    except curses.error:
        pass
    score = 0

    while True:
        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            direction = key

        head = [snake[0][0], snake[0][1]]
        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        snake.insert(0, head)

        if snake[0] == food:
            score += 1
            food = [
                random.randint(box[0][0]+1, box[1][0]-2),
                random.randint(box[0][1]+1, box[1][1]-2)
            ]
            try:
                stdscr.addstr(food[0], food[1], "*")
            except curses.error:
                pass
        else:
            tail = snake.pop()
            try:
                stdscr.addstr(tail[0], tail[1], " ")
            except curses.error:
                pass

        try:
            stdscr.addstr(snake[0][0], snake[0][1], "#")
        except curses.error:
            pass

        if (snake[0][0] in [box[0][0], box[1][0]-1] or
            snake[0][1] in [box[0][1], box[1][1]-1] or
            snake[0] in snake[1:]):
            msg = f"GAME OVER! Score: {score}"
            try:
                stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            except curses.error:
                pass
            stdscr.refresh()
            time.sleep(2)
            scoreboard["snake_highscore"] = max(scoreboard.get("snake_highscore", 0), score)
            save_scores()
            break

        stdscr.refresh()

# -------------------------
# Scoreboard display (rich)
# -------------------------
def show_scoreboard():
    table = Table(title="🏆 Vicky's Game Hub Scoreboard", show_lines=True)
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="cyan")
    table.add_row("Calculator uses", str(scoreboard.get("calculator_uses", 0)))
    table.add_row("Number Guessing wins", str(scoreboard.get("guessing_wins", 0)))

    total_rps = scoreboard.get("rps_wins",0) + scoreboard.get("rps_losses",0) + scoreboard.get("rps_draws",0)
    rps_rate = (scoreboard.get("rps_wins",0)/total_rps*100) if total_rps>0 else 0.0
    table.add_row("RPS Wins", str(scoreboard.get("rps_wins",0)))
    table.add_row("RPS Losses", str(scoreboard.get("rps_losses",0)))
    table.add_row("RPS Draws", str(scoreboard.get("rps_draws",0)))
    table.add_row("RPS Win %", f"{rps_rate:.2f}%")

    total_ttt = scoreboard.get("ttt_wins",0)+scoreboard.get("ttt_losses",0)+scoreboard.get("ttt_draws",0)
    ttt_rate = (scoreboard.get("ttt_wins",0)/total_ttt*100) if total_ttt>0 else 0.0
    table.add_row("TicTacToe Wins", str(scoreboard.get("ttt_wins",0)))
    table.add_row("TicTacToe Losses", str(scoreboard.get("ttt_losses",0)))
    table.add_row("TicTacToe Draws", str(scoreboard.get("ttt_draws",0)))
    table.add_row("TicTacToe Win %", f"{ttt_rate:.2f}%")

    table.add_row("Snake High Score", str(scoreboard.get("snake_highscore",0)))

    console.print(table)

# -------------------------
# Main menu
# -------------------------
def main_menu():
    while True:
        menu_panel = Panel.fit(
            "[bold magenta]Vicky's Game Hub[/bold magenta]\n\n"
            "1. Calculator\n"
            "2. Number Guessing\n"
            "3. Rock–Paper–Scissors\n"
            "4. Tic-Tac-Toe\n"
            "5. Snake\n"
            "6. Show Scoreboard\n"
            "7. Exit\n",
            title="🕹️ Menu", subtitle="Choose 1-7"
        )
        console.print(menu_panel)
        choice = Prompt.ask("Your choice", choices=[str(i) for i in range(1,8)], default="6")
        try:
            if choice == "1":
                calculator()
            elif choice == "2":
                guessing_game()
            elif choice == "3":
                rock_paper_scissors()
            elif choice == "4":
                tic_tac_toe()
            elif choice == "5":
                snake_game()
            elif choice == "6":
                show_scoreboard()
            elif choice == "7":
                console.print("[bold green]Thanks for playing![/bold green]")
                break
        except Exception as e:
            console.print(f"[red]An error occurred: {e}[/red]")
            console.print("[yellow]Returning to menu...[/yellow]")
            time.sleep(1)

if __name__ == "__main__":
    load_scores()
    main_menu()
