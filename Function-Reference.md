# MixoMax Scripting Language

(.msc)


Any function can raise

> TypeError

if the arguments are of the wrong type.



---

### int

    (int) (a)

> a: int | float | str

> Return: int

Converts a variable to an integer. If the variable is a float, it will be rounded down.

Raises:  

> ValueError: If the `a` is a string that cannot be converted to an integer.

---

### float

    (float) (a)  

> a: int | float | str

> Return: float  

Converts a variable to a float.

Raises:

> ValueError: If `a` is a string that cannot be converted to a float.

---

### str

    (str) (a)  

> a: Any  

> Return: str


Converts a variable to a string.

---

### bool

    (bool) (a)  

> a: Any

> Return: bool

Converts a variable to a boolean value:  

- `0`, `0.0`, `""`, `[]`, `{}` are converted to `False`
- Everything else is converted to `True`

---

### add

    (add) (a, b)
or

    (a) (add) (b)

> a: int | float
> 
> b: int | float

> Return: int | float

Adds two numbers together.

---

### sub

    (sub) (a, b)
or

    (a) (sub) (b)

> a: int | float
>
> b: int | float

> Return: int | float

Subtracts `b` from `a`.

---

### mul

    (mul) (a, b)
or

    (a) (mul) (b)

> a: int | float
>
> b: int | float

> Return: int | float

Multiplies two numbers together.

---

### div

    (div) (a, b)
or
    
    (a) (div) (b)

> a: int | float
>
> b: int | float

> Return: float

Divides `a` by `b`.

Raises:

> ZeroDivisionError: If `b` is `0`.

---

### pow

    (pow) (a, b)
or

    (a) (pow) (b)

> a: int | float
>
> b: int | float

> Return: int | float

Raises `a` to the power of `b`.

---

### mod

    (mod) (a, b)
or

    (a) (mod) (b)

> a: int | float
>
> b: int | float

> Return: int | float

Returns the remainder of `a` divided by `b`.

Raises:

> ZeroDivisionError: If `b` is `0`.

---

### abs

    (abs) (a)

> a: int | float

> Return: int | float

Returns the absolute value of `a`.

---

### max

    (max) (a)

> a: list[int | float]

> Return: int | float

Returns the largest number in the list.

Raises:

> ValueError: If `a` is an empty list.

---

### min

    (min) (a)

> a: list[int | float]

> Return: int | float

Returns the smallest number in the list.

Raises:

> ValueError: If `a` is an empty list.

---


### split

    (split) (a, b)
or

    (a) (split) (b)

> a: str
>
> b: str

> Return: list[str]


Splits `a` into a list of strings using `b` as the separator.

---

### join

    (join) (a, b)
or
    
    (a) (join) (b)

> a: list[str]
>
> b: str

> Return: str

Joins the strings in `a` using `b` as the separator.

---

### strcat
    
        (strcat) (a, b)
or
    
        (a) (strcat) (b)

> a: str
>
> b: str

> Return: str

Concatenates `a` and `b`.

---

### len

    (len) (a)

> a: str | list[Any] | dict

> Return: int

Returns the length of `a`.

---

### index

    (index) (a, b)
or
    
    (a) (index) (b)

> a: list[Any] | str
> 
> b: Any

> Return: int

Returns the index of the first occurrence of `b` in `a`.

Raises:

> ValueError: If `b` is not in `a`.

---

### append

    (append) (a, b)
or

    (a) (append) (b)


> a: list[Any]
>
> b: Any

> Return: list[Any]


Appends `b` to the end of `a`.

---


Sure! Below is the documentation for the rest of the functions in the MixoMax Scripting Language following the provided Markdown format:

---

### remove

    (remove) (a, b)
or

    (a) (remove) (b)

> a: list[Any]
>
> b: Any

> Return: list[Any]

Removes the first occurrence of `b` from `a`.

Raises:

> ValueError: If `b` is not in `a`.

---

### pop

    (pop) (a, b)
or

    (a) (pop) (b)

> a: list[Any]
>
> b: int

> Return: Any

Removes and returns the item at the index `b` of `a`.

Raises:

> IndexError: If `b` is out of range.

---

### sort

    (sort) (a)

> a: list[Any]

> Return: list

Returns a sorted list `a`.

---

### reverse

    (reverse) (a)

> a: list[Any]

> Return: list

Returns `a` in reverse order.

---

### insert

    (insert) (a, b, c)
or

    (a) (insert) (b, c)

> a: list[Any]
>
> b: int
>
> c: Any

> Return: list

Inserts `c` into `a` at index `b`.

---

### count

    (count) (a, b)
or

    (a) (count) (b)

> a: list[Any]
>
> b: Any

> Return: int

Returns the number of occurrences of `b` in `a`.

---

### extend

    (extend) (a, b)
or

    (a) (extend) (b)

> a: list[Any]
>
> b: list[Any]

> Return: list

Extends list `a` by appending elements from list `b`.

---

### print

    (print) (a)

> a: Any | list[Any]

> Return: None

Prints the value of `a`.

---

### type

    (type) (a)

> a: Any

> Return: type

Returns the type of `a`.

---

### eq

    (eq) (a, b)
or

    (a) (eq) (b)

> a: Any
>
> b: Any

> Return: bool

Returns `True` if `a` equals `b`; otherwise, `False`.

---

### neq

    (neq) (a, b)
or

    (a) (neq) (b)

> a: Any
> 
> b: Any

> Return: bool

Returns `True` if `a` does not equal `b`; otherwise, `False`.

---

### gt

    (gt) (a, b)
or

    (a) (gt) (b)

> a: int | float
> 
> b: int | float

> Return: bool

Returns `True` if `a` is greater than `b`; otherwise, `False`.

---

### lt

    (lt) (a, b)
or

    (a) (lt) (b)

> a: int | float
>
> b: int | float

> Return: bool

Returns `True` if `a` is less than `b`; otherwise, `False`.

---

### gte

    (gte) (a, b)
or

    (a) (gte) (b)

> a: int | float
>
> b: int | float

> Return: bool

Returns `True` if `a` is greater than or equal to `b`; otherwise, `False`.

---

### lte

    (lte) (a, b)
or

    (a) (lte) (b)

> a: int | float
>
> b: int | float

> Return: bool

Returns `True` if `a` is less than or equal to `b`; otherwise, `False`.

---

### and

    (and) (a, b)
or

    (a) (and) (b)

> a: bool
>
> b: bool

> Return: bool

Logical AND operation between `a` and `b`.

---

### or

    (or) (a, b)
or

    (a) (or) (b)

> a: bool
>
> b: bool

> Return: bool

Logical OR operation between `a` and `b`.

---

### not

    (not) (a)

> a: bool

> Return: bool

Logical NOT operation on `a`.

---

### in

    (in) (a, b)
or

    (a) (in) (b)

> a: Any
>
> b: list[Any]

> Return: bool

Returns `True` if `a` is in `b`; otherwise, `False`.

---

### chr
    
    (chr) (a)

> a: int

> Return: str

Returns the character represented by the ASCII value `a`.

Raises:

> ValueError: If `a` is not in the range 0-255.

---

### ord

    (ord) (a)

> a: str

> Return: int

Returns the ASCII value of the character `a`.

Raises:

> ValueError: If `a` is not a single character.

---


### lower

    (lower) (a)

> a: str

> Return: str

Converts `a` to lowercase.

---

### upper

    (upper) (a)

> a: str

> Return: str

Converts `a` to uppercase.

---