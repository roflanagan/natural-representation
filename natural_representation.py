from fractions import Fraction
from math import floor
from numpy import array

def natural_representation(f):
    """
    Compute the sequence of integers in the natural representation of the fraction f
    """
    integer_part = int(floor(f))
    if f == integer_part:
        return [integer_part]
    fractional_part = f - integer_part
    if fractional_part >= 0.5: 
        return [integer_part + 1] + natural_representation(1 / (1-fractional_part) - 2)
    else:
        rest = array(natural_representation(1 / fractional_part - 2))
        return [integer_part + 1] + list(-rest)

def evaluate_natural_representation(sequence):
    """
    Compute the fraction f from the sequence of integers in its natural representation
    """
    rest_of_sequence = array(sequence[1:])
    if len(rest_of_sequence) == 0:
        return sequence[0]
    if rest_of_sequence[0] >= 0:
        rest = evaluate_natural_representation(rest_of_sequence)
        return sequence[0] - Fraction(1, 2 + rest)
    else:
        rest = evaluate_natural_representation(-rest_of_sequence)
        return sequence[0] - 1 + Fraction(1, 2 + rest)

def show_examples(max_numerator, max_denominator):
    """
    Encode and decode all positive and negative rational numbers whose numerators
    and denominators don't exceed the specified limits
    """
    from fractions import gcd as greatest_common_divisor
    for n in range(-max_numerator, max_numerator + 1):
        for d in range(1, max_denominator + 1):
            if greatest_common_divisor(n, d) == 1:
                fraction = Fraction(n, d)
                sequence = natural_representation(fraction)
                recovered_fraction = evaluate_natural_representation(sequence)
                print fraction, "\t-->", str(sequence).ljust(12), "-->", recovered_fraction


if __name__ == "__main__":
    show_examples(9, 9)