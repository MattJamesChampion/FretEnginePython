from enum import Enum

DEFAULT_NOTE_SHIFT_VALUE = "natural"


class AbstractNote(Enum):
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


def convert_note_to_abstract(note_letter, note_shift=DEFAULT_NOTE_SHIFT_VALUE):
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
