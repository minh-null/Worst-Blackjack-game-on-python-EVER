import tkinter as tk
from tkinter import messagebox
import random

# Card setup
cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
card_values = {
    "A": 11,
    "J": 10,
    "Q": 10,
    "K": 10,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10
}

# Helper functions
def calculate_hand_value(hand):
    total = sum(card_values[card] for card in hand)
    aces = hand.count("A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def draw_card():
    return random.choice(cards)

# Main Game Class
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.wallet = 1000
        self.high_score = 100
        self.bet = 0
        self.doubled_down = False
        self.init_ui()

    def init_ui(self):
        # Labels
        self.info = tk.Label(self.root, text="Welcome to Blackjack!", font=("Helvetica", 14))
        self.info.pack(pady=10)

        self.wallet_label = tk.Label(self.root, text=f"Wallet: ${self.wallet}")
        self.wallet_label.pack()

        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack()
        self.bet_entry.insert(0, "10")

        # Buttons
        self.start_button = tk.Button(self.root, text="Start Round", command=self.start_round)
        self.start_button.pack(pady=5)

        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit, state="disabled")
        self.hit_button.pack(side="left", padx=10)

        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand, state="disabled")
        self.stand_button.pack(side="left", padx=10)

        self.double_button = tk.Button(self.root, text="Double Down", command=self.double_down, state="disabled")
        self.double_button.pack(side="left", padx=10)

        # Card Displays
        self.player_label = tk.Label(self.root, text="Your Hand: ")
        self.player_label.pack(pady=10)

        self.dealer_label = tk.Label(self.root, text="Dealer's Hand: ")
        self.dealer_label.pack(pady=10)

    def start_round(self):
        try:
            self.bet = int(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Invalid bet", "Please enter a valid number.")
            return

        if self.bet < 1 or self.bet > self.wallet:
            messagebox.showerror("Invalid bet", "Bet must be within your wallet balance.")
            return

        self.doubled_down = False
        self.wallet_label.config(text=f"Wallet: ${self.wallet}")
        self.info.config(text="Round started. Your move.")
        self.player_hand = [draw_card(), draw_card()]
        self.dealer_hand = [draw_card(), draw_card()]

        self.show_hands()
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")
        self.double_button.config(state="normal")
        self.start_button.config(state="disabled")

    def show_hands(self, reveal_dealer=False):
        self.player_label.config(
            text=f"Your Hand: {self.player_hand} (Total: {calculate_hand_value(self.player_hand)})"
        )
        if reveal_dealer:
            self.dealer_label.config(
                text=f"Dealer's Hand: {self.dealer_hand} (Total: {calculate_hand_value(self.dealer_hand)})"
            )
        else:
            self.dealer_label.config(
                text=f"Dealer's Hand: [{self.dealer_hand[0]}, ?]"
            )

    def hit(self):
        self.player_hand.append(draw_card())
        self.show_hands()

        if calculate_hand_value(self.player_hand) > 21:
            self.end_round("Bust! Dealer wins.")

    def stand(self):
        self.dealer_turn()

    def double_down(self):
        if self.wallet < self.bet * 2:
            messagebox.showwarning("Insufficient funds", "Not enough to double down.")
            return
        self.wallet -= self.bet  # Only deduct the extra part of the double
        self.bet *= 2
        self.doubled_down = True
        self.player_hand.append(draw_card())
        self.show_hands()
        self.stand()


    def dealer_turn(self):
        self.show_hands(reveal_dealer=True)
        while calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(draw_card())
            self.show_hands(reveal_dealer=True)
            self.root.update()

        self.resolve_round()


    def resolve_round(self):
        player_total = calculate_hand_value(self.player_hand)
        dealer_total = calculate_hand_value(self.dealer_hand)

        result = ""
        win = False
        tie = False

        if player_total > 21:
            result = "You busted! Dealer wins."
        elif dealer_total > 21 or player_total > dealer_total:
            result = "You win!"
            win = True
        elif dealer_total == player_total:
            result = "It's a tie!"
            tie = True
        else:
            result = "Dealer wins."

    # Wallet handling (Inside the method now)
        if win:
            self.wallet += self.bet
        elif tie:
            if self.doubled_down:
                self.wallet += self.bet  # Refund one bet
        else:
            self.wallet -= self.bet

        if self.wallet > self.high_score:
            self.high_score = self.wallet

    # Update UI
        self.info.config(text=f"{result} Wallet: ${self.wallet} | High score: ${self.high_score}")
        self.wallet_label.config(text=f"Wallet: ${self.wallet}")
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.double_button.config(state="disabled")
        self.start_button.config(state="normal")

    # Game over condition
        if self.wallet <= 0:
            messagebox.showinfo("Game Over", "You're out of money!")
            self.root.quit()

    


            

# Start the GUI
root = tk.Tk()
game = BlackjackGame(root)
root.mainloop()
