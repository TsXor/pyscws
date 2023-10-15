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
btext = text.encode(encoding='utf-8')
stk = pyscws.ScwsTokenizer()
stk.charset = 'utf8'
stk.set_dict(r"E:\Users\23Xor\Desktop\dict.utf8.xdb", pyscws.SCWS_XDICT_XDB)
stk.set_rule(r"E:\Users\23Xor\Desktop\rules.utf8.ini")
stk.send_text(btext)
tokens = [btext[r.off:r.off+r.len].decode() for r in stk.get_result_all()]
print(tokens)
```
```python
['Hello', ',', '我', '名字', '叫', '李', '那曲', '是', '一个', '中国人', ',', '我', '有时', '买', 'Q币', '来', '玩', ',', '我', '还', '听说', '过', 'C#', '语言']
```

## 版本
PyPI对于每个版本只允许存在一个文件，即使删除release也无法重传。  
由于作者时常大意，他就是要重传，因此在版本最后加一个“重传号”。  
即x.y.z.a与x.y.z.b事实上都是x.y.z版本。  
