# ChessAi-master

**ChessAi-master** is a Python project aimed at developing a chess-playing artificial intelligence using various algorithms and techniques. This project provides a platform for experimenting with different approaches to chess AI and understanding the complexities involved in creating an effective chess-playing program.

This project is created step by step following Eddie Sharick's [YouTube tutorial series](https://www.youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_). 

## Features

- **Object-Oriented Programming (OOP)**: Utilizes object-oriented principles to organize code into classes and objects, enhancing modularity, reusability, and maintainability.
- **Better File Structure**: Implements a well-structured file organization to enhance code readability and maintainability, separating concerns and functionalities into different modules.
- **Sound Effects**: Incorporates sound effects to enhance the user experience, providing auditory feedback for moves, captures, and game events.
- **Threading and Multiprocessing**: Implements threading and multiprocessing techniques to improve performance, allowing for concurrent execution of tasks such as move generation, evaluation, and user interface interaction.
- **Chess Engine**: Implements a basic chess engine capable of generating legal moves, evaluating positions, and making moves based on different algorithms.
- **Minimax Algorithm**: Utilizes the minimax algorithm with alpha-beta pruning to search through the game tree and find the optimal move.
- **Alpha-Beta Pruning**: Implements alpha-beta pruning to improve the efficiency of the minimax algorithm by eliminating redundant branches.
- **Evaluation Functions**: Includes evaluation functions to assess the strength of a given position, considering factors such as piece values, position control, mobility, and king safety.
- **User Interface**: Provides a simple text-based user interface for interacting with the chess engine and playing games against the AI.

## Installation

To use ChessAi-master, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Hetari/ChessAi-master.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ChessAi-master
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

After installing the project, you can run the chess engine and play games against the AI using the following command:

```bash
python main.py
```

Follow the on-screen instructions to make moves and interact with the chess engine.

## Contributing

Contributions to ChessAi-master are welcome! If you'd like to contribute to the project, feel free to fork the repository and submit a pull request with your changes.

## Acknowledgments

ChessAi-master is inspired by various chess AI projects and algorithms available in the open-source community. We extend our gratitude to Eddie Sharick for his excellent tutorial series, which served as a guide for the development of this project.

