import json
import sys
import pprint
import collections

def load_vowel_phonemes():
    phones_str = open('phonemes.txt', 'r').read().split("\n")
    phone_dict = set()
    for line in phones_str:
        words = line.split("\t")
        if words[1] == "vowel":
            phone_dict.add(words[0])
    
    return phone_dict


def get_vowels(structure, word, vowel_phonemes):
    list_of_possible_vowels = []
    if word in structure["0"]:
        prons = structure["0"][word]
        for pron in prons:
            vowels_in_pron = []
            for w_phoneme in pron:
                phoneme_to_check = w_phoneme
                if w_phoneme[-1].isdigit():
                    phoneme_to_check = w_phoneme[:-1]
                
                if phoneme_to_check in vowel_phonemes:
                    vowels_in_pron.append(phoneme_to_check)
            list_of_possible_vowels.append(vowels_in_pron)
    else:
        return None
    
    return list_of_possible_vowels

def lists_are_equal(test_list1, test_list2):
    if len(test_list1)== len(test_list2) and len(test_list1) == sum([1 for i, j in zip(test_list1, test_list2) if i == j]):
        return True
    else : 
        return False


def get_all_rhymes(vowels_of_all_pronounciations):
    all_rhyming_words = []
    for vowels in vowels_of_all_pronounciations:
        for structure in full_structure[str(len(vowels))]:
            for set_of_vowels in structure["vowels"]:
                if lists_are_equal(vowels, set_of_vowels):
                    all_rhyming_words.append(structure["word"])
    
    return all_rhyming_words

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=2)
    full_structure = {}
    with open('data.json', 'r') as d:
        full_structure = json.load(d)

    if len(sys.argv) < 2:
        print("pls supply a word")
        sys.exit()

    word_to_rhyme = sys.argv[1]   
    vowel_phonemes = load_vowel_phonemes() 
    vowels_of_all_pronounciations = get_vowels(full_structure, word_to_rhyme, vowel_phonemes)

    if vowels_of_all_pronounciations is None:
        print("word not found")
        sys.exit()

    print(vowels_of_all_pronounciations)
    pp.pprint(get_all_rhymes(vowels_of_all_pronounciations)) 
