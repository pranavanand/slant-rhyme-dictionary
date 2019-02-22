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

def load_english_words():
    file_str = open('common_words_list.txt', 'r').read().split("\n")
    set_of_words = set()
    for line in file_str:
        set_of_words.add(line)

    return set_of_words

def load_phoneme_types():
    file_str = open('phoneme_types.txt', 'r').read().split("\n")
    dict_of_phonemes = {}
    for line in file_str:
        phoneme_sound = line.split()
        dict_of_phonemes[phoneme_sound[0]] = phoneme_sound[1]

    return dict_of_phonemes


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
                    all_rhyming_words.append(structure)
    
    return all_rhyming_words

def get_imp_cons_for_pron(pron, vowels, vowel_phonemes):
   consonants = []
   vowel_index = 0
   pron_index = 0

   while vowel_index < len(vowels):
       # if pron_index >= len(pron):
        #    print(pron)
           #print(vowels)

       phoneme_to_check = pron[pron_index]
       if phoneme_to_check[-1].isdigit():
           phoneme_to_check = phoneme_to_check[:-1]
       # add prev and next tuple to consonants at vowel_index
       if phoneme_to_check in vowel_phonemes:
           vowel_index += 1
           prev = ""
           next_phon = ""
           if pron_index > 0:
               prev = pron[pron_index - 1]
           
           if pron_index < (len(pron) - 1):
               next_phon = pron[pron_index + 1]
           
           consonants.append((prev, next_phon))
       pron_index += 1
   return consonants
    

# consonant sounds between vowels being the same increases the score
def get_consonance_score(index_of_pron, word_structure, rhyme_prons, phonemes, vowel_phonemes):
    score = 0
    # may cause issue - unlikely though
    index_of_vowels = index_of_pron
    if index_of_pron >= len(word_structure["vowels"]):
        index_of_vowels = len(word_structure["vowels"]) - 1
    
    vowels = word_structure["vowels"][index_of_vowels]
    pron = word_structure["raw_prons"][index_of_pron]
    word_cons = get_imp_cons_for_pron(pron, vowels, vowel_phonemes)

    for rhyme_pron in rhyme_prons:
        temp_score = 0
        rhyme_cons = get_imp_cons_for_pron(rhyme_pron, vowels, vowel_phonemes)

        for i in range(len(vowels)):
            if word_cons[i][0] == rhyme_cons[i][0]:
                temp_score += 1
            
            if word_cons[i][1] == rhyme_cons[i][1]:
                temp_score += 1

        score = max(score, temp_score)

    return score

def order_rhymes(original_word_structure, rhyme_structures, common_english_words, phoneme_types, vowel_phonemes):
    rhyme_and_score = {}
    for rhyme_structure in rhyme_structures:
        rhyme_score = 0
        if rhyme_structure["word"] in common_english_words:
            rhyme_score += 0

        consonance_score = 0 
        for i in range(len(original_word_structure["raw_prons"])):
            consonance_score = max(consonance_score, get_consonance_score(i, original_word_structure, rhyme_structure["raw_prons"], phoneme_types, vowel_phonemes))
        rhyme_score += consonance_score

        if original_word_structure["word"] == rhyme_structure["word"]:
            rhyme_score = -1
        
        rhyme_and_score[rhyme_structure["word"]] = rhyme_score

    return rhyme_and_score

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
    common_english_words = load_english_words()
    phoneme_types = load_phoneme_types() 
    vowels_of_all_pronounciations = get_vowels(full_structure, word_to_rhyme, vowel_phonemes)

    if vowels_of_all_pronounciations is None:
        print("word not found")
        sys.exit()

    print(vowels_of_all_pronounciations)
    rhymes = get_all_rhymes(vowels_of_all_pronounciations)
    # pp.pprint(full_structure["0"])
    # fix this
    word_structure = {}
    word_structure["word"] = word_to_rhyme
    word_structure["raw_prons"] = full_structure["0"][word_to_rhyme]
    word_structure["vowels"] = vowels_of_all_pronounciations
    pp.pprint(sorted(order_rhymes(word_structure, rhymes, common_english_words, phoneme_types, vowel_phonemes).items(), key=lambda kv: kv[1])) 
