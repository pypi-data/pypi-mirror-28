"""
Functions that are not specific to "Row" objects
"""
import random
import string
import concurrent.futures
import multiprocessing as mp
from itertools import chain, zip_longest, repeat

from datetime import datetime
from dateutil.relativedelta import relativedelta


def dateconv(date, infmt, outfmt):
    """Converts date format

    Args:
        |  date(int or str): 199912 or '1999DEC'
        |  infmt(str): input format
        |  outfmt(str): output format

    Date format examples:
        |  %Y, %m, %d, %b ...
        |  https://docs.python.org/3/library/datetime.html

    Returns str
    """
    return datetime.strftime(datetime.strptime(str(date), infmt), outfmt)


def pmap(fn, *seqs, args=(), max_workers=None):
    """ Parallel map

    |  fn takes a zipped elts of seqs and 'args' as arguments
    |  max_workers is the minimum of 1 and max cpu count of the machine
    """
    max_workers = min(max_workers if isinstance(max_workers, int) else 1,
                      mp.cpu_count())
    if max_workers == 1:
        yield from (fn(*x, *args) for x in zip(*seqs))
    else:
        tempstr = _random_string()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for gs in grouper(zip(*seqs, *(repeat(a) for a in args)),
                              max_workers, tempstr):
                gs = (x for x in gs if x != tempstr)
                yield from executor.map(fn, *zip(*gs))


# copied from 'itertools'
def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks, generator

    Examples:
        >>> grouper('ABCDEFG', 3, 'x')
        ABC DEF Gxx"
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def _random_string(nchars=20):
    "Generates a random string of lengh 'n' with alphabets and digits. "
    chars = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(chars)
                   for _ in range(nchars))


def _peek_first(seq):
    """
    Note:
        peeked first item is pushed back to the sequence
    Args:
        seq (Iter[type])
    Returns:
        Tuple(type, Iter[type])
    """
    # never use tee, it'll eat up all of your memory
    seq1 = iter(seq)
    first_item = next(seq1)
    return first_item, chain([first_item], seq1)


# performance doesn't matter for this, most of the time
def _listify(x):
    """
    Example:
        >>> listify('a, b, c')
        ['a', 'b', 'c']

        >>> listify(3)
        [3]

        >>> listify([1, 2])
        [1, 2]
    """
    try:
        return [x1.strip() for x1 in x.split(',')]
    except AttributeError:
        try:
            return list(iter(x))
        except TypeError:
            return [x]


# If the return value is True it is converted to 1 or 0 in sqlite3
# istext is unncessary for validity check
def isnum(*xs):
    "Tests if x is numeric"
    try:
        for x in xs:
            float(x)
        return True
    except (ValueError, TypeError):
        return False


def ymd(date, size, fmt):
    """Date arithmetic

    Args:
        |  date(int or str): 19991231 or "1999-12-31'
        |  size(str): "3 months"
        |  fmt(str): date format

    Returns int if input(date) is int else str
    """
    if isinstance(size, str):
        n, unit = size.split()
        if not unit.endswith('s'):
            unit = unit + 's'
        size = {unit: int(n)}
    d1 = datetime.strptime(str(date), fmt) + relativedelta(**size)
    d2 = d1.strftime(fmt)
    return int(d2) if isinstance(date, int) else d2