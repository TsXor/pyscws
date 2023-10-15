# pyscws
SCWS的python接口，用Cython3写成。  

## 用法
整体与libscws近似，只是API改为了面向对象风格。  
`ScwsTokenizer::get_tops`与`ScwsTokenizer::get_words`会返回一个可迭代不可下标的链表wrapper，迭代这个链表wrapper可以得到节点的wrapper。  

## 警告
小孩子不懂事写着玩的。  

## 示例
```python
import pyscws
text = "Hello, 我名字叫李那曲是一个中国人, 我有时买Q币来玩, 我还听说过C#语言"
stk = pyscws.ScwsTokenizer()
stk.charset = 'utf8'
stk.set_dict(r"E:\Users\23Xor\Desktop\dict.utf8.xdb", pyscws.SCWS_XDICT_XDB)
stk.set_rule(r"E:\Users\23Xor\Desktop\rules.utf8.ini")
stk.send_text(text.encode(encoding='utf-8'))
result = list(r.to_dict() for r in stk.get_result_all())
```
能跑通，就是结果比较幽默（Windows）：
```python
[{'off': 0, 'idf': 0.0, 'len': 1, 'attr': b'un'}, {'off': 1, 'idf': 0.0, 'len': 1, 'attr': b'en'}, {'off': 3, 'idf': 0.0, 'len': 1, 'attr': b'en'}, {'off': 4, 'idf': 0.0, 'len': 5, 'attr': b'un'}, {'off': 10, 'idf': 0.0, 'len': 2, 'attr': b'un'}, {'off': 12, 'idf': 0.0, 'len': 1, 'attr': b'en'}, {'off': 16, 'idf': 0.0, 'len': 1, 'attr': b'un'}, {'off': 17, 'idf': 0.0, 'len': 1, 'attr': b'un'}, {'off': 19, 'idf': 1.732867956161499, 'len': 2, 'attr': b'en'}, {'off': 40, 'idf': 0.0, 'len': 4, 'attr': b'un'}, {'off': 48, 'idf': 0.0, 'len': 3, 'attr': b'un'}, {'off': 51, 'idf': 0.0, 'len': 1, 'attr': b'en'}, {'off': 60, 'idf': 0.0, 'len': 1, 'attr': b'un'}, {'off': 68, 'idf': 0.0, 'len': 1, 'attr': b'en'}, {'off': 91, 'idf': 0.0, 'len': 1, 'attr': b'en'}]
```

## 版本
PyPI对于每个版本只允许存在一个文件，即使删除release也无法重传。  
由于作者时常大意，他就是要重传，因此在版本最后加一个“重传号”。  
即x.y.z.a与x.y.z.b事实上都是x.y.z版本。  
