import pygad as pg
from pyo import *
from ga_music import *
from ga_options import *
from midiutil import MIDIFile


#dodac rozwiazanie na koniec melodii
#dodac dwudzwieki (40, 30, 30)
#dac opcje zmiany dlugosci dzwiekow
#posprzatac kod
#zapisywanie wyniku jako plik audio

def genetic_music_algo():
    def fitness_func(ga_instance, solution, sol_idx):

        print(f'\nGeneracja nr {(sol_idx//num_notes)+1}')
        print(f'Melodia nr {sol_idx}')
        music_instance.play_music(solution=solution)
        
        return option(None, 0, 'Ocena [0-10]', int)
    
    #Rafal Lawendowski

    def music_ga(is_continued: bool = False, previous_load: str = None, is_finished: bool = False):

        ga_instance = pg.GA(num_generations=1,
                            num_parents_mating=2,
                            fitness_func=fitness_func,
                            sol_per_pop=population_count,
                            num_genes=num_notes*3,
                            parent_selection_type='rank',
                            mutation_probability=mutation_prob,
                            mutation_num_genes=mutation_count,
                            gene_space=gene_space,
                            gene_type = int,
                            #keep_elitism=1,
                            save_best_solutions=True
                            )
        if is_finished:
            if option(None, False, 'Czy chcesz zapisac melodie?', bool):
                ga_instance = pg.load('previous_load')
                music_instance.save_melody_to_midi(option(None, f'Melodia_{time.strftime("%b%d%Y%H%M%S")}', 'Jak chcesz nazwać melodię?', str), ga_instance.best_solutions[0])
        else:
            if is_continued:
                ga_instance = pg.load(previous_load)
                ga_instance.run()
                ga_instance.save('previous_load')
            else:
                ga_instance.run()
                ga_instance.save('previous_load')
            
        


    def main():

        does_continue = True
        generation_idx = 0

        while does_continue:
            if does_continue != True:
                break              

            if generation_idx > 0:
                music_ga(is_continued=True, previous_load='previous_load')
            else:
                music_ga()
            
            does_continue = option(None, False, 'Czy chcesz kontynuować', bool)
            generation_idx += 1
        else:
            music_ga(is_finished=True)
            
        
    
    
    key=option(KEYS, 'C', 'Klucz', str)
    scale=option(SCALES, 'major', 'Skala', str)
    population_count=option(None, 4, 'Liczba melodii na populacje', int)
    bpm=option(None, 100, 'Tempo [0-128]', int)
    octaves_count=option(None, 2, 'Liczba oktaw', int)
    first_octave=option(None, 4, 'Numer pierwszej oktawy', int)
    tact_numbers=option(None, 2, 'Liczba taktów', int)
    notes_per_tact=option(None, 4, 'Liczba nut na takt', int)
    mutation_count=option(None, 2, 'Liczba mutacji', int)
    mutation_prob=option(None, 0.3, 'Prawdopodobienstwo mutacji [0-1]', float)

    eventScale = EventScale(root=key, scale=scale, first=first_octave, octaves=octaves_count+1)

    music_instance = GA_music(scale=eventScale, bpm=bpm, tact_numbers=tact_numbers, notes_per_tact=notes_per_tact) 


    num_notes = tact_numbers*notes_per_tact

    gene_subspace1 = [range(0, int(2*len(eventScale)/3)) for _ in range(0, num_notes)]
    gene_subspace2 = [range(0, 10) for _ in range(0, num_notes)] #probability of single/triple note
    gene_subspace3 = [range(1, 3) for _ in range(0, num_notes)]

    gene_space = []
    gene_space.extend(gene_subspace1)
    gene_space.extend(gene_subspace2)
    gene_space.extend(gene_subspace3)

 
    main()
    
        
    

genetic_music_algo()