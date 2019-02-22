import json
import pprint
import collections
def load_words():
    with open('dictionary.json') as word_file:
        valid_words = json.loads(word_file.read())

    return valid_words

def load_pronounciations():
    p_file_str = open('rawpronounciation.txt', 'r').read().split("\n")
    dict_of_p = {}
    for line in p_file_str:
        words_in_line = line.split(" ", 1)
        if words_in_line[0][-1] == ")":
            dict_of_p[words_in_line[0][:-3].lower()].append(words_in_line[1].lstrip().split(" "))
        else:
            dict_of_p[words_in_line[0].lower()] = [words_in_line[1].lstrip().split(" ")]

    return dict_of_p

def load_vowel_phonemes():
    phones_str = open('phonemes.txt', 'r').read().split("\n")
    phone_dict = set()
    for line in phones_str:
        words = line.split("\t")
        if words[1] == "vowel":
            phone_dict.add(words[0])
    
    return phone_dict

def get_common_words(english_words, pronounciations):
    p_copy = pronounciations.copy()
    for word in pronounciations:
        if word not in english_words:
            del p_copy[word]
    
    return p_copy

def lists_are_equal(test_list1, test_list2):
    if len(test_list1)== len(test_list2) and len(test_list1) == sum([1 for i, j in zip(test_list1, test_list2) if i == j]):
        return True
    else : 
        return False

# ASSUME THAT ALL WORDS HAVE THE SAME NUMBER OF VOWEL PHONEMES
def get_structure(words, vowel_phonemes):
    final_dict = {}
    for word, prons in words.items():
        vowels_of_prons = []
        for pron in prons:
            vowels_of_pron = []
            num_vowels = 0
            for w_phoneme in pron:
                phoneme_to_check = w_phoneme
                if w_phoneme[-1].isdigit():
                    phoneme_to_check = w_phoneme[:-1]
                
                if phoneme_to_check in vowel_phonemes:
                    vowels_of_pron.append(phoneme_to_check)
                    num_vowels += 1

            if len(vowels_of_prons) < 1 or lists_are_equal(vowels_of_pron, vowels_of_prons[0]):
                vowels_of_prons.append(vowels_of_pron)
        

        structure_to_add = {}
        structure_to_add["word"] = word
        structure_to_add["raw_prons"] = prons
        structure_to_add["vowels"] = vowels_of_prons
        if num_vowels in final_dict:
            final_dict[num_vowels].append(structure_to_add)
        else:
            final_dict[num_vowels] = [structure_to_add]

    return final_dict

if __name__ == '__main__':
    english_words = load_words()
    pronounciations = load_pronounciations()
    common_words = get_common_words(english_words, pronounciations)
    vowel_phonemes = load_vowel_phonemes()
    full_structure = get_structure(common_words, vowel_phonemes)
    full_structure[0] = common_words

    with open('data.json', 'w') as d:
        json.dump(full_structure, d, sort_keys=True, indent=2)
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(full_structure[4])
