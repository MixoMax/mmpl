# MixoMax Scripting Language

Read about the built-in Functions at the [Function Reference](Function-Reference.md)

## Key ideas:


### 1. Types

Type checking is enforced at each function call. The following types are supported:

- `bool`
- `int`
- `float`
- `str`
- `list`
- `dict`

As seen later on, a Variable can change its type.



### 2. Variables

Variables are declared by assigning a value to them. The type of the variable is inferred from the value.

### 3. Functions

A function can be called in two ways:

Assignment function call:
`(a) (function) (b, c, ...)`
or  
`(a) (?function) (b, c, ...)`

Direct function call:
`(function) (a, b, c, ...)`


The difference between these three is that the first automatically store the return value in `a` and the other two do not.  The difference between the second and the third is just stylistic preference.  



Examples:

Assignment functions:

1) `a (int)` 
```
a = "4"
a (int)
(print) ((type) (a), a)
```

would print `int 4`



2) `(a) (add) (b)` 
```
a = 4
b = 2
(a) (add) (b)
(print) (a)
```

would print `6`


3) `(a) (split) (b)`
```
a = "hello world"
b = " "
(a) (split) (b)
(print) ((type) (a), a)
```

would print `list ["hello", "world"]`


4) `(a) (join) (b)`
```
a = ['hello', 'world']
b = " "

(a) (join) (b)
(print) (a)
```

would print `hello world`



Way II:

1) `(len) a`
```
a = "hello"
l = (len) (a)
(print) (l)
```

would print `5`


2) `(add) (4, 2)`
```
a = (add) (4, 2)
(print) (a)
```

would print `6`


3) `(split) ("hello world", " ")`
```
a = (split) ("hello world", " ")

(print) (a)
```
would print `["hello", "world"]`


4) `(join) (["hello", "world"], " ")`
```
a = (join) (("hello", "world"), " ")

(print) (a)
```

would print `hello world`


### 4. contitions

Condition operators are:

- `a (eq) b` - a: Any, b: Any
- `a (neq) b` - a: Any, b: Any
- `a (gt) b` - a: int | float, b: int | float
- `a (lt) b` - a: int | float, b: int | float
- `a (gte) b` - a: int | float, b: int | float
- `a (lte) b` - a: int | float, b: int | float
- `a (and) b` - a: bool, b: bool
- `a (or) b` - a: bool, b: bool
- `a (not) b` - a: bool, b: bool
- `a (in) b` - a: Any, b: list | dict


### 5. Loops

- `for` - `for [var] in [list]:`
- `while` - `while [condition]:`
- `break`
- `continue`

Instead of pythons `range` function, msc uses `A...B^C` where A is the starting number, B is the ending number and C is the step. If C is not provided, it defaults to 1. If A is not provided, it defaults to 0.



### 6. Examples


Prime checker:

```
n = 100
for i in 2...n:
    is_prime = True
    for j in 2...i:
        if (0)(eq)((mod)(i, j)):
            is_prime = False
            break
    if is_prime:
        (print) (i)
```

would print all prime numbers from 2 to 100.


Using only direct function calls:

Fibonacci:

```
n = 10
a = 0
b = 1

for i in 0...n:
    (print) (a)
    c = (add) (a, b)
    a = b
    b = c
```


Using assignment function calls

Sum of first 10 numbers:

```
s = 0
for i in 0...10:
    s (add) (i)
(print) (s)
```


