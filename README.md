# 🐍 Snakes & Ladders King (Human vs Bot)

A vibrant, fully animated 2D Snakes and Ladders game built from scratch in Python using **Pygame**. Play a classic turn-based match against a simulated computer AI opponent that rolls and moves dynamically.

---

## 🚀 Features
* **Smooth Step-by-Step Animations:** Tokens physically hop across individual tiles sequentially instead of instantly teleporting.
* **Dynamic Dice Roller:** The dice visually spins through randomized face values before locking onto your roll outcome.
* **Automated Bot Logic:** A smart computer player that takes turns, waits organically, and navigates shortcuts or traps.
* **Boustrophedon Grid Map:** Built using custom math to map tile positions (1-100) into a continuous snake-like zigzag pixel coordinate map.

---

## 🎮 How To Play
1. **Your Turn:** The dashboard panel will display "CLICK DICE TO ROLL". Click the white dice square in the bottom-right corner.
2. **Movement:** Your blue token will walk forward the exact number of spaces rolled. 
3. **Shortcuts & Hazards:** Landing at the bottom of a **Green Ladder** will slide you up to safety. Landing on the head of an **Orange Snake** will slide you backward down the board!
4. **Winning:** The first player to reach exactly square **100** wins the match. If you roll a number that overshoots 100, your turn is skipped!

---

## 🛠️ Installation & Setup

### Prerequisites
Make sure you have Python 3.12, 3.13, or 3.14 installed on your machine.
