"""Note storage and manipluation."""

from enum import Enum
import re

DEFAULT_NOTE_SHIFT_VALUE = "natural"
"""Default value intended for use when note shift is not specified."""
DEFAULT_NOTE_OCTAVE_VALUE = 4
"""Default value intended for use when note octave is not specified."""


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
            note_octave (int, optional): The octave of the note
        Raises:
            ValueError: If note_octave cannot be cast as an int
        """
        self.set_note(note_letter, note_shift)
        self.note_octave = note_octave

    def __str__(self):
        """Return the string representation of Note."""
        return self.note.name + str(self.note_octave)

    @property
    def note(self):
        """Return the stored note."""
        return self._note

    def set_note(self, note_letter, note_shift=DEFAULT_NOTE_SHIFT_VALUE):
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
            note_letter (str): The note letter to update the Note with
            note_shift (str, optional): The note shift to update the Note with

        """
        self._note_letter = note_letter
        self._note_shift = note_shift
        self._note = convert_note_to_abstract(note_letter, note_shift)

    @property
    def note_octave(self):
        """Return the stored note's octave."""
        return self._note_octave

    @note_octave.setter
    def note_octave(self, input_note_octave=DEFAULT_NOTE_OCTAVE_VALUE):
        """Set the stored note's octave.

        Args:
            input_note_octave (str, optional): The note octave to update the
                Note with

        Raises:
            ValueError: If input_note_octave cannot be cast as an int
        """
        try:
            input_note_octave = int(input_note_octave)
        except ValueError:
            # The reason that this exception is caught and then immediately
            # re-raised is because the contract of this function dictates that
            # ValueError can be raised depending on the arguments used. As
            # such, it seemed wise to make the fact that casting as an int can
            # throw a ValueError explicit so that the location/cause of the
            # potential exception is clear.
            raise

        if 0 <= input_note_octave <= 10:
            self._note_octave = input_note_octave
        else:
            raise ValueError("input_note_octave ({}) must be between 0 and "
                             "10".format(input_note_octave))


def parse_note_string(note_string):
    """Parse a note string and return the note letter and note shift.

    This function takes a human readable note string, meant to represent one of
    the notes in the English chromatic scale, and returns the component
    parts (the note letter and whether it is shifted up (sharp), shifted down
    (flat) or not at all (natural)).

    This function is designed to work cooperatively with the function
    convert_note_to_abstract, which requires specific values to work correctly.
    As such, this function is able to take an unrefined input string and
    prepare it in such a way that it is valid for convert_note_to_abstract.

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
