"""Note storage and manipluation."""

from enum import Enum
import re

DEFAULT_NOTE_SHIFT_VALUE = "natural"
"""Default value intended for use when note shift is not specified."""
DEFAULT_NOTE_OCTAVE_VALUE = 4
"""Default value intended for use when note octave is not specified."""
OCTAVE_LOWER_BOUND = 0
"""The lowest allowed octave value (inclusive)"""
OCTAVE_UPPER_BOUND = 10
"""The highest allowed octave value (inclusive)"""


class AbstractNote(Enum):
    """A basic representation of a note in the English chromatic scale.

    Due to inherit complexity of music notes and their variations (due to the
    fact that, for example, "C Sharp" and "D Flat" are the same note), this is
    a highly abstracted and simplified representation of the notes in the
    English chromatic scale.

    This starts on C rather than A simply because C is the "first" note in
    scientific pitch notation. As an example, going down a semitone from C4
    (middle C) takes you to B3, meaning that it is on the third octave rather
    than the fourth. Since other classes that build on AbstractNote may deal
    with octaves, it makes sense to make it as easy as possible to process an
    octave change (which would simply require checking whether the processing
    has wrapped over the top or under the bottom of the Enum).
    """

    bsharp_cnatural = 0
    csharp_dflat = 1
    dnatural = 2
    dsharp_eflat = 3
    enatural_fflat = 4
    esharp_fnatural = 5
    fsharp_gflat = 6
    gnatural = 7
    gsharp_aflat = 8
    anatural = 9
    asharp_bflat = 10
    bnatural_cflat = 11

    def __add__(self, other):
        """Add a value and return the corresponding AbstractNote.

        This method uses modulo to wrap around the AbstractNote list and
        continue on the other side. This is done so that a "B" can be
        incremented by one and arrive at a "C" without causing an error.
        """
        return AbstractNote((self.value + other) % len(AbstractNote))

    def __sub__(self, other):
        """Subtract a value from return the corresponding AbstractNote.

        This method uses almost identical logic to the __add__ method for the
        same reasons outlined in the related docstring, except for subtraction.
        """
        return AbstractNote((self.value - other) % len(AbstractNote))


class Note:
    """An advanced representation of a note in the English chromatic scale.

    This class builds upon the basic structure of the AbstractNote class and
    is intended to provide additional logic and state to better represent a
    note.
    """

    def __init__(self,
                 note_letter,
                 note_shift=DEFAULT_NOTE_SHIFT_VALUE,
                 note_octave=DEFAULT_NOTE_OCTAVE_VALUE):
        """Create an instance of Note.

        Args:
            note_letter (str): The note letter to create Note with
            note_shift (str, optional): The note shift to create Note with
            note_octave (int, optional): The octave to create the note with
        """
        self.set_note(note_letter, note_shift, note_octave)

    def __str__(self):
        """Return the string representation of Note."""
        return "{} {}".format(self.note.name, str(self.note_octave))

    def __eq__(self, other):
        """Return whether the Note is equal to the passed Note."""
        return self.note == other.note and \
            self.note_octave == other.note_octave

    @property
    def note(self):
        """Return the stored note."""
        return self._note

    def set_note(self,
                 note_letter,
                 note_shift=DEFAULT_NOTE_SHIFT_VALUE,
                 note_octave=DEFAULT_NOTE_OCTAVE_VALUE):
        """Set the stored note.

        Takes two values (note_letter and note_shift), converts them into an
        AbstractNote and stores the result.

        This also stores the note_letter and note_shift values internally in
        case they have any further use.

        The reason that this function is not used as a setter for the "note"
        property is that setters can only take in one value cleanly; in theory
        a tuple or other such construct could be used to package the values on
        one side and then unpack them once passed, but that only serves to
        complicate the contract by requiring users to package their values
        first.

        Args:
            note_letter (str): The note letter to set the Note with
            note_shift (str, optional): The note shift to set the Note with
            note_octave (int, optional): The note octave to set the Note with
        """
        self._note_letter = note_letter
        self._note_shift = note_shift
        self.note_octave = note_octave
        self._note = convert_note_to_abstract(note_letter, note_shift)

    @property
    def note_octave(self):
        """Return the stored note's octave."""
        return self._note_octave

    @note_octave.setter
    def note_octave(self, input_note_octave):
        """Set the stored note's octave.

        Args:
            input_note_octave (int): The note octave to update the Note with
        """
        if is_note_octave_valid(input_note_octave):
            self._note_octave = input_note_octave
        else:
            raise ValueError("input_note_octave ({}) must be between {} and "
                             "{}".format(input_note_octave,
                                         OCTAVE_LOWER_BOUND,
                                         OCTAVE_UPPER_BOUND))


def parse_note_string(note_string):
    """Parse a note string and return the note letter and note shift.

    This function takes a human readable note string, meant to represent one of
    the notes in the English chromatic scale, and returns the component
    parts (the note letter and whether it is shifted up (sharp), shifted down
    (flat) or not at all (natural)).

    This function is designed to work cooperatively with the function
    convert_note_to_abstract, which requires specific values to work correctly.
    As such, this function is able to take an unrefined input string and
    prepare it in such a way that it is valid for convert_note_to_abstract. For
    this to work properly however, the result of parse_note_string (which is a
    tuple) must be unpacked before being passed over to
    convert_note_to_abstract (using the asterisk syntax).

    Due to the fact that re.IGNORECASE is used, values that use an uppercase
    flat symbol ("B" instead of "b") are accepted. This is an unintended side
    effect, but it's preferable to rejecting mixed or upper case note shifts
    (such as "Natural" or "SHARP") or complicating the regex unnecessarily.

    Args:
        note_string (str): The human readable note string to be parsed

    Returns:
        note_letter (str): The letter component of note_string, lowercase
        note_shift (str): The shift component of note_string, lowercase

    Raises:
        ValueError: If the regex does not successfully parse note_string
        TypeError: If note_string does not have a valid .lower() method

    TODO:
        Add support for actual unicode natural, sharp and flat symbols
    """
    pattern = r"^([A-G])[ ]?(natural|sharp|#|flat|b)?$"

    result = re.match(pattern, note_string, re.IGNORECASE)

    if result:
        note_letter, note_shift = result.groups()

        if note_shift is None:
            note_shift = DEFAULT_NOTE_SHIFT_VALUE
        else:
            note_shift = parse_note_shift(note_shift)
        try:
            return note_letter.lower(), note_shift.lower()
        except AttributeError:
            raise TypeError("note_string ({}) is an invalid "
                            "type".format(note_string))
    else:
        raise ValueError("note_string ({}) could not "
                         "be parsed".format(note_string))


def is_note_valid(input_note):
    """Check that input_note is a valid Note.

    Args:
        input_note (Note): The Note that is being checked

    Returns:
        bool: Whether input_note is a valid Note or not
    """
    result = False

    try:
        result = is_note_letter_valid(input_note._note_letter) and \
            is_note_shift_valid(input_note._note_shift) and \
            is_note_octave_valid(input_note.note_octave)
    except AttributeError:
        result = False

    return result


def is_abstract_note_valid(input_abstract_note):
    """Check that input_abstract_note is a valid AbstractNote.

    Args:
        input_abstract_note (AbstractNote): The AbstractNote that is being
            checked

    Returns:
        bool: Whether input_abstract_note is a valid AbstractNote or not
    """
    return input_abstract_note in AbstractNote


def is_note_letter_valid(input_note_letter):
    """Check that input_note_letter is a valid note letter.

    Args:
        input_note_letter (str): The note letter that is being checked

    Returns:
        bool: Whether input_note_letter is a valid note letter or not

    Raises:
        TypeError: If input_note_letter is an invalid type
    """
    lower_bound = "a"
    upper_bound = "g"

    character_range = range(ord(lower_bound), ord(upper_bound) + 1)

    valid_note_letters = [chr(letter) for letter in character_range]

    try:
        return input_note_letter.lower() in valid_note_letters
    except AttributeError:
        raise TypeError("input_note_letter ({}) is an invalid "
                        "type".format(input_note_letter))


def is_note_shift_valid(input_note_shift):
    """Check that input_note_shift is a valid note shift.

    Args:
        input_note_shift (str): The note shift that is being checked

    Returns:
        bool: Whether input_note_shift is a valid note shift or not

    Raises:
        TypeError: If input_note_shift is an invalid type
    """
    valid_note_shifts = (
        "flat",
        "natural",
        "sharp",
        "#",
        "b"
    )

    try:
        return input_note_shift.lower() in valid_note_shifts
    except AttributeError:
        raise TypeError("input_note_shift ({}) is an invalid "
                        "type".format(input_note_shift))


def is_note_octave_valid(input_note_octave):
    """Check that input_note_octave is a valid note_octave.

    Args:
        input_note_octave (int): The note octave that is being checked

    Returns:
        bool: Whether input_note_octave is a valid note octave or not

    Raises:
        TypeError: If input_note_octave is an invalid type
    """
    try:
        return OCTAVE_LOWER_BOUND <= input_note_octave <= OCTAVE_UPPER_BOUND
    except TypeError:
        raise TypeError("input_note_octave ({}) must be an "
                        "integer".format(input_note_octave))


def parse_note_shift(note_shift):
    """Parse a note shift and return a refined value representing the shift.

    This function accepts a note_shift and converts the multiple variations
    into a single value for the three main shifts (flat, natural and sharp).

    Args:
        note_shift (str): The unrefined string representing the shift

    Returns:
        str: The refined string representing the shift

    Raises:
        TypeError: If note_shift does not have a valid .lower() method
        ValueError: If note_shift does not match a value in the shift dict
    """
    note_shift_translation_dict = {
        "natural": "natural",
        "sharp": "sharp",
        "#": "sharp",
        "flat": "flat",
        "b": "flat",
    }

    try:
        return note_shift_translation_dict[note_shift.lower()]
    except AttributeError:
        raise TypeError("note_shift ({}) is an "
                        "invalid type".format(note_shift))
    except KeyError:
        raise ValueError("note_shift ({}) does not match with a "
                         "valid note shift".format(note_shift))


def convert_note_to_abstract(note_letter, note_shift=DEFAULT_NOTE_SHIFT_VALUE):
    """Convert note letter and note shift to an AbstractNote and return it.

    This function is used to match specific note letter/shift pairs to their
    AbstractNote representations. It does not allow for ambiguity or
    inaccuracy; if the letter isn't valid, the shift is misspelt or the like,
    this function will fail.

    This function is designed to work cooperatively with parse_note_string,
    which accepts a string and parses it into arguments which match those
    required in this function.

    Args:
        note_letter (str): The note letter that will be processed
        note_shift (str, optional): The note shift that will be processed

    Returns:
        AbstractNote: The converted AbstractNote representation of the
            arguments

    Raises:
        TypeError: If note_letter and/or note_shift do not have valid .lower()
            methods
        ValueError: If the provided note_letter and note_shift do not
            correspond to a valid AbstractNote
    """
    note_translation_dict = {
        ("b", "sharp"): AbstractNote.bsharp_cnatural,
        ("c", "natural"): AbstractNote.bsharp_cnatural,
        ("c", "sharp"): AbstractNote.csharp_dflat,
        ("d", "flat"): AbstractNote.csharp_dflat,
        ("d", "natural"): AbstractNote.dnatural,
        ("d", "sharp"): AbstractNote.dsharp_eflat,
        ("e", "flat"): AbstractNote.dsharp_eflat,
        ("e", "natural"): AbstractNote.enatural_fflat,
        ("f", "flat"): AbstractNote.enatural_fflat,
        ("e", "sharp"): AbstractNote.esharp_fnatural,
        ("f", "natural"): AbstractNote.esharp_fnatural,
        ("f", "sharp"): AbstractNote.fsharp_gflat,
        ("g", "flat"): AbstractNote.fsharp_gflat,
        ("g", "natural"): AbstractNote.gnatural,
        ("g", "sharp"): AbstractNote.gsharp_aflat,
        ("a", "flat"): AbstractNote.gsharp_aflat,
        ("a", "natural"): AbstractNote.anatural,
        ("a", "sharp"): AbstractNote.asharp_bflat,
        ("b", "flat"): AbstractNote.asharp_bflat,
        ("b", "natural"): AbstractNote.bnatural_cflat,
        ("c", "flat"): AbstractNote.bnatural_cflat
    }
    try:
        return note_translation_dict[(note_letter.lower(), note_shift.lower())]
    except AttributeError:
        raise TypeError("note_letter ({}) and/or note_shift ({}) are "
                        "an invalid type".format(note_letter, note_shift))
    except KeyError:
        raise ValueError("note_letter ({}) and/or note_shift ({}) "
                         "do not match with a "
                         "valid AbstractNote".format(note_letter, note_shift))
