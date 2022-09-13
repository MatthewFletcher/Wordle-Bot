from string import ascii_lowercase

class Letter:
    def __init__(self) -> None:
        self.is_known = False
        self.valid_remaining_letters = set(ascii_lowercase)
        self.letter = ""
    
    def remove_potentials(self, letters:str) -> None:
        #If letter is already known, skip it
        if not self.is_known:
            for letter in letters:
                self.valid_remaining_letters.discard(letter)

    def set_letter(self, letter:str) -> None:
        self.valid_remaining_letters = set(letter)
        self.letter = letter
        self.is_known = True
    
    def __str__(self) -> str:
        if self.is_known:
            return self.letter
        else:
            return f"[{''.join(sorted(self.valid_remaining_letters))}]"