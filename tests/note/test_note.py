import unittest
from note.note import AbstractNote, convert_note_to_abstract, parse_note_shift

BASIC_CHECK_NUMBERS = (-1, 0, 1, 100)


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
                self.assertRaises(ValueError, AbstractNote, invalid_input)


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
                self.assertRaises(ValueError, parse_note_shift, invalid_input)

    def test_raises_exception_with_invalid_input_type(self):
        invalid_inputs = BASIC_CHECK_NUMBERS

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                self.assertRaises(TypeError, parse_note_shift, invalid_input)


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
                self.assertRaises(ValueError,
                                  convert_note_to_abstract,
                                  *invalid_input)

    def test_raises_exception_with_invalid_input_type(self):
        invalid_inputs = BASIC_CHECK_NUMBERS

        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                self.assertRaises(TypeError,
                                  convert_note_to_abstract,
                                  invalid_input)
