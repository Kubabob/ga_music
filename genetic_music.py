import pygad as pg
from pyo import *
from music_algorithms import *
from ga_options import *
from midiutil import MIDIFile


class Genetic_music:
    '''
    Creates music based on idea of genetic algorithm

    Parameters
    ----------
    Everything is set inside __init__

    Set parameters
    ---------
    key: str
        The base key of melody.
        ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']
    scale: str
        The music scale of melody.
        [‘major’, ‘minorH’, ‘minorM’, ‘ionian’, ‘dorian’, ‘phrygian’, ‘lydian’, ‘mixolydian’, ‘aeolian’, ‘locrian’,
        ‘wholeTone’, ‘majorPenta’, ‘minorPenta’, ‘egyptian’, ‘majorBlues’, ‘minorBlues’, ‘minorHungarian’]
    population_count: int
        Number of melodies in 1 generation of genetic algorithm. Each cycle is made of 2 generations.
    bpm: int
        Beats per minute. Tempo of melody.
    octaves_count: int
        Number of octaves that melody will consist of. One octave is 8 keys, 1st and 8th are the same. The higher
        number the more note diverse your melody will be.
        ex. C D E F G A B C is one octave of C major
    first_octave: int
        Number of the first octave. People are mainly speaking in 4th octave.
    tact_numbers: int
        Number of tacts of the melody. 1 tact can be interpreted as 1 segment.
    notes_per_tact: int
        Number of notes per tact(segment) of melody.
    mutation_count: int
        Number of random notes of the melody that will randomly change after generation passes.
    mutation_prob: float
        Probability that note will actually change

    Returns
    -------
    Set of melodies that have to be rated. Best 2 are going to create new generation of melodies. Best rated melody can
    be saved in MIDI file.
    '''

    def __init__(self):
        keys = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]
        scales = ["major", 'minorH', "minorM", "ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian",
                  "locrian", 'wholeTone', 'majorPenta', 'minorPenta', 'egyptian', 'majorBlues', 'minorBlues',
                  'minorHungarian']
        self.gene_space = None
        self.key = option(keys, 'C', 'Key', str)
        self.scale = option(scales, 'major', 'Scale', str)
        self.population_count = option(None, 4, 'Number of melodies per generation', int)
        self.bpm = option(None, 100, 'Tempo [0-128]', int)
        self.octaves_count = option(None, 2, 'Number of octaves', int)
        self.first_octave = option(None, 4, 'Number of first octave', int)
        self.tact_numbers = option(None, 2, 'Number of tacts', int)
        self.notes_per_tact = option(None, 4, 'Number of notes per tact', int)
        self.mutation_count = option(None, 2, 'Number of potential mutations', int)
        self.mutation_prob = option(None, 0.3, 'Mutation probability [0-1]', float)
        self.num_notes = self.tact_numbers * self.notes_per_tact

        self.eventScale = EventScale(root=self.key, scale=self.scale, first=self.first_octave,
                                     octaves=self.octaves_count + 1)

        self.music_instance = Music_algorithms(scale=self.eventScale, bpm=self.bpm, tact_numbers=self.tact_numbers,
                                               notes_per_tact=self.notes_per_tact)

        gene_subspace1 = [range(0, int(2 * len(self.eventScale) / 3)) for _ in range(0, self.num_notes)]  # notes
        gene_subspace2 = [range(0, 10) for _ in range(0, self.num_notes)]  # probability of single/double/triple note
        gene_subspace3 = [range(1, 3) for _ in range(0, self.num_notes)]  # lenghts of notes

        self.gene_space = []
        self.gene_space.extend(gene_subspace1)
        self.gene_space.extend(gene_subspace2)
        self.gene_space.extend(gene_subspace3)

    def fitness_func(self, ga_instance, solution, sol_idx):
        '''
        Fitness function required by genetic algorithm instance. Pygad requires all 3 parameters in order to work.
        '''

        self.music_instance.play_music(solution=solution)

        return option(None, 0, 'Ocena [0-10]', int)


    def music_ga(self, is_continued: bool = False, previous_load: str = None, is_finished: bool = False):
        '''
        Creates the generatic algorithm instance.
        Runs made melodies.
        Saves the best one if desired.
        '''

        ga_instance = pg.GA(num_generations=1,
                            num_parents_mating=2,
                            fitness_func=self.fitness_func,
                            sol_per_pop=self.population_count,
                            num_genes=self.num_notes * 3,
                            parent_selection_type='rank',
                            crossover_type='two_points',
                            mutation_probability=self.mutation_prob,
                            mutation_num_genes=self.mutation_count,
                            gene_space=self.gene_space,
                            gene_type=int,
                            save_best_solutions=True
                            )
        if is_finished:
            if option(None, True, 'Czy chcesz zapisac melodie?', bool):
                ga_instance = pg.load('previous_load')
                self.music_instance.save_melody_to_midi(option(None, f'Melodia_{time.strftime("%b%d%Y%H%M%S")}',
                                                               'Jak chcesz nazwać melodię?', str),
                                                        ga_instance.best_solutions[0])
                print(f'Wynik najlepszej: {ga_instance.best_solution()[1]}')
        else:
            if is_continued:
                ga_instance = pg.load(previous_load)
                ga_instance.run()
                ga_instance.save('previous_load')
            else:
                ga_instance.run()
                ga_instance.save('previous_load')

    def run(self):
        '''
        Runs the algorithm
        '''

        does_continue = True
        generation_idx = 0

        while does_continue:
            if not does_continue:
                break

            if generation_idx > 0:
                self.music_ga(is_continued=True, previous_load='previous_load')
            else:
                self.music_ga()

            does_continue = option(None, False, 'Czy chcesz kontynuować', bool)
            generation_idx += 1
        else:
            self.music_ga(is_finished=True)

