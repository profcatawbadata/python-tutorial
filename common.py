#!/usr/bin/env python3

# This is free and unencumbered software released into the public
# domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a
# compiled binary, for any purpose, commercial or non-commercial, and
# by any means.

# In jurisdictions that recognize copyright laws, the author or
# authors of this software dedicate any and all copyright interest in
# the software to the public domain. We make this dedication for the
# benefit of the public at large and to the detriment of our heirs
# and successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to
# this software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <http://unlicense.org>

"""Things that other scripts import and use."""

import itertools
import re


_LINK_REGEX = r'\[(.*?)\]\((.*?)\)'


def find_links(file):
    """Find all markdown links in a file object.

    Yield (lineno, regexmatch) tuples.
    """
    # don't yield same link twice
    seen = set()

    # we need to loop over the file two lines at a time to support
    # multi-line (actually two-line) links, so this is kind of a mess
    firsts, seconds = itertools.tee(file)
    next(seconds)  # first line is never second line

    # we want 1-based indexing instead of 0-based and one-line links get
    # caught from linepair[1], so we need to start at two
    for lineno, linepair in enumerate(zip(firsts, seconds), start=2):
        lines = linepair[0] + linepair[1]
        for match in re.finditer(_LINK_REGEX, lines, flags=re.DOTALL):
            if match.group(0) not in seen:
                seen.add(match.group(0))
                yield match, lineno


def get_markdown_files():
    """Yield the names of all markdown files in this tutorial.

    This assumes that the README contains links to everything.
    """
    yield 'README.md'
    with open('README.md', 'r') as f:
        for match, lineno in find_links(f):
            target = match.group(2)
            # Currently the README doesn't link to itself, but I don't
            # want to break things if it will in the future.
            if target.endswith('.md') and target != 'README.md':
                yield target


def askyesno(question, default=True):
    """Ask a yes/no question and return True or False.

    The default answer is yes if default is True and no if default is
    False.
    """
    if default:
        # yes by default
        question += ' [Y/n] '
    else:
        # no by default
        question += ' [y/N] '
    while True:
        result = input(question).upper().strip()
        if result == 'Y':
            return True
        if result == 'N':
            return False
        if not result:
            return default