import unittest
from note.note import (AbstractNote,
                       convert_note_to_abstract,
                       DEFAULT_NOTE_OCTAVE_VALUE,
                       DEFAULT_NOTE_SHIFT_VALUE,
                       is_note_valid,
                       is_abstract_note_valid,
                       is_note_letter_valid,
                       is_note_shift_valid,
                       is_note_octave_valid,
                       Note,
                       parse_note_shift,
                       parse_note_string)

BASIC_CHECK_NUMBERS = (-1, 0, 1, 100)
BASIC_CHECK_STRINGS = ("test", "ABCDEFG", ".?!", " ", "")


class TestAbstractNote(unittest.TestCase):
    def test_init_does_not_throw_exceptions_with_valid_input(self):
        valid_inputs = (
            0,
            1,
            5,
            11
        )

        for valid_input in valid_inputs:
            with self.subTest(valid_input=valid_input):
                try:
                    AbstractNote(valid_input)
                except Exception:
                    self.fail("AbstractNote threw an exception with "
                              "valid arguments")

    def test_init_throws_exception_with_invalid_input_value(self):
        invalid_inputs = (
            "H",
            "z",
            -1,
            100
        )

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(ValueError):
                    AbstractNote(invalid_input)

    def test_addition_returns_correct_result(self):
        argument_result_triples = (
            ((AbstractNote.bnatural_cflat, 2), AbstractNote.csharp_dflat),
            ((AbstractNote.bsharp_cnatural, 5), AbstractNote.esharp_fnatural),
            ((AbstractNote.enatural_fflat, 9), AbstractNote.csharp_dflat),
            ((AbstractNote.anatural, 299), AbstractNote.gsharp_aflat),
            ((AbstractNote.anatural, -2), AbstractNote.gnatural)
        )

        for (note, modifier), intended_result in argument_result_triples:
            with self.subTest(arguments=((note, modifier), intended_result)):
                actual_result = note + modifier
                self.assertEqual(actual_result, intended_result)

    def test_subtraction_returns_correct_result(self):
        argument_result_triples = (
            ((AbstractNote.bsharp_cnatural, 4), AbstractNote.gsharp_aflat),
            ((AbstractNote.enatural_fflat, 9), AbstractNote.gnatural),
            ((AbstractNote.dnatural, 299), AbstractNote.dsharp_eflat),
            ((AbstractNote.fsharp_gflat, -2), AbstractNote.gsharp_aflat)
        )

        for (note, modifier), intended_result in argument_result_triples:
            with self.subTest(argument=((note, modifier), intended_result)):
                actual_result = note - modifier
                self.assertEqual(actual_result, intended_result)


class TestNote(unittest.TestCase):
    valid_note_octaves = (
        0,
        1,
        4,
        10
    )

    invalid_note_octave_values = (
        -1,
        11,
        100
    )

    invalid_note_octave_types = (
        [10],
        (5,)
    )

    def setUp(self):
        self.note_letter = "C"
        self.note_shift = "Natural"
        self.note_octave = 4

    def test_init_does_not_throw_exception_with_valid_note(self):
        note_argument_tuples = (
            ("F", "flat", 0),
            ("G", "SHARP", 9),
            ("A", "FlAt", 5),
            ("B", "shaRP", 7),
            ("C", "Natural"),
            ("D", "NATURAL"),
            ("e", "natural"),
            ("f", "nAtUrAl"),
            ("G", "flat"),
            ("a", "SHARP"),
            ("b"),
            ("C"),
        )

        for note_argument_tuple in note_argument_tuples:
            with self.subTest(note_argument_tuple=note_argument_tuple):
                try:
                    Note(*note_argument_tuple)
                except Exception:
                    self.fail("Note init threw an exception with "
                              "valid arguments")

    def test_init_sets_values_correctly_with_valid_values(self):
        note_argument_result_tuples = (
            (("F", "flat", 0), (AbstractNote.enatural_fflat,
                                0)),
            (("G", "SHARP", 9), (AbstractNote.gsharp_aflat,
                                 9)),
            (("A", "FlAt", 5), (AbstractNote.gsharp_aflat,
                                5)),
            (("B", "shaRP", 7), (AbstractNote.bsharp_cnatural,
                                 7)),
            (("C", "Natural"), (AbstractNote.bsharp_cnatural,
                                DEFAULT_NOTE_OCTAVE_VALUE)),
            (("D", "NATURAL"), (AbstractNote.dnatural,
                                DEFAULT_NOTE_OCTAVE_VALUE)),
            (("e", "natural"), (AbstractNote.enatural_fflat,
                                DEFAULT_NOTE_OCTAVE_VALUE)),
            (("f", "nAtUrAl"), (AbstractNote.esharp_fnatural,
                                DEFAULT_NOTE_OCTAVE_VALUE)),
            (("G", "flat"), (AbstractNote.fsharp_gflat,
                             DEFAULT_NOTE_OCTAVE_VALUE)),
            (("a", "SHARP"), (AbstractNote.asharp_bflat,
                              DEFAULT_NOTE_OCTAVE_VALUE)),
            (("b"), (AbstractNote.bnatural_cflat,
                     DEFAULT_NOTE_OCTAVE_VALUE)),
            (("C"), (AbstractNote.bsharp_cnatural,
                     DEFAULT_NOTE_OCTAVE_VALUE))
        )

        for note_argument_result_tuple in note_argument_result_tuples:
            arguments, results = note_argument_result_tuple
            with self.subTest(args=(arguments, results)):
                test_note = Note(*arguments)

                self.assertEqual(test_note.abstract_note, results[0])
                self.assertEqual(test_note.note_octave, results[1])

    def test_init_raises_exception_with_invalid_note_letter_value(self):
        invalid_note_letters = (
            "H",
            "z",
            ".?!",
            " ",
            ""
        )

        for invalid_note_letter in invalid_note_letters:
            with self.subTest(invalid_note_letter=invalid_note_letter):
                with self.assertRaises(ValueError):
                    Note(invalid_note_letter,
                         self.note_shift,
                         self.note_octave)

    def test_init_raises_exception_with_invalid_note_letter_type(self):
        invalid_note_letters = BASIC_CHECK_NUMBERS

        for invalid_note_letter in invalid_note_letters:
            with self.subTest(invalid_note_letter=invalid_note_letter):
                with self.assertRaises(TypeError):
                    Note(invalid_note_letter,
                         self.note_shift,
                         self.note_octave)

    def test_init_raises_exception_with_invalid_note_shift_value(self):
        invalid_note_shifts = BASIC_CHECK_STRINGS

        for invalid_note_shift in invalid_note_shifts:
            with self.subTest(invalid_note_shift=invalid_note_shift):
                with self.assertRaises(ValueError):
                    Note(self.note_letter,
                         invalid_note_shift,
                         self.note_octave)

    def test_init_raises_exception_with_invalid_note_shift_type(self):
        invalid_note_shifts = BASIC_CHECK_NUMBERS

        for invalid_note_shift in invalid_note_shifts:
            with self.subTest(invalid_note_shift=invalid_note_shift):
                with self.assertRaises(TypeError):
                    Note(self.note_letter,
                         invalid_note_shift,
                         self.note_octave)

    def test_init_raises_exception_with_invalid_note_octave_value(self):
        invalid_note_octaves = self.invalid_note_octave_values

        for invalid_note_octave in invalid_note_octaves:
            with self.subTest(invalid_note_octave=invalid_note_octave):
                with self.assertRaises(ValueError):
                    Note(self.note_letter,
                         self.note_shift,
                         invalid_note_octave)

    def test_init_raises_exception_with_invalid_note_octave_type(self):
        invalid_note_octaves = self.invalid_note_octave_types

        for invalid_note_octave in invalid_note_octaves:
            with self.subTest(invalid_note_octave=invalid_note_octave):
                with self.assertRaises(TypeError):
                    Note(self.note_letter,
                         self.note_shift,
                         invalid_note_octave)

    def test_note_octave_updates_correctly(self):
        valid_note_octaves = self.valid_note_octaves

        for valid_note_octave in valid_note_octaves:
            with self.subTest(valid_note_octave=valid_note_octave):
                test_note = Note(self.note_letter,
                                 self.note_shift,
                                 self.note_octave)

                test_note.note_octave = valid_note_octave

                self.assertEqual(test_note.note_octave, int(valid_note_octave))

    def test_note_octave_update_raises_exception_with_invalid_value(self):
        invalid_note_octaves = self.invalid_note_octave_values

        for invalid_note_octave in invalid_note_octaves:
            with self.subTest(invalid_note_octave=invalid_note_octave):
                test_note = Note(self.note_letter,
                                 self.note_shift,
                                 DEFAULT_NOTE_OCTAVE_VALUE)

                with self.assertRaises(ValueError):
                    test_note.note_octave = invalid_note_octave

    def test_note_octave_update_raises_exception_with_invalid_type(self):
        invalid_note_octaves = self.invalid_note_octave_types

        for invalid_note_octave in invalid_note_octaves:
            with self.subTest(invalid_note_octave=invalid_note_octave):
                test_note = Note(self.note_letter,
                                 self.note_shift,
                                 DEFAULT_NOTE_OCTAVE_VALUE)

                with self.assertRaises(TypeError):
                    test_note.note_octave = invalid_note_octave

    def test_set_note_updates_correctly(self):
        valid_note_arguments = (
            ("A", "flat", 0),
            ("b", "SHARP", 10),
            ("C", "NATURAL", 5),
            ("d", "fLaT"),
            ("E", "SHarP"),
            ("f"),
            ("G")
        )

        for note_arguments in valid_note_arguments:
            with self.subTest(note_arguments=note_arguments):
                test_note = Note(self.note_letter,
                                 self.note_shift,
                                 self.note_octave)

                intended_result = Note(*note_arguments)

                test_note.set_note(*note_arguments)

                self.assertEqual(test_note, intended_result)


class TestIsNoteValid(unittest.TestCase):
    valid_notes = (
        Note("A"),
        Note("b", "flat"),
        Note("C", "SHARP"),
        Note("d", note_octave=7),
        Note("e", "natural", 9)
    )

    class InvalidNote:
        def __init__(self, note_letter, note_shift, note_octave):
            self.note_letter = note_letter
            self.note_shift = note_shift
            self.note_octave = note_octave

    invalid_notes = (
        InvalidNote("Z", DEFAULT_NOTE_SHIFT_VALUE, DEFAULT_NOTE_OCTAVE_VALUE),
        InvalidNote("b", "abc", DEFAULT_NOTE_OCTAVE_VALUE),
        InvalidNote("C", DEFAULT_NOTE_SHIFT_VALUE, 100)
    )

    def test_returns_true_for_valid_note(self):
        for valid_note in self.valid_notes:
            with self.subTest(valid_note=valid_note):
                self.assertTrue(is_note_valid(valid_note))

    def test_returns_false_for_invalid_note(self):
        for invalid_note in self.invalid_notes:
            with self.subTest(invalid_note=invalid_note):
                self.assertFalse(is_note_valid(invalid_note))


class TestIsAbstractNoteValid(unittest.TestCase):
    valid_abstract_notes = AbstractNote
    invalid_abstract_notes = BASIC_CHECK_NUMBERS + BASIC_CHECK_STRINGS

    def test_returns_true_for_valid_abstract_note(self):
        for valid_abstract_note in self.valid_abstract_notes:
            with self.subTest(valid_abstract_note=valid_abstract_note):
                self.assertTrue(is_abstract_note_valid(valid_abstract_note))

    def test_returns_false_for_invalid_abstract_note(self):
        for invalid_abstract_note in self.invalid_abstract_notes:
            with self.subTest(invalid_abstract_note=invalid_abstract_note):
                self.assertFalse(is_abstract_note_valid(invalid_abstract_note))


class TestIsNoteLetterValid(unittest.TestCase):
    valid_note_letters = (
        "A",
        "b",
        "D",
        "g",
    )

    invalid_note_letters = (
        "h",
        "Q",
        "z",
        "."
    )

    invalid_note_letter_types = (
        ["A"],
        (7),
        1
    )

    def test_returns_true_for_valid_note_letter(self):
        valid_note_letters = self.valid_note_letters

        for valid_note_letter in valid_note_letters:
            with self.subTest(valid_note_letter=valid_note_letter):
                self.assertTrue(is_note_letter_valid(valid_note_letter))

    def test_returns_false_for_invalid_note_letter(self):
        invalid_note_letters = self.invalid_note_letters

        for invalid_note_letter in invalid_note_letters:
            with self.subTest(invalid_note_letter=invalid_note_letter):
                self.assertFalse(is_note_letter_valid(invalid_note_letter))

    def test_raises_exception_with_invalid_note_letter_type(self):
        invalid_note_letters = self.invalid_note_letter_types

        for invalid_note_letter in invalid_note_letters:
            with self.subTest(invalid_note_letter=invalid_note_letter):
                with self.assertRaises(TypeError):
                    is_note_letter_valid(invalid_note_letter)


class TestIsNoteShiftValid(unittest.TestCase):
    valid_note_shifts = (
        "sharp",
        "NATURAL",
        "FlAt",
        "b",
        "#"
    )

    invalid_note_shifts = (
        "shrp",
        "test",
        "##",
        "bb",
        "FLAT!"
    )

    invalid_note_shift_types = (
        ["sharp"],
        (17,),
        2
    )

    def test_returns_true_for_valid_note_shift(self):
        for valid_note_shift in self.valid_note_shifts:
            with self.subTest(valid_note_shift=valid_note_shift):
                self.assertTrue(is_note_shift_valid(valid_note_shift))

    def test_returns_false_for_invalid_note_shift(self):
        for invalid_note_shift in self.invalid_note_shifts:
            with self.subTest(invalid_note_shift=invalid_note_shift):
                self.assertFalse(is_note_shift_valid(invalid_note_shift))

    def test_raises_exception_with_invalid_note_shift_type(self):
        for invalid_note_shift in self.invalid_note_shift_types:
            with self.subTest(invalid_note_shift=invalid_note_shift):
                with self.assertRaises(TypeError):
                    is_note_shift_valid(invalid_note_shift)


class TestIsNoteOctaveValid(unittest.TestCase):
    valid_note_octaves = (
        0,
        3,
        5,
        7,
        10
    )

    invalid_note_octaves = (
        -100,
        -1,
        11,
        100
    )

    invalid_note_octave_types = (
        [3],
        (7,),
        "A",
        "z"
    )

    def test_returns_true_for_valid_note_octave(self):
        for valid_note_octave in self.valid_note_octaves:
            with self.subTest(valid_note_octave=valid_note_octave):
                self.assertTrue(is_note_octave_valid(valid_note_octave))

    def test_returns_false_for_invalid_note_octave(self):
        for invalid_note_octave in self.invalid_note_octaves:
            with self.subTest(invalid_note_octave=invalid_note_octave):
                self.assertFalse(is_note_octave_valid(invalid_note_octave))

    def test_raises_exception_for_invalid_note_octave_type(self):
        for invalid_note_octave in self.invalid_note_octave_types:
            with self.subTest(invalid_note_octave=invalid_note_octave):
                with self.assertRaises(TypeError):
                    is_note_octave_valid(invalid_note_octave)


class TestParseNoteString(unittest.TestCase):
    def test_does_not_throw_exception_with_valid_input(self):
        note_strings = (
            "C natural",
            "cnatural",
            "D Sharp",
            "Eflat",
            "G #",
            "Ab",
            "Bb",
            "bb",
            "Cb",
            "d",
            "E"
        )

        for note_string in note_strings:
            with self.subTest(note_string=note_string):
                try:
                    parse_note_string(note_string)
                except Exception:
                    self.fail("parse_note_string failed with a valid string")

    def test_returns_correct_result_on_valid_input(self):
        argument_result_pairs = (
            ("A", ("a", "natural")),
            ("bb", ("b", "flat")),
            ("Cflat", ("c", "flat")),
            ("D SHARP", ("d", "sharp")),
            ("e nAtUrAl", ("e", "natural")),
            ("f #", ("f", "sharp")),
        )

        for argument_result_pair in argument_result_pairs:
            argument, intended_result = argument_result_pair
            with self.subTest(argument_result_pair=argument_result_pair):
                actual_result = parse_note_string(argument)
                self.assertEqual(actual_result, intended_result)

    def test_raises_exception_with_invalid_note_string_value(self):
        invalid_note_strings = (
            "H",
            "z",
            "#d",
            "ba"
        )

        for invalid_note_string in invalid_note_strings:
            with self.subTest(invalid_note_string=invalid_note_string):
                with self.assertRaises(ValueError):
                    parse_note_string(invalid_note_string)

    def test_raises_exception_with_invalid_note_string_type(self):
        invalid_note_strings = BASIC_CHECK_NUMBERS

        for invalid_note_string in invalid_note_strings:
            with self.subTest(invalid_note_string=invalid_note_string):
                with self.assertRaises(TypeError):
                    parse_note_string(invalid_note_strings)


class TestParseNoteShift(unittest.TestCase):
    def test_does_not_throw_exception_with_valid_input(self):
        note_shift_strings = (
            "#",
            "b",
            "flat",
            "FLAT",
            "fLaT",
            "NATURAL",
            "ShArP"
        )

        for note_shift_string in note_shift_strings:
            with self.subTest(note_shift_string=note_shift_string):
                try:
                    parse_note_shift(note_shift_string)
                except Exception:
                    self.fail("parse_note_shift failed with a valid string")

    def test_returns_correct_result_on_valid_input(self):
        argument_result_pairs = (
            ("#", "sharp"),
            ("b", "flat"),
            ("flat", "flat"),
            ("FLAT", "flat"),
            ("fLaT", "flat"),
            ("NATURAL", "natural"),
            ("ShArP", "sharp")
        )

        for argument_result_pair in argument_result_pairs:
            argument, intended_result = argument_result_pair
            with self.subTest(argument_result_pair=argument_result_pair):
                actual_result = parse_note_shift(argument)
                self.assertEqual(actual_result, intended_result)

    def test_raises_exception_with_invalid_input_value(self):
        invalid_inputs = (
            "Test",
            "flt",
            "SHRP"
        )

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(ValueError):
                    parse_note_shift(invalid_input)

    def test_raises_exception_with_invalid_input_type(self):
        invalid_inputs = BASIC_CHECK_NUMBERS

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(TypeError):
                    parse_note_shift(invalid_input)


class TestConvertNoteToAbstract(unittest.TestCase):
    def test_does_not_throw_exception_with_valid_input(self):
        argument_pairs = (
            ("a", "flat"),
            ("b", "natural"),
            ("c", "sharp"),
            ("d")
        )

        for argument_pair in argument_pairs:
            with self.subTest(argument_pair=argument_pair):
                try:
                    convert_note_to_abstract(*argument_pair)
                except Exception:
                    self.fail("convert_note_to_abstract failed with "
                              "valid input")

    def test_returns_correct_result_on_valid_input(self):
        argument_result_pairs = (
            (("A", "FLAT"), AbstractNote.gsharp_aflat),
            (("b", "natural"), AbstractNote.bnatural_cflat),
            (("G", "Sharp"), AbstractNote.gsharp_aflat),
            (("d"), AbstractNote.dnatural)
        )

        for argument_result_pair in argument_result_pairs:
            argument, intended_result = argument_result_pair
            with self.subTest(argument_result_pair=argument_result_pair):
                actual_result = convert_note_to_abstract(*argument)

                self.assertEqual(actual_result, intended_result)

    def test_raises_exception_with_invalid_input_value(self):
        invalid_inputs = (
            ("H"),
            ("z"),
            ("m", "flat"),
            ("a", "abcdefg")
        )

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(ValueError):
                    convert_note_to_abstract(*invalid_input)

    def test_raises_exception_with_invalid_input_type(self):
        invalid_inputs = BASIC_CHECK_NUMBERS

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(TypeError):
                    convert_note_to_abstract(invalid_input)
