import math


def get_sequence(x, y, length):
    """
    Creates sequence of pseudo-random numbers
    Each element depends on two previous:
    S(i) = (math.tan(S(i-1))+1/math.sin(S(i-2)))*math.cos(S(i-2))
    """
    for j in range(length):
        result = (math.tan(x)+1/math.sin(y))*math.cos(y)
        y = x
        x = result
        yield result


def get_congruent_sequence(a, c, m, t0, length):
    """
    Implementation of linear-congruent method.
    Each element depends on two previous:
    T(i) = (A*T(i-1)+C) mod M
    :param m:  max number in sequence
    :param t0: initial element
    """
    for j in range(length):
        result = (a * t0 + c) % m
        t0 = result
        yield result


def get_adv_sequence(x, y, a, c, m, t0, length):
    """
    Mix of linear-congruent method with sequence of pseudo-random numbers.
    Has more wide range and float numbers.

    Each element depends on two previous:
    S(i) = (math.tan(S(i-1))+1/math.sin(S(i-2)))*math.cos(S(i-2))
    T(i) = (A*T(i-1)+C) mod M
    S(i) = S(i) * T(i)
    """
    for j in range(length):
        congruent_result = (a * t0 + c) % m
        result = (math.tan(x)+1/math.sin(y))*math.cos(y)
        result *= congruent_result
        y = x
        x = result
        t0 = result
        yield result


def check_modulo_one(j, number):
    """
    Checks if one of the ranges in sequence is 1
    If true, returns inverted j
    Else j
    """
    if number == 1:
        j *= -1
    return j


def range_zero_check(j, min, max):
    """
    Checks if one of the ranges in sequence is 0 and j is out of range
    If true, returns inverted j
    Else j
    """
    if j < min == 0 or j > max == 0:
        j *= -1
    return j


def check_range_modulo_zero(j, number):
    """
    If j mod number is 0, trying to add to j factor, mutually simple to number
    """
    if number != 0:
        if j % number == 0:
            j *= (1.5 * number)
    return j


def check_min_range(j, min):
    """
    Checks j >= min
    If false, returns j mod min
    Else j
    """
    if j < min:
        j %= min
    return j


def check_max_range(j, max):
    """
    Checks j <= max
    If false, returns j mod max
    Else j
    """
    if j > max:
        j %= max
    return j


def count_digits(n):
    """
    Count digits in integer
    """
    if n > 0:
        digits = int(math.log10(n)) + 1
    elif n == 0:
        digits = 1
    else:
        digits = int(math.log10(-n)) + 1
    return digits
