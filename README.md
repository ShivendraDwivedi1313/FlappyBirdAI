# AI Flappy Bird using NEAT

An AI-powered implementation of the classic Flappy Bird game where neural networks learn to play autonomously using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm.

## Overview

This project combines **Python**, **Pygame**, and **NEAT-Python** to train an artificial intelligence agent capable of navigating obstacles in Flappy Bird. Instead of manually coding the bird's behavior, neural networks evolve over multiple generations, gradually improving their performance through natural selection and mutation.

## Features

* AI-controlled Flappy Bird using NEAT
* Evolutionary neural network training
* Real-time game simulation with Pygame
* Fitness-based genome selection
* Dynamic obstacle generation
* Collision detection using pixel-perfect masks
* Generation and score tracking
* Customizable NEAT configuration

## Tech Stack

* Python
* Pygame
* NEAT-Python

## How It Works

1. Each bird is controlled by a neural network.
2. Inputs to the network:

   * Bird's current Y position
   * Distance from the top pipe
   * Distance from the bottom pipe
3. Output:

   * Jump or do not jump
4. Birds earn fitness by surviving longer and passing pipes.
5. The best-performing genomes reproduce and mutate.
6. Over generations, the AI learns optimal flying behavior.

## Installation

```bash
pip install pygame neat-python
```

## Run

```bash
python main.py
```

## Results

The AI progressively improves over generations, learning when to jump and how to avoid collisions with pipes. Training performance can be monitored through generation count and score statistics displayed during gameplay.

## Future Improvements

* Save and load trained models
* Visualize neural network structures
* Faster training using parallel evaluation
* Custom difficulty levels
* Performance analytics dashboard
