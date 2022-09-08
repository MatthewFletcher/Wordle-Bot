import string
import os
import re
import sys
from typing import Pattern


import numpy as np
from colorama import Back

from enum import Enum


class Letter_Score(Enum):
    VALID_PLACE = 2
    VALID_LETTER = 1
    INVALID_LETTER = -1


class Game:
    def __init__(self, word_length: int = 5) -> None:
        self.STAT_FILE = f"/tmp/stats{os.getpid()}.json"
        self.WORD_FILE = "/Users/fletch-mac/Desktop/wordle_list.txt"
        self.WORD_LEN = word_length
        self.MAX_GUESS_NUM = 6
        self.guessed_matrix = np.array(
            [(np.zeros(5, dtype=int)) for _ in list(string.ascii_lowercase)],
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
                if input("Are you sure you want to end?"):
                    sys.exit()
            if w in self.VALID_WORDS:
                break
            else:
                print(f"{w} is not a valid guess")
        self.current_guess = w

    def generate_regex(self) -> re.Pattern:
        # Original regex is ".....", matching all 5 letter words
        re_str = ["." for _ in range(self.WORD_LEN)]
        for idx, pos_arr in enumerate(self.guessed_matrix.T):
            # Score of 2 means that letter is confirmed in that place
            if any(pos_arr == Letter_Score.VALID_PLACE):
                re_str[idx] = chr(ord("a") + pos_arr.argmax())
            if any(pos_arr == Letter_Score.INVALID_LETTER):
                # re_str[idx]
                pass
        return re.compile("".join(re_str))

    def get_possible_words(self) -> list:
        r = self.generate_regex()
        # Create list of words that are still valid options
        ret_arr = [word for word in self.VALID_WORDS if r.match(word)]
        return ret_arr

    def check_guess(self) -> np.ndarray:
        ret_arr = np.zeros(self.WORD_LEN, dtype=int)
        for idx, guess_letter, word_letter in zip(
            range(self.WORD_LEN), self.current_guess, self.word
        ):
            if guess_letter == word_letter:
                self.guessed_matrix[ord(guess_letter) - ord("a")][
                    idx
                ] = Letter_Score.VALID_PLACE
                ret_arr[idx] = 2
            elif guess_letter in str(self.word):
                self.guessed_matrix[ord(guess_letter) - ord("a")][
                    idx
                ] = Letter_Score.VALID_LETTER
                ret_arr[idx] = 1
            else:
                self.guessed_matrix[ord(guess_letter) - ord("a")][
                    idx
                ] = Letter_Score.INVALID_LETTER
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
            self.print_guess()
            if sum(guess_arr) == 2 * self.WORD_LEN:
                print("Success")
                break
        print("Game Over")


g = Game()
g.play_person_game()
