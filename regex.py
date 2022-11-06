from string import ascii_lowercase
from letter import Letter

class Regex:
    def __init__(self, word_length=5):
        #Known invalid letters
        self.gray_letters = set()
        #Letters in word but not in that location
        self.yellow_letters = ["" for _ in range(word_length)]
        #Letters known to be in a certain location
        self.green_letters = ["" for _ in range(word_length)]

        self.letter_pattern = [Letter() for _ in range(word_length)]
        
        
    
    def add_gray_letters(self, letters:str):
        '''
        Takes a list of letters and updates corresponding list
        '''
        self.gray_letters.add(set(letters))
    def add_green_letters(self, letter_pairs):
        '''
        Takes a list of tuples of (known_letter, index_in_word) and updates corresponding list
        '''
        for letter, idx in letter_pairs:
            self.green_letters[idx] = letter
    def add_yellow_letters(self, letter_pairs):
        '''
        Takes a list of tuples of (known_wrong_letter, index_in_word) and updates corresponding list
        '''
        for letter,idx in letter_pairs:
            self.yellow_letters[idx] = letter
    
    def generate_regex(self):
        #Creates 
        negative_lookaheads = fr"(?!.*[{''.join(self.gray_letters)}])"
        positive_lookaheads = "".join([fr"(?=\S*[{letter}])" for letter in self.yellow_letters])

        for idx, letter, yellow, green in enumerate(zip(self.letter_pattern, self.yellow_letters, self.green_letters)):
            if self.letter_pattern[idx].is_known:
                #TODO CONTINUE
                continue

        return 