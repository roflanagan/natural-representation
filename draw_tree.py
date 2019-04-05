from natural_representation import natural_representation, evaluate_natural_representation
from fractions import Fraction
from sys import argv

def sort_sequences(sequences):
    return sorted(sequences, key=evaluate_natural_representation)

def children(sequence, include_negative=True):
    result = []
    if sequence == [0] and not include_negative:
        return [[1]]
    if sequence[-1] >= 0:
        result.append(sequence[:-1] + [sequence[-1]+1])
    if sequence[-1] <= 0:
        result.append(sequence[:-1] + [sequence[-1]-1])
    if sequence[-1] != 0 or len(sequence) == 1:
        result.append(sequence + [0])
    return result

def height(sequence):
    return sum(map(abs, sequence)) + len(sequence)

def sequences_by_height(max_height, include_negative=True):
    if max_height == 1:
        return [[[0]]]
    sequences_so_far = sequences_by_height(max_height-1, include_negative)
    next_sequences = []
    for sequence in sequences_so_far[-1]:
        next_sequences += children(sequence, include_negative)
    sequences_so_far.append(next_sequences)
    return sequences_so_far

def all_sequences_up_to_height(max_height, include_negative=True):
    sequence_lists = sequences_by_height(max_height, include_negative)
    return [sequence for sequence_list in sequence_lists for sequence in sequence_list]

def sorted_sequences_up_to_height(max_height, include_negative=True):
    return sort_sequences(all_sequences_up_to_height(max_height, include_negative))

def horizontal_coordinate_to_sequence(max_height, include_negative=True):
    sorted_sequences = sorted_sequences_up_to_height(max_height, include_negative)
    return dict(list(enumerate(sorted_sequences)))

def grid_coordinates_to_sequence(max_height, include_negative=True):
    x_to_sequence = horizontal_coordinate_to_sequence(max_height, include_negative)
    return dict([((x, height(sequence)), sequence) for x, sequence in x_to_sequence.iteritems()])

def sequence_to_grid_coordinates(max_height, include_negative=True):
    coordinates_to_sequence = grid_coordinates_to_sequence(max_height, include_negative)
    return dict([(tuple(sequence), c) for c, sequence in coordinates_to_sequence.iteritems()])

def offset(x_height_1, x_height_2):
    x1, height1 = x_height_1
    x2, height2 = x_height_2
    updown = "uuu" if height2 > height1 else "ddd"
    across = "r" if x2 > x1 else "l"
    return updown * abs(height2 - height1) + across * abs(x2 - x1)

def arrow_annotation(parent_sequence, child_sequence):
    if child_sequence[-1] == 0:
        return ', "\\Diamond2_{{}_{V}}\\Diamond" description'
    if parent_sequence[-1] * child_sequence[-1] > 0:
        return ""
    if child_sequence[-1] == 1 and tuple(parent_sequence) != tuple([0]):
        return ', "\\Diamond" near start'
    if child_sequence[-1] == -1 and tuple(parent_sequence) == tuple([0]):
        return ', "\\Diamond"\''
    return ""

def get_arrow(parent_sequence, child_sequence, sequence_to_coordinates):
    annotation = arrow_annotation(parent_sequence, child_sequence)
    arrow_offset = offset(sequence_to_coordinates[parent_sequence], sequence_to_coordinates[child_sequence])
    return "\\ar[-" + annotation + "]{" + arrow_offset + "}"

def get_arrows(parent_sequence, sequence_to_coordinates):
    if parent_sequence is None:
        return ""
    child_sequences = children(parent_sequence)
    return "".join([get_arrow(tuple(parent_sequence), tuple(child_sequence), sequence_to_coordinates)
                    for child_sequence in child_sequences 
                    if tuple(child_sequence) in sequence_to_coordinates])

def grid_entries(max_height, include_negative=True):
    coordinates_to_sequence = grid_coordinates_to_sequence(max_height, include_negative)
    sequence_to_coordinates = sequence_to_grid_coordinates(max_height, include_negative)
    max_width = len(coordinates_to_sequence)
    add_arrows = lambda x: [x, get_arrows(x, sequence_to_coordinates)]
    return [[add_arrows(coordinates_to_sequence.get((x, height))) for x in range(max_width)] 
            for height in range(1, max_height+1)]

def tikz_cd_table_entry(grid_entry, ratios=False):
    if grid_entry[0] is None:
        return "{}"
    entry, arrows = grid_entry
    if ratios:
        number = evaluate_natural_representation(entry)
        if number.denominator == 1:
            return str(number.numerator) + arrows
        return ("%d/%d" % (number.numerator, number.denominator)) + arrows
    entry_strings = map(str, entry)
    first_entry, rest = entry_strings[0], entry_strings[1:]
    if len(rest) == 0:
        return "\\left [" + first_entry + "\\right ]" + arrows
    return "\\left [" + first_entry + ";" + ",".join(rest) + "\\right ]" + arrows

def insert_empty_rows(grid):
    new_rows = [grid[0]]
    for row in grid[1:]:
        new_rows.append([[None, ""]] * len(row))
        new_rows.append([[None, ""]] * len(row))
        new_rows.append(row)
    return new_rows

def tikz_cd_table(max_height, ratios=False, spacing_reduction=45, include_negative=True):
    grid = insert_empty_rows(grid_entries(max_height, include_negative))
    table_entries = [[tikz_cd_table_entry(entry, ratios) for entry in row]
                     for row in grid]
    table_text = " \\\\ \n".join([(" &[-%dpt] " % spacing_reduction).join(row) 
                                  for row in table_entries[::-1]]) + " \\\\ \n"
    return "\\begin{tikzcd}\n" + table_text + "\\end{tikzcd}\n"


if __name__ == '__main__':
    max_height = 4 if len(argv) < 2 else int(argv[1])
    show_ratios = False if len(argv) < 3 or argv[2] in ['0', 'False', 'false', 'no'] else True
    spacing_reduction = 45 if len(argv) < 4 else int(argv[3])
    include_negative = True if len(argv) < 5 or argv[5] not in ['0', 'False', 'false', 'no'] else False
    print tikz_cd_table(max_height, show_ratios, spacing_reduction, include_negative)