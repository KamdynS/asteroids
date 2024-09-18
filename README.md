# Advanced Asteroids Game

## Overview

This project is an expanded version of the classic Asteroids game, originally developed as part of a Boot.dev course. Taking the foundational concepts learned in the course, this version incorporates advanced features and demonstrates a deeper understanding of game development principles using Pygame and object-oriented programming.

## Features

- **Classic Asteroids Gameplay**: Navigate through space, shoot asteroids, and survive as long as possible.
- **Multiple Enemy Types**: Face off against various enemy types, each with unique behaviors:
  - Black Asteroids: Classic asteroid behavior
  - Green Enemies: Chase the player
  - Blue Enemies: Predict player movement
  - Red Bosses: Challenging encounters with split mechanics
- **Primitive AI**: Enemies utilize basic AI for more engaging gameplay.
- **Dynamic Difficulty**: Game becomes progressively challenging as you play.
- **Polished UI**: 
  - Start Menu: Begin your space adventure
  - Game Over Screen: View your final score and choose to restart or quit
  - In-game HUD: Keep track of your score in real-time
- **Boss Encounters**: Face off against powerful red bosses with health bars.

## Usage

1. Ensure you have Python and Pygame installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/advanced-asteroids.git
   ```
3. Navigate to the project directory:
   ```
   cd advanced-asteroids
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the game:
   ```
   python main.py
   ```

## How to Play

- Use `W`, `A`, `S`, `D` keys to move your ship.
- Press `SPACE` to shoot.
- Destroy asteroids and enemies to score points.
- Avoid collisions with asteroids and enemies.
- Defeat boss enemies for big score boosts!

## Contributing

Contributions to enhance the game are welcome! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Implement your changes and commit them: `git commit -m 'Add some feature'`
4. Push to your branch: `git push origin feature-name`
5. Create a pull request detailing your changes.

Please ensure your code adheres to the project's coding standards and include tests if applicable.

## The Making of Advanced Asteroids

This project started as a course assignment from Boot.dev, where the goal was to create a basic Asteroids clone. However, I wanted to push my skills further and create a more engaging and complex game. Here's what I added beyond the original course requirements:

1. **Enemy AI**: Implemented different behaviors for various enemy types, making the gameplay more dynamic and challenging.
2. **Boss Encounters**: Added powerful boss enemies that split into smaller enemies when defeated, inspired by classic arcade games.
3. **UI Enhancements**: Created a start menu and game over screen to give the game a more polished feel.
4. **Scoring System**: Implemented a scoring system that rewards players for defeating different enemy types.
5. **Progressive Difficulty**: The game becomes more challenging over time, keeping players engaged for longer sessions.

By expanding on the original concept, this project demonstrates not just the ability to follow a tutorial, but to take those learned concepts and apply them creatively to build a more complex and entertaining game.

## Acknowledgments

- Boot.dev for providing the foundational knowledge and inspiration for this project.
- The Pygame community for their excellent documentation and resources.

---
