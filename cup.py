# cup.py
import random
from rich.console import Console
from rich.panel import Panel

console = Console()

class CupGame:
    def __init__(self, profile):
        self.profile = profile  # link to profile to save score
        self.wins_key = "cup_wins"
        if self.wins_key not in self.profile.scoreboard:
            self.profile.scoreboard[self.wins_key] = 0

    def play(self):
        console.print(Panel.fit("[bold green]Cup Game[/bold green]\nGuess which cup hides the ball (1-3). Type 0 to exit."))
        while True:
            ball = random.randint(1, 3)
            guess = input("Pick a cup (1-3) or 0 to exit: ")
            if guess == "0":
                break
            if guess not in ["1","2","3"]:
                console.print("[red]Invalid choice[/red]")
                continue
            if int(guess) == ball:
                console.print("[green]🎉 Correct![/green]")
                self.profile.scoreboard[self.wins_key] += 1
            else:
                console.print(f"[red]Wrong! The ball was under cup {ball}[/red]")
            self.profile.save()
