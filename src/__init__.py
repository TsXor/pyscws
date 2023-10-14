from .scws import ScwsTokenizer, _get_int_size

__all__ = ['ScwsTokenizer']

MADE_INT_SIZE = _get_int_size()

SCWS_WORD_FULL = 0x01   # 多字: 整词
SCWS_WORD_PART = 0x02   # 多字: 前词段
SCWS_WORD_USED = 0x04   # 多字: 已使用
SCWS_WORD_RULE = 0x08   # 多字: 自动识别的
SCWS_WORD_LONG = 0x10   # 多字: 短词组成的长词
SCWS_WORD_MALLOCED  = 0x80  # xdict_query 结果必须调用 free

SCWS_ZFLAG_PUT      = 0x02  # 单字: 已使用
SCWS_ZFLAG_N2       = 0x04  # 单字: 双字名词头
SCWS_ZFLAG_NR2      = 0x08  # 单字: 词头且为双字人名
SCWS_ZFLAG_WHEAD    = 0x10  # 单字: 词头
SCWS_ZFLAG_WPART    = 0x20  # 单字: 词尾或词中
SCWS_ZFLAG_ENGLISH  = 0x40  # 单字: 夹在中间的英文

SCWS_XDICT_PRIME = 0x3ffd    # 词典结构树数：16381
SCWS_XDICT_XDB = 1
SCWS_XDICT_MEM = 2
SCWS_XDICT_TXT = 4      # ...
SCWS_XDICT_SET = 4096   # set flag.

SCWS_IGN_SYMBOL     = 0x01
SCWS_DEBUG          = 0x08
SCWS_DUALITY        = 0x10
SCWS_MULTI_NONE     = 0x00000   # nothing
SCWS_MULTI_SHORT	= 0x01000   # split long words to short words from left to right
SCWS_MULTI_DUALITY	= 0x02000   # split every long words(3 chars?) to two chars
SCWS_MULTI_ZMAIN    = 0x04000   # split to main single chinese char atr = j|a|n?|v?
SCWS_MULTI_ZALL		= 0x08000   # attr = ** , all split to single chars
SCWS_MULTI_MASK		= 0xff000   # mask check for multi set
