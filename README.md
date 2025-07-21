<<<<<<< HEAD
# El Juego del Ping Pong

"El Juego del Ping Pong" – Oh, it's just a little something, a digital diversion, really. You know, a classic Pong game, cobbled together with Python and Pygame. It's not exactly *Annie Hall*, but it's got paddles and a ball. You can even play against a computer, which, let's be honest, is probably less judgmental than most people. We track the scores, because, well, someone has to keep tabs on these things, right? It's a simple, retro experience, a brief respite from the crushing weight of existence, or at least from deciding what to have for dinner.

## Features

-   **AI Opponent:** Play against a computer-controlled paddle.
-   **Score Tracking:** Scores are saved to a `scores.txt` file with timestamps.
-   **Customizable Difficulty:** Choose between Easy, Medium, and Hard difficulties.
-   **Customizable Paddle Color:** Select from White, Light Blue, or Light Red for your paddle.
-   **Pause Menu:** Pause the game to adjust difficulty or paddle color, and resume.
-   **Player Side Selection:** Choose to control the left or right paddle at the start of the game.
-   **Exit Functionality:** Exit the game by pressing `E`.

## How to Run the Game

To run "El Juego del Ping Pong" on your local machine, follow these steps:

### 1. Navigate to the Game Directory

Open your terminal or command prompt and navigate to the `game_pong` directory:

```bash
cd /home/jorgevazt/Documents/Gemini/game_pong
```

### 2. Create a Virtual Environment (Recommended)

It's highly recommended to create a virtual environment to manage project dependencies and avoid conflicts with your system's Python packages. From within the `game_pong` directory, run:

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

Activate the newly created virtual environment:

-   **On Linux/macOS:**

    ```bash
    source venv/bin/activate
    ```

-   **On Windows (Command Prompt):**

    ```bash
    .\venv\Scripts\activate.bat
    ```

-   **On Windows (PowerShell):**

    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

### 4. Install Dependencies

With the virtual environment activated, install the necessary Python libraries (Pygame):

```bash
pip install pygame
```

### 5. Run the Game

Once the dependencies are installed, you can run the game:

```bash
python main.py
```

## Game Controls

-   **Side Selection (Intro Screen):**
    -   Press `L` to control the **Left Paddle**.
    -   Press `R` to control the **Right Paddle**.
    -   Press `1` for Easy difficulty, `2` for Medium, `3` for Hard.
    -   Press `W` for White paddle, `B` for Light Blue, `P` for Light Red.

-   **In-Game Controls:**
    -   If you chose the **Left Paddle:** Use `W` (Up) and `S` (Down) to move.
    -   If you chose the **Right Paddle:** Use `Up Arrow` and `Down Arrow` to move.
    -   Press `Enter` to **Pause/Unpause** the game. While paused, you can change difficulty and paddle color.
    -   Press `E` to **Exit** the game.

## Score Tracking

Game scores are automatically saved to `scores.txt` located in the `game_pong` directory. Each entry includes the date, timestamp, winner, and final score.
=======
# el_juego_del_pong
>>>>>>> b1f436cd7184af36081a47da676341e4efba6c4a
