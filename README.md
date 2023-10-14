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
result = list(r.to_dict() for r in stk.get_result())
```
能跑通，就是结果比较幽默（Windows）：
```python
[{'off': 0, 'idf': 0.0, 'len': 1, 'attr': b'un'}, {'off': 1, 'idf': 0.0, 'len': 1, 'attr': b'en'}]
```
