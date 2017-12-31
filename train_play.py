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

def eval_genomes(genomes, config):
    count = 0
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        #if not best_net:
        #    players = [NaivePlayer() for _ in range(3)]
        #else:
        #    players = [DeepPlayer(best_net) for _ in range(3)]

        players = [NaivePlayer() for _ in range(3)]
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

        #print(scores)
        sq = map(lambda x: x**2, scores)
        mean_score = sum(sq)*1.0/len(sq)

        print("Genome", count)
        count += 1
        print(676 - mean_score)
        genome.fitness = 676 - mean_score

        #if genome.fitness > BASE + threshold:
        #    BASE += STEP
        #    best_net = net
        #    with open('best_player.dat','wb') as f:
        #        pickle.dump(best_net, f)

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
    with open('best_player.dat', 'wb') as f:
        pickle.dump(winner_net, f)

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
