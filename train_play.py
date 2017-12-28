#!/usr/bin/python
"""
Learn hearts
"""

from __future__ import print_function
import os
import neat
import time
import pickle
from simulate import Game
from naive import NaivePlayer
from deep import DeepPlayer

try:
    with open('best_player.dat','rb') as f:
        best_net = pickle.load(f)
except:
    best_net = None
STEP = 100
BASE = STEP
threshold = 22

def mse(A):
    return map(lambda x: x**2, A)

def eval_genomes(genomes, config):
    global best_net
    global BASE
    global threshold
    global STEP
    count = 0
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        if not best_net:
            players = [NaivePlayer() for _ in range(3)]
        else:
            players = [DeepPlayer(best_net) for _ in range(3)]
        players.append(DeepPlayer(net))
        
        scores = []
        for _ in range(25):
            seed = int(time.time()*256)
            G = Game(players, seed)
            G.reset_score()

            # 0 = keep
            G.play_round(0)
            #score = G.play_game()
            score = G.get_score()
            scores.append(score[-1])

        # Highest possible squared score is 26**2 = 676
        sq = mse(scores)
        mean_score = float(sum(scores))/len(scores)
        normalized_mean_score = mean_score*26 / 676
        print("Game", count)
        count += 1
        genome.fitness = 26 - mean_score + BASE

        if genome.fitness > BASE + threshold:
            BASE += STEP
            best_net = net
            with open('best_player.dat','wb') as f:
                pickle.dump(best_net, f)

def run(config_file):

    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Restore population checkpoint
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-9')

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)
    
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
