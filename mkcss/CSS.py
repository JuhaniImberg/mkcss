"""Contains the CSS class."""

from __future__ import print_function
from __future__ import unicode_literals
from functools import wraps
import sys

from mkcss import Color


class CSS(object):

    """This is used for all generation."""

    def __init__(self):
        self.all = []
        self.text = ""
        self.tabs = 0
        self.compact = False

    def write(self, text):
        """Write some text onto self.text with proper tabs and newlines"""
        self.text += "{0}{1}{2}".format(
            ("" if self.compact else self.tabs * "    "),
            text,
            ("" if self.compact else "\n"))

    def sps(self):
        """Returns a ' ' if not in compact mode"""
        return '' if self.compact else ' '

    def header(self, text):
        """Add a header comment to the CSS"""
        def realcomment():
            """Add a header comment to the CSS"""
            original = self.compact
            self.compact = False
            self._comment(text, strip=False)
            self.compact = original
        self.all.insert(0, {"func": realcomment})

    def _comment(self, text, strip=True):
        """Brutally add a comment to current place in self.text"""
        if "\n" in text:
            self.write("/*")
            for line in text.split("\n"):
                if strip:
                    line = line.strip()
                if self.compact:
                    self.text += line + " "
                else:
                    self.write(" * " + line)
            self.write(" */")
        else:
            self.write("/* {0} */".format(text))

    def selector(self, *tags, **stuff):
        """Decorator for a function. Tags will be used as the selectors tags
           and function body will be used as the declarations."""
        if "values" in stuff:
            values = stuff["values"]

            def anon(values=values):
                """This should be a anonymous function. It just wraps
                stuff[values] keyvalues into a function to be added to all."""
                self.write(
                    (',' + self.sps()).join(tags) + self.sps() + "{")
                self.tabs += 1
                for index in values:
                    self(index, values[index])
                self.tabs -= 1
                self.write("}")
            self.all.append({"func": anon})
        else:
            def realdec(func):
                """Returns the real wrapper"""
                @wraps(func)
                def wrapper(*args, **kwargs):
                    """The actual wrapper"""
                    self.write(
                        (',' + self.sps()).join(tags) + self.sps() + "{")
                    self.tabs += 1
                    if func.__doc__ and not self.compact:
                        self._comment(func.__doc__)
                    func(*args, **kwargs)
                    self.tabs -= 1
                    self.write("}")
                self.all.append({"func": wrapper})
                return wrapper
            return realdec

    def __call__(self, *args, **kwargs):
        """Add a declaration"""
        values = []
        arguments = args[1:]
        if type(arguments[0]) is tuple:
            arguments = arguments[0]
        for i in arguments:
            if type(i) is int or type(i) is float:
                if i == 0:
                    values.append("0")
                else:
                    values.append(str(int(round(i))) + "px")
            elif type(i) is Color:
                values.append(i.rgb())
            elif type(i) is str:
                values.append(i)
        self.write(args[0] + ":" + self.sps() + ' '.join(values) + ";")

    def make(self, filename, dry=False, compact=None):
        """Create the .css file"""
        self.text = ""
        if compact is not None:
            self.compact = compact
        for i in self.all:
            i["func"]()
        if dry:
            print(self.text)
        else:
            print("Making " + filename)
            with open(filename, "w") as fil:
                if sys.version_info >= (3, 0):
                    fil.write(self.text)
                else:
                    fil.write(self.text.encode('utf8'))
                fil.close()
