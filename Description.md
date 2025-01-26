# Mixo script

(.msc file ending)

Mixo is a simple scripting language. It is primarily designed for programming competitions such as leetcode or Advent Of Code. It includes a lot of syntactic sugar to make it easier to write code quickly.

## Features

Mixo focuses on making common programming operations more readable and concise:

- **IO Operations**: Built-in read/write operations that support both files and standard IO
- **Chained Operations**: Multiple operations can be combined in a readable way using blocks
- **Lambda Functions**: Easy-to-read lambda syntax using `(param) => {expression}`
- **Variable Management**: Clear variable creation and assignment using descriptive keywords

## Syntax

### IO Operations

Reading from files or stdin:
```msc
read
    "path/to/file.txt"  // or "io:stdin" for standard input
    split "delimiter"   // optional: split input by delimiter
    as variableName    // store result in variable
```

Writing to files or stdout:
```msc
write
    variable
    join "delimiter"  // optional: join elements with delimiter
    to "path/to/file.txt"  // or "io:stdout" for standard output
```

### Variable Assignment

Variables are created using descriptive declarations:
```msc
create
    type           // e.g., list, map, set
    as varName
```

### Operations and Mapping

Single operation on elements:
```msc
map
    sourceVar
    as element
    to targetVar
    op operation   // operation can be a function name or lambda
```

Multiple operations in one block:
```msc
map
    sourceVar
    as element
    to targetVar
    op (x) => {x * 2}   // first operation
    op abs              // second operation
    op toString         // third operation
```

### Lambda Functions

Lambda functions use a clear arrow syntax:
```msc
(param) => {expression}

// Examples:
(x) => {x * x}
(str) => {str.toLowerCase()}
```

### Comments

Single-line comments start with `//`:
```msc
// This is a comment
```

## Example

Here's a complete example that reads numbers from a file, processes them, and writes the results:

```msc
// Read input from file
read
    "./input.txt"
    split "\n"
    as lines

// Create a list for numbers
create
    list
    as nums

// Convert strings to integers
map
    lines
    as line
    to nums
    op toInt

// Square and get absolute values
map
    nums
    as num
    to nums
    op (num) => {num * num}
    op abs

// Write results to file
write
    nums
    join "\n"
    to "./output.txt"
```

### Alternative IO Sources

Mixo supports both file and standard IO:
- Files: Use file paths (`"./input.txt"`, `"./output.txt"`)
- Standard IO: Use special identifiers (`"io:stdin"`, `"io:stdout"`)
