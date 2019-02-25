import json
import sys
import pprint
import collections
import timeit

def lists_are_equal(test_list1, test_list2):
    if len(test_list1)== len(test_list2) and len(test_list1) == sum([1 for i, j in zip(test_list1, test_list2) if i == j]):
        return True
    else : 
        return False

def get_all_rhymes(vowels_of_all_pronounciations):
    all_rhyming_words = []
    # get all pronounciations
    for vowels in vowels_of_all_pronounciations:
        for word in full_structure["num_syllable_word"][str(len(vowels))]:
            for set_of_vowels in full_structure[word]["vowels"]:
                if lists_are_equal(vowels, set_of_vowels):
                    all_rhyming_words.append(full_structure[word])
    
    return all_rhyming_words

def get_imp_cons_for_pron(pron, vowels, vowel_phonemes):
   consonants = []
   vowel_index = 0
   pron_index = 0

   while vowel_index < len(vowels):
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

def order_rhymes(original_word_structure, rhyme_structures, phoneme_types, vowel_phonemes):
    rhyme_and_score = {}
    for rhyme_structure in rhyme_structures:
        rhyme_score = 0

        consonance_score = 0 
        for i in range(len(original_word_structure["raw_prons"])):
            temp_consonance_score = get_consonance_score(i, original_word_structure, rhyme_structure["raw_prons"], phoneme_types, vowel_phonemes)
            consonance_score = max(consonance_score, temp_consonance_score)
        rhyme_score += consonance_score

        if original_word_structure["word"] not in rhyme_structure["word"]:
            rhyme_and_score[rhyme_structure["word"]] = rhyme_score

    return rhyme_and_score

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=2)
    full_structure = {}
    with open('./data/data.json', 'r') as d:
        full_structure = json.load(d)

    if len(sys.argv) < 2:
        print("pls supply a word")
        sys.exit()

    word_to_rhyme = sys.argv[1]   
    vowel_phonemes = full_structure["vowel_phonemes"]
    phoneme_types = full_structure["phoneme_types"]

    if word_to_rhyme not in full_structure:
        print("word not found")
        sys.exit()

    word_structure = full_structure[word_to_rhyme]
    rhymes = get_all_rhymes(word_structure["vowels"])
    pp.pprint(sorted(order_rhymes(word_structure, rhymes, phoneme_types, vowel_phonemes).items(), key=lambda kv: kv[1])) 
