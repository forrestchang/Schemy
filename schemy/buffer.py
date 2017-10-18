# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

"""
The buffer module assists in iterating through lines and tokens.
"""

import math

class Buffer:
    """
    A buffer provides a way of accessing a sequence of tokens across lines.

    >>> buf = Buffer(iter([['(', '+'], [15], [12, ')']]))
    >>> buf.pop()
    '('
    >>> buf.pop()
    '+'
    >>> buf.current()
    15
    >>> print(buf)
    1: ( +
    2: >> 15
    """

    def __init__(self, source):
        self.index = 0
        self.lines = []
        self.source = source
        self.current_lines = ()
        self.current()

    def pop(self):
        """
        Remove the next item from self and return it.
        """
        current = self.current()
        self.index += 1
        return current

    @property
    def more_on_line(self):
        return self.index < len(self.current_lines)

    def current(self):
        """
        Return the current element, or None if none exists.
        """
        while not self.more_on_line:
            self.index = 0
            try:
                self.current_line = next(self.source)
                self.lines.append(self.current_line)
            except StopIteration:
                self.current_line = ()
                return None
        return self.current_line[self.index]

    def __str__(self):
        """
        Return recently read contents; current element marked with >>.
        """

        # Fromat string for right-justified line numbers
        n = len(self.lines)
        msg = '{0:>' + str(math.floor(math.log10(n)) + 1) + '}: '

        # Up to three previous lines and current line are included in output
        s = ''
        for i in range(max(0, n-4), n-1):
            s += msg.format(i+1) + ' '.join(map(str, self.lines[i])) + '\n'
        s += msg.format(n)
        s += ' '.join(map(str, self.current_line[:self.index]))
        s += ' >> '
        s += ' '.join(map(str, self.current_line[self.index:]))
        return s.strip()

try:
    import readline
except:
    pass


class InputReader:
    """
    An InputReader is an iterable that prompts the user for input.
    """
    def __init__(self, prompt):
        self.prompt = prompt

    def __iter__(self):
        while True:
            yield  input(self.prompt)
            self.prompt = ' ' * len(self.prompt)


class LineReader:
    """
    A LineReader is an iterable that prints lines after a prompt.
    """
    def __init__(self, lines, prompt, comment=';'):
        self.lines = lines
        self.prompt = prompt
        self.comment = comment

    def __iter__(self):
        while self.lines:
            line = self.lines.pop(0).strip('\n')
            if (self.prompt is not None and line != '' and not line.lstrip().startswith(self.comment)):
                print(self.prompt + line)
                self.prompt = ' ' * len(self.prompt)
            yield line
        raise EOFError