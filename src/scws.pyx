# cython: language_level=3
cimport cscws
import platform
from pathlib import Path


if platform.system().lower() == 'windows':
    fpath_encoding = 'ansi'
else:
    fpath_encoding = 'utf-8'

cpdef int _get_int_size():
    return sizeof(int)

cdef class ScwsTopwords:
    '''
    很显然SCWS的设计不是完美的，这就是为什么这个对象只管析构。
    '''
    cdef cscws.scws_topword* head

    def __iter__(self) -> ScwsTopwordsIterator:
        ret = ScwsTopwordsIterator()
        ret._source = self
        ret._cur = self.head
        return ret
    
    def __dealloc__(self):
        cscws.scws_free_tops(self.head)

cdef class ScwsTopwordsIterator:
    cdef ScwsTopwords _source
    cdef cscws.scws_topword* _cur

    def __next__(self) -> ScwsTopwordStructView:
        if self._cur == NULL: raise StopIteration
        ret = ScwsTopwordStructView()
        ret._source = self._source
        ret._c_obj = self._cur
        self._cur = self._cur.next
        return ret

cdef class ScwsTopwordStructView:
    '''
    正如其名，这是对scws_topword的只读封装，并不管理内存。
    但是它会保留来源集合对象的引用以保证自己读取的内存不被GC。
    '''
    cdef ScwsTopwords _source
    cdef cscws.scws_topword* _c_obj
    
    @property
    def word(self) -> bytes:
        return <bytes>(self._c_obj.word)
    
    @property
    def weight(self) -> float:
        return self._c_obj.weight
    
    @property
    def times(self) -> int:
        return self._c_obj.times
    
    @property
    def attr(self) -> bytes:
        return <bytes>(self._c_obj.attr)
    
    def to_dict(self):
        return {
            'word': self._c_obj.word,
            'weight': self._c_obj.weight,
            'times': self._c_obj.times,
            'attr': self._c_obj.attr,
        }


cdef class ScwsResults:
    '''
    同上。
    '''
    cdef cscws.scws_result* head

    def __iter__(self) -> ScwsResultsIterator:
        ret = ScwsResultsIterator()
        ret._source = self
        ret._cur = self.head
        return ret

    def __dealloc__(self):
        cscws.scws_free_result(self.head)

cdef class ScwsResultsIterator:
    cdef ScwsResults _source
    cdef cscws.scws_result* _cur

    def __next__(self) -> ScwsResultView:
        if self._cur == NULL: raise StopIteration
        ret = ScwsResultView()
        ret._source = self._source
        ret._c_obj = self._cur
        self._cur = self._cur.next
        return ret

cdef class ScwsResultView:
    '''
    同上。
    '''
    cdef ScwsResults _source
    cdef cscws.scws_result* _c_obj

    @property
    def off(self) -> int:
        return self._c_obj.off

    @property
    def idf(self) -> float:
        return self._c_obj.idf

    @property
    def len_(self) -> int:
        return self._c_obj.len

    @property
    def attr(self) -> bytes:
        return <bytes>(self._c_obj.attr)

    def to_dict(self):
        return {
            'off': self._c_obj.off,
            'idf': self._c_obj.idf,
            'len': self._c_obj.len,
            'attr': self._c_obj.attr,
        }


cdef class ScwsTokenizer:
    SCWS_IGN_SYMBOL     = 0x01
    SCWS_DEBUG          = 0x08
    SCWS_DUALITY        = 0x10
    SCWS_MULTI_NONE     = 0x00000   # nothing
    SCWS_MULTI_SHORT	= 0x01000   # split long words to short words from left to right
    SCWS_MULTI_DUALITY	= 0x02000   # split every long words(3 chars?) to two chars
    SCWS_MULTI_ZMAIN    = 0x04000   # split to main single chinese char atr = j|a|n?|v?
    SCWS_MULTI_ZALL     = 0x08000   # attr = ** , all split to single chars
    SCWS_MULTI_MASK     = 0xff000   # mask check for multi set

    cdef cscws.scws_tokenizer* _c_obj
    cdef str _charset

    def __cinit__(self):
        self._c_obj = cscws.scws_new()
        self._charset = 'gbk'
    
    def __dealloc__(self):
        cscws.scws_free(self._c_obj)
    
    cpdef fork(self):
        # cython并不支持placement new cdef class
        # 因此fork是参照scws_fork重新实现的
        '''
        /* hightman.110320: fork scws */
        scws_t scws_fork(scws_t p)
        {
            scws_t s = scws_new();

            if (p != NULL && s != NULL)
            {
                s->mblen = p->mblen;
                s->mode = p->mode;
                // fork dict/rules
                s->r = scws_rule_fork(p->r);
                s->d = xdict_fork(p->d);
            }

            return s;
        }
        '''
        child = ScwsTokenizer()
        child._c_obj.mblen = self._c_obj.mblen
        child._c_obj.mode = self._c_obj.mode
        child._c_obj.r = cscws.scws_rule_fork(self._c_obj.r)
        child._c_obj.d = cscws.xdict_fork(self._c_obj.d)

        return child
    
    @property
    def ignore(self) -> bool:
        return bool(self._c_obj.mode & self.SCWS_IGN_SYMBOL)
    
    @ignore.setter
    def ignore(self, ignore: bool):
        cscws.scws_set_ignore(self._c_obj, <int>ignore)
    
    @property
    def duality(self) -> bool:
        return bool(self._c_obj.mode & self.SCWS_DUALITY)

    @duality.setter
    def duality(self, duality: bool):
        cscws.scws_set_duality(self._c_obj, <int>duality)
    
    @property
    def debug(self) -> bool:
        return bool(self._c_obj.mode & self.SCWS_DEBUG)

    @debug.setter
    def debug(self, debug: bool):
        cscws.scws_set_debug(self._c_obj, <int>debug)
    
    @property
    def multi_vals(self) -> int:
        return self._c_obj.mode & self.SCWS_MULTI_MASK
    
    @multi_vals.setter
    def multi_vals(self, multi_vals: int):
        cscws.scws_set_multi(self._c_obj, multi_vals)
    
    @property
    def modes(self) -> int:
        return self._c_obj.mode
    
    @modes.setter
    def modes(self, modes: int):
        self._c_obj.mode = modes
    
    @property
    def charset(self) -> str:
        return self._charset
    
    @charset.setter
    def charset(self, charset: str):
        cscws.scws_set_charset(self._c_obj, charset.encode('ascii'))
        self._charset = charset

    def send_text(self, text: bytes):
        cscws.scws_send_text(self._c_obj, text, len(text))

    def get_result(self) -> ScwsResults:
        ret = ScwsResults()
        ret.head = cscws.scws_get_result(self._c_obj)
        return ret
    
    def get_tops(self, limit: int, xattr: bytes) -> ScwsTopwords:
        ret = ScwsTopwords()
        ret.head = cscws.scws_get_tops(self._c_obj, limit, xattr)
        return ret
    
    def get_words(self, xattr: bytes) -> ScwsTopwords:
        ret = ScwsTopwords()
        ret.head = cscws.scws_get_words(self._c_obj, xattr)
        return ret
    
    def has_word(self, xattr: bytes) -> int:
        return cscws.scws_has_word(self._c_obj, xattr)
    
    def add_dict(self, fpath: str | Path, mode: int) -> int:
        return cscws.scws_add_dict(self._c_obj, str(fpath).encode(encoding=fpath_encoding), mode)

    def set_dict(self, fpath: str | Path, mode: int) -> int:
        return cscws.scws_set_dict(self._c_obj, str(fpath).encode(encoding=fpath_encoding), mode)
    
    def set_rule(self, fpath: str | Path):
        cscws.scws_set_rule(self._c_obj, str(fpath).encode(encoding=fpath_encoding))
