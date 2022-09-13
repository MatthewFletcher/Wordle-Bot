from nis import match
import string
import os
import re
import sys
from typing import Pattern
from black import main


import numpy as np
from colorama import Back

from enum import Enum

from letter import Letter


class Letter_Score(Enum):
    GREEN = 2
    YELLOW = 1
    GRAY = -1


class Game:
    def __init__(self, word_length: int = 5) -> None:
        self.STAT_FILE = f"/tmp/stats{os.getpid()}.json"
        self.WORD_FILE = "data/wordle_list.txt"
        self.WORD_LEN = word_length
        self.MAX_GUESS_NUM = 6
        #Matrix of 6 (guesses) x 26 (letters) 
        #Contains status codes of each guess
        #This matrix as written should be capable of holding all data from each game
        self.guessed_matrix = np.array(
            [(np.zeros(self.MAX_GUESS_NUM, dtype=int)) for _ in list(string.ascii_lowercase)],
            dtype=object,
        )
        self.current_guess = ""
        # Get words from list
        with open(self.WORD_FILE, "r") as f:
            all_words = [word.strip() for word in f.readlines()]
            # Valid words are words of length 5, and all letters are ascii letters
            self.VALID_WORDS = np.array(
                [
                    word.lower()
                    for word in all_words
                    if len(word) == self.WORD_LEN
                    and all(c in string.ascii_letters for c in word)
                ]
            )
            self.remaining_words = self.VALID_WORDS
            # Select a random word from list
            self.word = np.random.choice(self.VALID_WORDS)

    def get_new_word(self) -> None:
        # Reset word list
        self.remaining_words = self.VALID_WORDS
        # Reset word to guess
        self.word = np.random.choice(self.VALID_WORDS).lower()

    def get_guess(self, prompt="Enter word: ") -> None:
        while True:
            try:
                w = input(prompt).lower()
            except EOFError as e:
                if input("Are you sure you want to end? [y/n]").lower() not in ('y'):
                    sys.exit()
            if w in self.VALID_WORDS:
                break
            else:
                print(f"{w} is not a valid guess")
        self.current_guess = w

    def generate_regex(self) -> re.Pattern:
        # Original regex is ".....", matching all 5 letter words
        re_set = [Letter() for _ in range(self.WORD_LEN)]
        #iterate through each element of word with a length 26 array
        #Guess checker sets letter indexes to their various scores. 
        #letter_idx is current position in word (0-4)
        #letter_scores is result of each letter using Letter_Score values
        for letter_idx, letter_scores in enumerate(self.guessed_matrix.T):
            
            #If letter was guessed correctly (green), set that letter in the regex
            # to the determined letter
            green_idx = np.where(letter_scores==Letter_Score.GREEN)[0]
            if green_idx.size:
                re_set[letter_idx].set_letter(self.letter_from_index(green_idx[0]))
           
            #If letter is gray, remove that letter from ALL undetermined squares
            gray_idx = np.where(letter_scores==Letter_Score.GRAY)[0]
            if gray_idx.size:
                for letter in re_set:
                    letter.remove_potentials(self.letter_from_index(gray_idx[0]))

            #If letter is yellow, remove that letter from THAT square
            yellow_idx = np.where(letter_scores==Letter_Score.YELLOW)[0]
            if yellow_idx.size:
                re_set[letter_idx].remove_potentials(self.letter_from_index(yellow_idx[0]))
        return re.compile("".join([str(letter) for letter in re_set]))
    
    def letter_from_index(self, idx:int) -> str:
        return chr(ord('a') + idx)

    def get_possible_words(self) -> list:
        regex = self.generate_regex()
        # Create list of words that are still valid options
        ret_arr = [word for word in self.VALID_WORDS if regex.match(word)]
        return ret_arr

    def check_guess(self) -> np.ndarray:
        ret_arr = np.zeros(self.WORD_LEN, dtype=int)
        for idx, guess_letter, word_letter in zip(
            range(self.WORD_LEN), self.current_guess, self.word
        ):
            if guess_letter == word_letter:
                self.guessed_matrix[ord(guess_letter) - ord("a")][
                    idx
                ] = Letter_Score.GREEN
                ret_arr[idx] = 2
            elif guess_letter in str(self.word):
                self.guessed_matrix[ord(guess_letter) - ord("a")][
                    idx
                ] = Letter_Score.YELLOW
                ret_arr[idx] = 1
            else:
                self.guessed_matrix[ord(guess_letter) - ord("a")][
                    idx
                ] = Letter_Score.GRAY
                ret_arr[idx] = 0

        return ret_arr

    def print_guess(self) -> None:
        print_str = ""
        guess_arr = self.check_guess()
        for guess_letter, word_letter in zip(self.current_guess, self.word):
            if guess_letter == word_letter:
                print_str += Back.GREEN + guess_letter
            elif guess_letter in str(self.word):
                print_str += Back.YELLOW + guess_letter
            else:
                print_str += Back.LIGHTBLACK_EX + guess_letter
        print_str += Back.RESET
        print(print_str)

    def play_person_game(self):
        print(f"Word value: {self.word}")

        for i in range(self.MAX_GUESS_NUM):
            print(f"On guess {i}")
            self.get_guess("Enter guess here: ")
            guess_arr = self.check_guess()
            print(self.generate_regex())
            print(self.get_possible_words())
            self.print_guess()
            if sum(guess_arr) == 2 * self.WORD_LEN:
                print("Success")
                break
        print("Game Over")

if __name__ == "__main__":
    g = Game()
    g.play_person_game()
