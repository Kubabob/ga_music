from pyo import *
import pygad as pg
import time


KEYS = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]
SCALES = ["major", "minorM", "ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian"]
IS_PAUSE = [True, False]
INSTRUMENTS = ['1', 'funky90', 'funky80', 'MyInstrument']



def is_float(a_string):
    try:
        float(a_string)
        return True
    except ValueError:
        return False

def case_insensitive_search(key: str, list: list[str]):
    for element in list:
        if key.casefold() == element.casefold():
            key = element
            return True
    else:
        return False

def option(reference, default, prompt, answer_type):
    if reference != None:
        choosen = input(f'Do wyboru:\n{reference}\n\n{prompt}[{default}]: ')
    else:
        choosen = input(f'{prompt}[{default}]: ')
    

    if is_float(choosen):
        if float(choosen).is_integer():
            choosen = int(choosen)

        else:
            choosen = float(choosen)

        
    elif choosen.casefold() == "TRUE".casefold():
        choosen = True
    elif choosen.casefold() == "FALSE".casefold():
        choosen = False

    elif choosen == '':
        return default
    
    if reference != None:
        if type(choosen) != answer_type:
            print(f'Niepoprawny typ zmiennej!')
            input('Naciśnij ENTER aby kontynuować')
            return option(reference, default, prompt, answer_type)
        elif type(choosen) != str:
            if choosen not in reference:
                    print(f'Niepoprawna wartość!')
                    input('Naciśnij ENTER aby kontynuować')
                    return option(reference,default,prompt,answer_type)
            else:
                return choosen
        elif type(choosen) == str:
            if case_insensitive_search(choosen, reference) == False:
                print(f'Niepoprawna wartość!')
                input('Naciśnij ENTER aby kontynuować')
                return option(reference,default,prompt,answer_type)
            else:
                choosen = [x for x in reference if str(x).casefold() == choosen.casefold()][0]
                print(choosen)
                return choosen
        else:
            choosen = [x for x in reference if str(x).casefold() == choosen.casefold()][0]
            return choosen
        
    else:
        return choosen
        

