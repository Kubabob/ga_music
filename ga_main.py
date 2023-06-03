import pygad as pg
from pyo import *
from ga_music import *
from ga_options import *


def ga_algo():
    def fitness_func(ga_instance, solution, sol_idx):
        solution = list(solution)
        tuning(key=key,
               scale_=scale,
               population_count=population_count,
               mutation_prob=mutation_prob,
               bpm=bpm,
               octaves_count=octaves_count,
               first_octave=first_octave,
               instrument=instrument,
               tact_numbers=tact_numbers,
               notes_per_tact=notes_per_tact,
               is_pause=is_pause,
               solution=solution)
        
        rating = option([i for i in range(0,11)], 0, 'Ocena [0-10]', int)
        return rating
    
    key=option(KEYS, 'C', 'Klucz', str)
    scale=option(SCALES, 'major', 'Skala', str)
    num_generations=option(None, 2, 'Liczba generacji', int)
    population_count=option(None, 4, 'Liczba na populacje', int)
    bpm=option(None, 100, 'Tempo [0-128]', int)
    octaves_count=option(None, 2, 'Liczba oktaw', int)
    first_octave=option(None, 4, 'Numer pierwszej oktawy', int)
    instrument=option(INSTRUMENTS, 'MyInstrument', 'Wybierz instrument', str)
    tact_numbers=option(None, 2, 'Liczba taktów', int)
    notes_per_tact=option(None, 4, 'Liczba nut na takt', int)
    mutation_count=option(None, 2, 'Liczba mutacji', int)
    mutation_prob=option(None, 0.5, 'Prawdopodobienstwo mutacji [0-1]', float)
    is_pause=option(IS_PAUSE, False, 'Czy uwzględniać pauzy', bool)
    

    ga_instance = pg.GA(num_generations=num_generations,
                        num_parents_mating=2,
                        fitness_func=fitness_func,
                        sol_per_pop=population_count,
                        num_genes=tact_numbers*notes_per_tact,
                        gene_type=int,
                        parent_selection_type='rank',
                        mutation_probability=mutation_prob,
                        mutation_num_genes=mutation_count,
                        gene_space=[i for i in range(0, 8*octaves_count)],
                        keep_elitism=1
                        )
    
    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print(f"Parameters of the best solution: {solution}")
    print(f"Fitness value of the best solution = {solution_fitness}\n")
    tuning(key=key,
               scale_=scale,
               population_count=population_count,
               mutation_prob=mutation_prob,
               bpm=bpm,
               octaves_count=octaves_count,
               first_octave=first_octave,
               instrument=instrument,
               tact_numbers=tact_numbers,
               notes_per_tact=notes_per_tact,
               is_pause=is_pause,
               solution=list(solution))
        

ga_algo()