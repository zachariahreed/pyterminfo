`pyterminfo` is a parser for terminfo-style terminal descriptions. Roughly, it provides equivalent functionality of the `ncurses` functions `tigetflag`, `tigetnum`, `tigetstr`, and, `tparm`. The API presented is different though and hopefully more "pythonic". 

An example shows basic usage:

```python
import pyterminfo
  
# loads capabilities for $TERM
t = pyterminfo.terminfo()
    
t.os                  # a boolean capability
t.cols                # a numeric capability
t.sgr0                # a string capability
t.setaf(6)            # a parameterized-string capability
t.set_a_foreground(6) # long names work as well

```    

By default, string capabilities are `str`s (or functions returning a `str`). While not *strictly* correct, it can be convenient. Passing `binary=True` to `pyterminfo.terminfo` causes string capabilities to be `bytes` based.

Finally, a note about `pyterminfo`'s implementation. Typically, parameterized-string capabilities are implemented in a manner similiar to `printf` (parsing the format string on each invokation). Here, parameterized-string capabilities are implemented through generation of `python` bytecode. For example, from the capability:

    setab=\E[%?%p1%{8}%<%t4%p1%d%e%p1%{16}%<%t10%p1%{8}%-%d%e48;5;%p1%d%;m,
    
the following is generated (in `str` mode):

```
  1           0 LOAD_CONST               0 (<built-in method join of str object at 0x7ff4de3da848>)
              3 LOAD_CONST               1 ('\x1b[')
              6 LOAD_FAST                0 (a1)
              9 LOAD_CONST               2 (8)
             12 COMPARE_OP               0 (<)
             15 POP_JUMP_IF_FALSE       31
             18 LOAD_CONST               3 ('4')
             21 LOAD_CONST               4 ('%d')
             24 LOAD_FAST                0 (a1)
             27 BINARY_MODULO
             28 JUMP_FORWARD            39 (to 70)
        >>   31 LOAD_FAST                0 (a1)
             34 LOAD_CONST               5 (16)
             37 COMPARE_OP               0 (<)
             40 POP_JUMP_IF_FALSE       60
             43 LOAD_CONST               6 ('10')
             46 LOAD_CONST               4 ('%d')
             49 LOAD_FAST                0 (a1)
             52 LOAD_CONST               2 (8)
             55 BINARY_SUBTRACT
             56 BINARY_MODULO
             57 JUMP_FORWARD            10 (to 70)
        >>   60 LOAD_CONST               7 ('48;5;')
             63 LOAD_CONST               4 ('%d')
             66 LOAD_FAST                0 (a1)
             69 BINARY_MODULO
        >>   70 LOAD_CONST               8 ('m')
             73 BUILD_TUPLE              4
             76 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             79 RETURN_VALUE



```

The transformation from format string to bytecode happens in serveral stages which can be visualized by the curious. For the above, we can render:


| High Level | Low Level |
|------------|-----------|
| <img src="https://raw.githubusercontent.com/zachariahreed/pyterminfo/gh-pages/TERMINFO-set_a_foreground.png" width=375> | <img src="https://raw.githubusercontent.com/zachariahreed/pyterminfo/gh-pages/BYTECODE-set_a_foreground.png" width=375> |

