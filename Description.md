# Mixo script

(.msc file ending)

Mixo is a simple scripting language heavily inspired by Python. It is primarily designed for programming competitions such as leetcode or Advent Of Code. It includes a lot of syntactic sugar to make it easier to write code quickly.


Mixo is transpiled to Python, so you can use any Python library in your Mixo code.  
Any valid python code is also valid Mixo code.  

In a Mixo script, the `main(...)` function is the entry point of the script and will be called when the script is run.


## Features

These are the features that Mixo has that Python does not have.

- **Range shorthand**: `x...y^z` is equivalent to `range(x, y, z)`. If x is not provided, it defaults to 0. If z is not provided, it defaults to 1. y is required.
- **Lambdas**: Instead of the `lambda` keyword, Mixo uses this notation for anonymous functions: `(args) => {body}`. For example, `(x) => {x + 1}` is equivalent to `lambda x: x + 1`.
- **Arrow operator**: `[1, 2, 3] -> abs -> (x) => {x + 1}` is equivalent to `map(lambda x: x + 1, map(abs, [1, 2, 3]))`.
- **Null-Coalescing and automatic Error handling**: See [Null-Coalescing and automatic Error handling](#null-coalescing-and-automatic-error-handling) for more information.


### Null-Coalescing and automatic Error handling

Mixo has a feature that allows you to handle errors and null values more easily:  
Adding a `?` after a function call will return `None` if the function call raises an error.  
Adding a `?? value` after a function call will return `value` if the function returns `None` or raises an error.  

Here is an example:

```msc

a = func_that_will_raise_error() ?
b = func_that_will_raise_error() ?? "default value"

print(a)
print(b)
```

In this example, `func_that_will_raise_error` will raise an error.  
Therefore, `a` will be `None` and `b` will be `"default value"`.  


## Syntax

Mixo has a syntax that is very similar to Python. Here are some of the differences:

- **No colons**: Mixo does not use colons to denote code blocks. Instead, it uses curly braces. For example, `if x > 0:` in Python would be `if x > 0 {` in Mixo.
- **No indentation**: Mixo does not use indentation to denote code blocks. Instead, it uses curly braces. For example, in Python, you would write:

```python
if x > 0:
    print("x is positive")
else:
    print("x is not positive")
```

In Mixo, you would write:

```msc
if x > 0 {
    print("x is positive")
} else {
    print("x is not positive")
}
```
