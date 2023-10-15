from typing import Union, TypedDict, Generator
from pathlib import Path


def _get_int_size() -> int: pass


class ScwsTopWordAttrs(TypedDict):
    word: bytes
    weight: float
    times: int
    attr: bytes

class ScwsTopwordStructView:
    word: bytes
    weight: float
    times: int
    attr: bytes
    def to_dict(self) -> ScwsTopWordAttrs: pass

class ScwsTopwordsIterator:
    def __next__(self) -> ScwsTopwordStructView: pass

class ScwsTopwords:
    def __iter__(self) -> ScwsTopwordsIterator: pass


class ScwsResultAttrs(TypedDict):
    off: int
    idf: float
    len: int
    attr: bytes

class ScwsResultView:
    off: int
    idf: float
    len: int
    attr: bytes
    def to_dict(self) -> ScwsResultAttrs: pass

class ScwsResultsIterator:
    def __next__(self) -> ScwsResultView: pass

class ScwsResults:
    def __iter__(self) -> ScwsResultsIterator: pass


class ScwsResultEnd(Exception): pass


class ScwsTokenizer:
    ignore: bool
    duality: bool
    debug: bool
    multi_vals: int
    modes: int
    charset: str

    def fork(self) -> 'ScwsTokenizer': pass
    def send_text(self, text: bytes) -> None: pass
    def get_result(self) -> ScwsResults: pass
    def get_result_all(self) -> Generator[ScwsResultView, None, None]: pass
    def get_tops(self, limit: int, xattr: bytes) -> ScwsTopwords: pass
    def get_words(self, xattr: bytes) -> ScwsTopwords: pass
    def has_word(self, xattr: bytes) -> bool: pass
    def add_dict(self, fpath: Union[str, Path], mode: int) -> None: pass
    def set_dict(self, fpath: Union[str, Path], mode: int) -> None: pass
    def set_rule(self, fpath: Union[str, Path]) -> None: pass
