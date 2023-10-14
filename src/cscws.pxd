cdef extern from 'scws/libscws/xdict.h':
    ctypedef struct scws_word:
        float tf
        float idf
        unsigned char flag
        char attr[3]

    ctypedef struct scws_xdict
    ctypedef struct scws_xdict:
        void* xdict
        int xmode
        int ref # hightman.20130110: refcount (zero to really free/close)
        scws_xdict* next

    cdef scws_xdict* xdict_fork(scws_xdict* xd)


cdef extern from 'scws/libscws/pool.h':
    ctypedef struct pheap:
        int size
        int used
        char block[0]

    ctypedef struct pclean
    ctypedef struct pclean:
        void* obj
        pclean* nxt

    ctypedef struct scws_pool:
        int size            # total allocated
        int dirty           # total wasted
        pheap* heap	
        pclean* clean


cdef extern from 'scws/libscws/xtree.h':
    ctypedef struct tree_node
    ctypedef struct tree_node:
        char* key
        void* value
        int vlen
        tree_node* left
        tree_node* right

    ctypedef struct scws_xtree: 
        scws_pool* p        # pool for memory manager
        int base            # base number for hasher (prime number recommend)
        int prime           # good prime number for hasher
        int count           # total nodes
        tree_node* trees    # trees [total=prime+1]


cdef extern from 'scws/libscws/rule.h':
    cdef struct scws_rule_item:
        short flag
        char zmin
        char zmax
        char name[17]
        char attr[3]
        float tf
        float idf
        unsigned int bit  # my bit
        unsigned int inc  # include
        unsigned int exc  # exclude

    cdef struct scws_rule_attr
    cdef struct scws_rule_attr:
        char attr1[2]
        char attr2[2]
        unsigned char npath[2]
        short ratio
        scws_rule_attr* next

    cdef struct scws_rule:
        scws_xtree* tree
        scws_rule_attr attr
        scws_rule_item items[32] # SCWS_RULE_MAX
        int ref # hightman.20130110: refcount (zero to really free/close)

    cdef scws_rule* scws_rule_fork(scws_rule* r)


cdef extern from 'scws/libscws/scws.h':
    cdef struct scws_result
    cdef struct scws_result:
        int off
        float idf
        unsigned char len
        char attr[3]
        scws_result* next

    cdef struct scws_topword
    cdef struct scws_topword:
        char* word
        float weight
        short times
        char attr[2]
        scws_topword* next

    cdef struct scws_zchar:
        int start
        int end

    ctypedef struct scws_st:
        scws_xdict* d
        scws_rule* r
        unsigned char* mblen
        unsigned int mode
        unsigned char* txt
        int zis
        int len
        int off
        int wend
        scws_result* res0
        scws_result* res1
        scws_word*** wmap
        scws_zchar* zmap

ctypedef scws_st scws_tokenizer

cdef extern from 'scws/libscws/scws.h':
    cdef scws_tokenizer* scws_new()
    cdef void scws_free(scws_tokenizer* s)
    cdef scws_tokenizer* scws_fork(scws_tokenizer* s)

    cdef int scws_add_dict(scws_tokenizer* s, const char *fpath, int mode)
    cdef int scws_set_dict(scws_tokenizer* s, const char *fpath, int mode)
    cdef void scws_set_charset(scws_tokenizer* s, const char *cs)
    cdef void scws_set_rule(scws_tokenizer* s, const char *fpath)

    void scws_set_ignore(scws_tokenizer* s, int yes)
    void scws_set_multi(scws_tokenizer* s, int mode)
    void scws_set_debug(scws_tokenizer* s, int yes)
    void scws_set_duality(scws_tokenizer* s, int yes)

    void scws_send_text(scws_tokenizer* s, const char *text, int len)
    scws_result* scws_get_result(scws_tokenizer* s)
    void scws_free_result(scws_result* result)
    scws_topword* scws_get_tops(scws_tokenizer* s, int limit, const char *xattr)
    scws_topword* scws_get_words(scws_tokenizer* s, const char *xattr)
    void scws_free_tops(scws_topword* tops)
    int scws_has_word(scws_tokenizer* s, const char *xattr)
