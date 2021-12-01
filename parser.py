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
        raise NotImplementedError
    
    def parse(self, s: str) -> T:
        res, start = self.parse_partial(s, 0)
        assert start == len(s)
        return res
    
    def then(self, other: Union["Parser[U]", str]) -> "Parser[U]":
        return self >> other
    
    def skip(self, other: Union["Parser[U]", str]) -> "Parser[T]":
        return self << other
    
    def map(self, f: Callable[[T], U]) -> "Parser[U]":
        @parser
        def map_parser(s: str, i: int) -> Tuple[U, int]:
            t, rest = self.parse_partial(s, i)
            return f(t), rest
        return map_parser
    
    def filter(self, f: Callable[[T], bool]) -> "Parser[T]":
        @parser
        def filter_parser(self, s: str, i: int) -> Tuple[T, int]:
            t, rest = self.parse_partial(s, i)
            if not f(t):
                raise ParseException(f"value {t!r} did not match predicate")
        return filter_parser
    
    def rep(self) -> "Parser[List[T]]":
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
    
    def repstr(self) -> "Parser[str]":
        return self.rep().joinstr()
    
    def rep1str(self) -> "Parser[str]":
        return self.rep1().joinstr()
    
    def joinstr(self) -> "Parser[str]":
        return self.map("".join)
    
    def optional(self) -> "Parser[Optional[T]]":
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
    
    def __add__(self, other: Union["Parser[U]", str]) -> "ConcatParser[Union[T, U]]":
        if isinstance(other, str):
            other = string(other)
        return ConcatParser([self, other])


class FunctionParser(Generic[T], Parser[T]):
    def __init__(self, f: Callable[[str, int], Tuple[T, int]]) -> None:
        self.f = f
    
    def parse_partial(self, s: str, i: int) -> Tuple[T, int]:
        return self.f(s, i)

parser = FunctionParser

def do(f: Callable[[], Generator[Union[Parser[Any], str], Any, T]]):
    @parser
    @functools.wraps(f)
    def parse_partial(s: str, i: int) -> Tuple[T, int]:
        it = f()
        parser = next(it)
        while True:
            if isinstance(parser, str):
                parser = string(parser)
            to_send, i = parser.parse_partial(s, i)
            try:
                parser = it.send(to_send)
            except StopIteration as s:
                return s.value, i
    return parse_partial

class ConcatParser(Generic[T], Parser[List[T]]):
    def __init__(self, parsers: List[Parser[T]]):
        self.parsers = parsers
    
    def parse_partial(self, s: str, i: int) -> Tuple[List[T], int]:
        out: List[T] = []
        for parser in self.parsers:
            result, i = parser.parse_partial(s, i)
            out.append(result)
        return out, i
    
    def __add__(self, other: "Parser[U]") -> "ConcatParser[Union[T, U]]":
        return ConcatParser(self.parsers + [other])


def pure(val: T) -> Parser[T]:
    return parser(lambda _, i: (val, i))

def char(predicate: Callable[[str], bool] = lambda x: True):
    @parser
    def char_parser(s: str, i: int) -> Tuple[str, int]:
        if i < len(s):
            if not predicate(s[i]):
                raise ParseException("char didn't meet predicate")
            else:
                return s[i], i+1
        else:
            raise ParseException("char reached eof")
    return char_parser

def string(val: str) -> Parser[str]:
    @parser
    def string_parser(s: str, i: int) -> Tuple[str, int]:
        if s[i:i+len(val)] == val:
            return val, i+len(val)
        else:
            raise ParseException(f"match {val!r} not found in {s[i:i+10]!r}")
    return string_parser

def regex(r: str, flags: int = 0, group = 0) -> Parser[str]:
    ...

alpha = char(str.isalpha)
word = alpha.rep1str()

space = char(str.isspace)
spaces = space.rep1str()

digit_char = char(str.isnumeric)
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
