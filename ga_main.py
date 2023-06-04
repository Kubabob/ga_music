import pygad as pg
from pyo import *
from ga_music import *
from ga_options import *


def ga_algo():
    def fitness_func(ga_instance, solution, sol_idx):
        solution = list(solution)
        print(solution)
        tuning(scale=eventScale,
               bpm=bpm,
               instrument=instrument,
               tact_numbers=tact_numbers,
               notes_per_tact=notes_per_tact,
               solution=solution)
        
        #time.sleep(0.5)

        rating = option([i for i in range(0,11)], 0, 'Ocena [0-10]', int)
        return int(rating)
    
    key=option(KEYS, 'C', 'Klucz', str)
    scale=option(SCALES, 'major', 'Skala', str)
    num_generations=option(None, 2, 'Liczba generacji', int)
    population_count=option(None, 4, 'Liczba na populacje', int)
    bpm=option(None, 100, 'Tempo [0-128]', int)
    octaves_count=option(None, 2, 'Liczba oktaw', int)
    first_octave=option(None, 4, 'Numer pierwszej oktawy', int)
    instrument=option(INSTRUMENTS, 'funky80', 'Wybierz instrument', str)
    tact_numbers=option(None, 2, 'Liczba taktów', int)
    notes_per_tact=option(None, 4, 'Liczba nut na takt', int)
    mutation_count=option(None, 2, 'Liczba mutacji', int)
    mutation_prob=option(None, 0.5, 'Prawdopodobienstwo mutacji [0-1]', float)

    eventScale = EventScale(root=key, scale=scale, first=first_octave, octaves=octaves_count)
    

    ga_music = pg.GA(num_generations=num_generations,
                        num_parents_mating=2,
                        fitness_func=fitness_func,
                        sol_per_pop=population_count,
                        num_genes=tact_numbers*notes_per_tact,
                        gene_type=int,
                        parent_selection_type='rank',
                        mutation_probability=mutation_prob,
                        mutation_num_genes=mutation_count,
                        gene_space=[i for i in range(0, len(eventScale))],
                        keep_elitism=1
                        )
    
    ga_music.run()

    solution, solution_fitness, solution_idx = ga_music.best_solution()
    solution = list(solution)
    print(f"Parameters of the best solution: {solution}")
    print(f"Fitness value of the best solution = {solution_fitness}\n")
    tuning(scale=scale,
               bpm=bpm,
               instrument=instrument,
               tact_numbers=tact_numbers,
               notes_per_tact=notes_per_tact,
               solution=solution)
        

ga_algo()
