# I have no idea
import functools
import typing
from typing import Any, Generator, Optional, Tuple, Union, Callable, List, Generic

T = typing.TypeVar("T")
U = typing.TypeVar("U")

class ParseException(Exception):
    pass

class Parser(Generic[T]):
    def parse_partial(self, s: str, i: int) -> Tuple[T, int]:
        """Parses a part of s starting from i.
        
        Returns a value and the next character index to parse from. Can raise
        ParseException to stop parsing.
        """
        raise NotImplementedError
    
    def parse(self, s: str) -> T:
        """Parse a whole string to a value."""
        res, start = self.parse_partial(s, 0)
        assert start == len(s), (start, len(s))
        return res
    
    def then(self, other: Union["Parser[U]", str]) -> "Parser[U]":
        """Do self, then other, discarding self."""
        return self >> other
    
    def skip(self, other: Union["Parser[U]", str]) -> "Parser[T]":
        """Do self, then other, discarding other."""
        return self << other
    
    def either(self, other: Union["Parser[U]", str]) -> "Parser[Union[T, U]]":
        """Try self, falling back to other if self fails."""
        return self / other
    
    def concat(self, other: Union["Parser[U]", str]) -> "ConcatParser[T, U]":
        return self + other
    
    def map(self, f: Callable[[T], U]) -> "Parser[U]":
        """Applies a function to a parser's result."""
        @parser
        def map_parser(s: str, i: int) -> Tuple[U, int]:
            t, rest = self.parse_partial(s, i)
            return f(t), rest
        return map_parser
    
    def filter(self, pred: Callable[[T], bool]) -> "Parser[T]":
        """Causes parser to raise ParseException if value doesn't pass pred."""
        @parser
        def filter_parser(s: str, i: int) -> Tuple[T, int]:
            t, rest = self.parse_partial(s, i)
            if not pred(t):
                raise ParseException(f"value {t!r} did not match predicate")
            return t, rest
        return filter_parser
    
    def rep(self) -> "Parser[List[T]]":
        """Repeats a parser until ParseException."""
        @parser
        def rep_parser(s: str, i: int) -> Tuple[List[T], int]:
            out: List[T] = []
            while True:
                try:
                    t, i = self.parse_partial(s, i)
                except ParseException:
                    break
                out.append(t)
            return out, i
        return rep_parser
    
    def rep1(self) -> "Parser[List[T]]":
        """Repeats a parser at least once until ParseException."""
        @parser
        def rep1_parser(s: str, i: int) -> Tuple[List[T], int]:
            t, i = self.parse_partial(s, i)
            out: List[T] = [t]
            while True:
                try:
                    t, i = self.parse_partial(s, i)
                except ParseException:
                    break
                out.append(t)
            return out, i
        return rep1_parser
    
    def repsep(self, sep: Union["Parser[Any]", str]) -> "Parser[List[T]]":
        """Repeats a parser, then a separator, then the parser, ..."""
        if isinstance(sep, str):
            sep = string(sep)
        
        @parser
        def repsep_parser(s: str, i: int) -> Tuple[List[T], int]:
            try:
                t, i = self.parse_partial(s, i)
            except ParseException:
                return [], i
            
            rest, i = (sep >> self).rep().parse_partial(s, i)
            return [t] + rest, i
        return repsep_parser

    def rep_until_chars(self, chars: int) -> "Parser[typing.List[T]]":
        @parser
        def inner(s: str, i: int):
            target = i + chars
            out = []
            while i < target:
                a, i = self.parse_partial(s, i)
                out.append(a)
            if i != target:
                raise ParseException("too many chars parsed")
            return out, i
        return inner

    def times(self, n: int) -> "Parser[List[T]]":
        @parser
        def times_parser(s: str, i: int) -> Tuple[List[T], int]:
            out = []
            for _ in range(n):
                t, i = self.parse_partial(s, i)
                out.append(t)
            return out, i
        return times_parser
    
    def repstr(self) -> "Parser[str]":
        """Repeats a string parser until ParseException."""
        return self.rep().joinstr()
    
    def rep1str(self) -> "Parser[str]":
        """Repeats a string parser at least once until ParseException."""
        return self.rep1().joinstr()
    
    def joinstr(self) -> "Parser[str]":
        """Turns a parser of List[str] to str."""
        return self.map("".join)
    
    def timesstr(self, n: int) -> "Parser[str]":
        return self.times(n).joinstr()
    
    def optional(self) -> "Parser[Optional[T]]":
        """"""
        return self / pure(None)
    
    def __lshift__(self, other: Union["Parser[U]", str]) -> "Parser[U]":
        if isinstance(other, str):
            other = string(other)
        
        @parser
        def skip_parser(s: str, i: int) -> Tuple[Union[T, U], int]:
            t, i = self.parse_partial(s, i)
            _, i = other.parse_partial(s, i)
            return t, i
        return skip_parser
    
    def __rshift__(self, other: Union["Parser[U]", str]) -> "Parser[T]":
        if isinstance(other, str):
            other = string(other)
        
        @parser
        def then_parser(s: str, i: int) -> Tuple[Union[T, U], int]:
            _, i = self.parse_partial(s, i)
            return other.parse_partial(s, i)
        return then_parser
    
    def __truediv__(self, other: Union["Parser[U]", str]) -> "Parser[Union[T, U]]":
        if isinstance(other, str):
            other = string(other)
        
        @parser
        def either_parser(s: str, i: int) -> Tuple[Union[T, U], int]:
            try:
                return self.parse_partial(s, i)
            except ParseException:
                return other.parse_partial(s, i)
        return either_parser
    
    def __add__(self, other: Union["Parser[U]", str]) -> "ConcatParser[T, U]":
        if isinstance(other, str):
            other = string(other)
        return ConcatParser(self, other)


class FunctionParser(Generic[T], Parser[T]):
    def __init__(self, f: Callable[[str, int], Tuple[T, int]]) -> None:
        self.f = f
    
    def parse_partial(self, s: str, i: int) -> Tuple[T, int]:
        return self.f(s, i)

parser = FunctionParser

class LazyParser(Generic[T], Parser[T]):
    def __init__(self, p: Callable[[], Parser[T]]) -> None:
        self.p = p
        self.parser: Optional[Parser[T]] = None
    
    def parse_partial(self, s: str, i: int) -> Tuple[T, int]:
        if not self.parser:
            self.parser = self.p()
        return self.parser.parse_partial(s, i)

lazy = LazyParser

class DoParser(Generic[T], Parser[T]):
    def __init__(self, f: Callable[[], Generator[Union[Parser[Any], str], Any, T]]) -> None:
        self.f = f
    
    def parse_partial(self, s: str, i: int) -> Tuple[T, int]:
        it = self.f()
        try:
            parser = next(it)
            while True:
                if isinstance(parser, str):
                    parser = string(parser)
                to_send, i = parser.parse_partial(s, i)
                parser = it.send(to_send)
        except StopIteration as stop:
            return stop.value, i

do = DoParser

class ConcatParser(Generic[T, U], Parser[Tuple[T, U]]):
    def __init__(self, fst: Parser[T], snd: Parser[U]) -> None:
        self.fst = fst
        self.snd = snd
    
    def parse_partial(self, s: str, i: int) -> Tuple[Tuple[T, U], int]:
        t, i = self.fst.parse_partial(s, i)
        u, i = self.snd.parse_partial(s, i)
        return (t, u), i


def pure(val: T) -> Parser[T]:
    """Returns a parser which immediately returns a value."""
    return parser(lambda _, i: (val, i))

def string(val: str) -> Parser[str]:
    """Returns a parser that expects the exact string given."""
    @parser
    def string_parser(s: str, i: int) -> Tuple[str, int]:
        if s[i:i+len(val)] == val:
            return val, i+len(val)
        else:
            raise ParseException(f"match {val!r} not found in {s[i:i+10]!r}")
    return string_parser

def regex(r: str, flags: int = 0, group = 0) -> Parser[str]:
    ...

@parser
def char(s: str, i: int) -> Tuple[str, int]:
    "Any char."
    if i < len(s):
        return s[i], i+1
    else:
        raise ParseException("char reached eof")

alpha = char.filter(str.isalpha)
word = alpha.rep1str()

space = char.filter(str.isspace)
spaces = space.rep1str()

digit_char = char.filter(str.isnumeric)
digit = digit_char.map(int)
number_nosign_str = digit_char.rep1str()
number_nosign = number_nosign_str.map(int)
number_str = (string("-") / string("+") / pure("") + number_nosign_str).joinstr()
number = number_str.map(int)

if __name__ == "__main__":
    @do
    def test():
        i = yield number
        yield '-'
        c = yield number
        return (i, c)

    print(test.repsep(space).parse("123-4 5-6 7-8"))

    parens = lazy(lambda: string('(') >> parens.rep().map(tuple) << string(')'))
    
    print(parens.parse("((())()())"))

    aoc2018day20_paren = lazy(lambda: string('(') >> aoc2018day20_parts.repsep('|') << string(')'))
    aoc2018day20_dir = char.filter("NESW".__contains__).rep1str()
    aoc2018day20_part = aoc2018day20_dir.either(aoc2018day20_paren)
    aoc2018day20_parts = aoc2018day20_part.rep()
    aoc2018day20 = string('^') >> aoc2018day20_parts << string('$')

    def aoc2018day20_expand(l):
        out = [""]
        for c in l:
            if isinstance(c, str):
                out = [x + c for x in out]
            else:
                out = [x + c for v in c for c in aoc2018day20_expand(v) for x in out]
        return out
    result = aoc2018day20.parse('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')
    print(result)
    print(aoc2018day20_expand(result))
