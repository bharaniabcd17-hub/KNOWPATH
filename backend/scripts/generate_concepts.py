"""Generator script to produce all 79 concepts for PROJECT-EVOLVE Knowledge Genome."""
import os

# Concept metadata definition
CONCEPTS_DEF = [
    # Difficulty 1: Foundations
    {
        "slug": "variables-basics",
        "title": "Variables and Assignment",
        "difficulty": 1,
        "prerequisites": [],
        "description": "How Python associates names with values and handles dynamic typing.",
        "content_md": """## Variables and Assignment

In Python, a variable is a symbolic name that acts as a reference or label to an object stored in memory. Unlike statically typed languages like C or Java, Python does not require explicit type declarations. You create a variable simply by assigning a value to it using the assignment operator (`=`).

```python
age = 21
name = "Alex"
is_student = True
```

When you assign `x = 5`, Python creates an integer object `5` in memory and points the name `x` to it. If you subsequently assign `x = 'hello'`, Python changes the reference to a new string object `'hello'`. Variable names must begin with a letter or an underscore and can contain letters, numbers, and underscores, but cannot match Python keywords like `def`, `class`, or `if`.
"""
    },
    {
        "slug": "data-types-overview",
        "title": "Python Data Types Overview",
        "difficulty": 1,
        "prerequisites": ["variables-basics"],
        "description": "Overview of primitive and container data types in Python.",
        "content_md": """## Data Types Overview

Every value in Python has an associated data type. Python's built-in types can be categorized into scalar primitives (numeric types, booleans, strings) and collection types (lists, tuples, dictionaries, sets).

You can inspect the type of any object using the built-in `type()` function:

```python
x = 42
print(type(x))  # <class 'int'>
```

Python is strongly and dynamically typed: values are typed at runtime, and the language prevents nonsensical implicit conversions (such as adding a string directly to an integer without explicit casting).
"""
    },
    {
        "slug": "integers",
        "title": "Integer Type",
        "difficulty": 1,
        "prerequisites": ["data-types-overview"],
        "description": "Whole numbers with arbitrary precision in Python 3.",
        "content_md": """## Integer Type

The `int` type in Python represents whole numbers, both positive and negative, as well as zero. In Python 3, integers have arbitrary precision—they can grow as large as your machine's memory allows, avoiding integer overflow bugs common in other languages.

```python
small = 42
huge = 10 ** 50  # Python handles arbitrarily large ints seamlessly
```

Integers support standard base notations including binary (`0b1010`), octal (`0o755`), and hexadecimal (`0xFF`). You can convert other types or strings into integers using the `int()` constructor.
"""
    },
    {
        "slug": "floats",
        "title": "Float Type",
        "difficulty": 1,
        "prerequisites": ["data-types-overview"],
        "description": "Double-precision IEEE 754 floating-point numbers.",
        "content_md": """## Float Type

Floating-point numbers (`float`) represent real numbers with fractional components. In CPython, floats are implemented using double-precision (64-bit) IEEE 754 representations.

```python
price = 19.99
scientific = 1.5e-3  # 0.0015
```

Because binary floating-point representations cannot represent all decimal fractions exactly, expressions such as `0.1 + 0.2` equal `0.30000000000000004` rather than exactly `0.3`. For financial calculations where exact decimal arithmetic is mandatory, Python provides the `decimal` module.
"""
    },
    {
        "slug": "strings-basics",
        "title": "String Basics",
        "difficulty": 1,
        "prerequisites": ["data-types-overview"],
        "description": "Creation, quotation, and basic operations on text strings.",
        "content_md": """## String Basics

Strings (`str`) represent sequences of Unicode characters. They can be enclosed in single quotes (`'...'`), double quotes (`"..."`), or triple quotes (`'''...'''` or `\"\"\"...\"\"\"`) for multi-line strings.

```python
single = 'Hello'
double = "World"
multiline = '''Line 1
Line 2'''
```

Strings are immutable in Python: once created, individual characters within a string cannot be modified or replaced in place. New strings must be created through operations like concatenation or slicing.
"""
    },
    {
        "slug": "booleans",
        "title": "Boolean Type",
        "difficulty": 1,
        "prerequisites": ["data-types-overview"],
        "description": "True and False values, and truth value testing in Python.",
        "content_md": """## Boolean Type

The `bool` type represents truth values: `True` and `False`. In Python, `bool` is a subclass of `int`, meaning `True == 1` and `False == 0`.

```python
is_active = True
has_permission = False
```

Every Python object has an innate truth value. Values considered *falsy* include `None`, `False`, numeric zero (`0`, `0.0`), and empty collections (`""`, `[]`, `{}`, `set()`, `()`). All other values evaluate to *truthy* when tested in conditional expressions.
"""
    },
    {
        "slug": "none-type",
        "title": "NoneType and None Value",
        "difficulty": 1,
        "prerequisites": ["data-types-overview"],
        "description": "The absence of a value and the None singleton.",
        "content_md": """## NoneType and None

`None` is a special constant in Python that represents the absence of a value or a null state. It is the sole instance of `NoneType`.

```python
result = None
if result is None:
    print("No result found")
```

Functions that do not explicitly return a value implicitly return `None`. Always check for `None` using identity comparison (`x is None` or `x is not None`), rather than equality (`x == None`), because custom classes can overload `==` but identity is invariant.
"""
    },
    {
        "slug": "print-function",
        "title": "The print() Function",
        "difficulty": 1,
        "prerequisites": ["variables-basics"],
        "description": "Standard output formatting with print(), sep, and end.",
        "content_md": """## The print() Function

The `print()` built-in function writes text representations of objects to standard output (`sys.stdout`), separated by spaces and terminated by a newline by default.

```python
print("Hello", "World", sep="-", end="!\\n")
# Output: Hello-World!
```

The `sep` parameter controls the separator between multiple arguments, while `end` specifies what character is printed at the end of the line. The `file` parameter allows directing output to files or stream objects.
"""
    },
    {
        "slug": "input-function",
        "title": "The input() Function",
        "difficulty": 1,
        "prerequisites": ["variables-basics", "strings-basics"],
        "description": "Reading user input from standard input as strings.",
        "content_md": """## The input() Function

The `input([prompt])` function reads a line from standard input, converts it to a string (stripping the trailing newline), and returns it.

```python
name = input("Enter your name: ")
age = int(input("Enter your age: "))  # Must explicitly convert string to int
```

Crucially, `input()` always returns a string. Attempting numeric operations on the return value without type conversion (like `int()` or `float()`) will raise a `TypeError` or perform unexpected string concatenation.
"""
    },
    {
        "slug": "comments",
        "title": "Comments and Code Style",
        "difficulty": 1,
        "prerequisites": ["variables-basics"],
        "description": "Inline comments, block comments, docstrings, and PEP 8 guidelines.",
        "content_md": """## Comments and Code Style

Comments allow developers to explain why code exists and clarify complex logic. Python uses the hash character (`#`) for single-line comments.

```python
# Calculate the final discounted price
final_price = base_price * (1 - discount_rate)
```

Docstrings (`\"\"\"...\"\"\"`) serve as formal documentation for modules, classes, and functions, accessible via `help()` and the `__doc__` attribute. Python follows the PEP 8 style guide, recommending 4 spaces per indentation level and snake_case for variable and function names.
"""
    },

    # Difficulty 2: Operators & Flow Control
    {
        "slug": "arithmetic-operators",
        "title": "Arithmetic Operators",
        "difficulty": 2,
        "prerequisites": ["integers", "floats"],
        "description": "Addition, subtraction, true division, floor division, modulo, and exponentiation.",
        "content_md": """## Arithmetic Operators

Python supports the standard arithmetic operators: `+` (addition), `-` (subtraction), `*` (multiplication), `/` (true division), `//` (floor division), `%` (modulo / remainder), and `**` (exponentiation).

```python
print(7 / 2)   # 3.5 (true division always returns float)
print(7 // 2)  # 3   (floor division discards fractional part)
print(7 % 2)   # 1   (remainder)
print(2 ** 3)  # 8   (exponentiation)
```

Notice that in Python 3, `/` always yields a `float`, even when dividing two integers evenly (e.g. `4 / 2 == 2.0`). Floor division rounds toward negative infinity: `-7 // 2` evaluates to `-4`.
"""
    },
    {
        "slug": "comparison-operators",
        "title": "Comparison Operators",
        "difficulty": 2,
        "prerequisites": ["integers", "booleans"],
        "description": "Equality, inequality, ordering, and chained comparisons.",
        "content_md": """## Comparison Operators

Comparison operators evaluate expressions and return a boolean (`True` or `False`). They include `==` (equal to), `!=` (not equal to), `<` (less than), `>` (greater than), `<=` (less than or equal to), and `>=` (greater than or equal to).

```python
print(5 > 3)    # True
print(10 == 10) # True
print(5 != 5)   # False
```

Python uniquely supports chained comparisons: `1 < x < 10` is equivalent to `(1 < x) and (x < 10)`, with `x` evaluated only once. Remember that `==` tests value equality, whereas `is` tests object identity.
"""
    },
    {
        "slug": "logical-operators",
        "title": "Logical Operators",
        "difficulty": 2,
        "prerequisites": ["booleans", "comparison-operators"],
        "description": "and, or, not operators and short-circuit evaluation semantics.",
        "content_md": """## Logical Operators

Python provides three boolean operators: `and`, `or`, and `not`.

```python
print(True and False) # False
print(True or False)  # True
print(not True)       # False
```

Python logical operators employ short-circuit evaluation: evaluation stops as soon as the outcome is determined. Moreover, `and` and `or` return the actual operand value that determined the result, not strictly a boolean: `"" or "default"` evaluates to `"default"`, while `"first" and "second"` evaluates to `"second"`.
"""
    },
    {
        "slug": "string-formatting",
        "title": "String Formatting",
        "difficulty": 2,
        "prerequisites": ["strings-basics", "variables-basics"],
        "description": "Formatted string literals (f-strings), str.format(), and printf-style formatting.",
        "content_md": """## String Formatting

Python offers multiple methods for interpolating variables into strings, with formatted string literals (f-strings, introduced in Python 3.6) being the modern standard.

```python
name = "Maya"
score = 98.456
print(f"Candidate {name} scored {score:.1f}%")  # Candidate Maya scored 98.5%
```

F-strings are prefixed with `f` and evaluate expressions inside curly braces `{}` at runtime. They support format specifiers such as alignment (`<`, `>`, `^`), decimal precision (`.2f`), and comma separators (`,`). Older methods include `str.format()` and `%` formatting.
"""
    },
    {
        "slug": "string-methods",
        "title": "String Methods",
        "difficulty": 2,
        "prerequisites": ["strings-basics"],
        "description": "Essential built-in methods: upper, lower, strip, split, join, replace.",
        "content_md": """## String Methods

Python strings provide a rich library of built-in transformation and search methods. Because strings are immutable, every string method returns a new string rather than modifying the original.

```python
text = "  Python,Data,Analysis  "
clean = text.strip()                     # "Python,Data,Analysis"
tokens = clean.split(",")                # ['Python', 'Data', 'Analysis']
rejoined = " -> ".join(tokens)           # "Python -> Data -> Analysis"
upper_text = rejoined.upper()            # "PYTHON -> DATA -> ANALYSIS"
```

Common methods include `strip()` for removing whitespace, `split(sep)` for tokenizing into a list, `''.join(iterable)` for concatenating items, and `replace(old, new)`.
"""
    },
    {
        "slug": "string-indexing",
        "title": "String Indexing and Slicing",
        "difficulty": 2,
        "prerequisites": ["strings-basics"],
        "description": "Zero-based indexing, negative indices, and slice syntax [start:stop:step].",
        "content_md": """## String Indexing and Slicing

Strings are ordered sequences of characters. Individual characters can be accessed using zero-based indexing (`text[0]`), while negative indices count backward from the end (`text[-1]`).

```python
s = "Python"
print(s[0])     # 'P'
print(s[-1])    # 'n'
print(s[1:4])   # 'yth' (stop index is exclusive)
print(s[::-1])  # 'nohtyP' (reverse string using negative step)
```

The slice syntax `s[start:stop:step]` extracts a substring from `start` up to (but excluding) `stop` in increments of `step`. Omitting `start` defaults to `0`, omitting `stop` defaults to the string length, and omitting `step` defaults to `1`.
"""
    },
    {
        "slug": "string-operations",
        "title": "String Operations",
        "difficulty": 2,
        "prerequisites": ["strings-basics", "string-methods"],
        "description": "Concatenation, repetition, membership testing with 'in', and length.",
        "content_md": """## String Operations

In addition to dedicated methods, Python provides intuitive operator syntax for sequence operations on strings.

```python
greeting = "Hello" + " " + "World"  # Concatenation
divider = "-" * 20                  # Repetition: '--------------------'
has_py = "py" in "python"           # Membership: True
length = len(greeting)              # Length: 11
```

The `+` operator concatenates strings, `*` repeats them, `in` checks for substring presence in $O(N)$ time, and `len()` returns character count in $O(1)$ time.
"""
    },
    {
        "slug": "string-immutability",
        "title": "String Immutability",
        "difficulty": 2,
        "prerequisites": ["strings-basics"],
        "description": "Memory safety, hashability, and why string mutation raises TypeError.",
        "content_md": """## String Immutability

In Python, strings are immutable objects. Once a string object is allocated in memory, its characters cannot be altered, appended, or deleted in place.

```python
s = "hello"
# s[0] = 'H'  # Raises TypeError: 'str' object does not support item assignment
s = "H" + s[1:]  # Creates a brand new string and rebinds variable 's'
```

Immutability ensures thread safety and guarantees that string hash values remain constant throughout an application's lifecycle, allowing strings to serve safely as dictionary keys and set elements.
"""
    },
    {
        "slug": "type-conversion",
        "title": "Type Conversion and Casting",
        "difficulty": 2,
        "prerequisites": ["integers", "floats", "strings-basics"],
        "description": "Explicit type casting using int(), float(), str(), and bool().",
        "content_md": """## Type Conversion and Casting

Type casting converts a value from one data type to another. Python does not implicitly convert strings to numbers or vice-versa, making explicit conversion mandatory.

```python
num_str = "45"
num = int(num_str)       # String to integer: 45
price_str = "19.95"
price = float(price_str) # String to float: 19.95
code = str(100)          # Number to string: "100"
```

If a string cannot be parsed into the requested type (such as `int("abc")`), Python raises a `ValueError`. Explicit conversion ensures predictable program behavior and prevents silent data coercion bugs.
"""
    },
    {
        "slug": "if-statements",
        "title": "If Statements",
        "difficulty": 2,
        "prerequisites": ["booleans", "comparison-operators"],
        "description": "Conditional branching and indentation-based block structuring.",
        "content_md": """## If Statements

The `if` statement allows programs to branch execution based on boolean conditions. Python relies on consistent indentation (typically 4 spaces) rather than curly braces or keywords to define code blocks.

```python
score = 85
if score >= 60:
    print("Passing grade")
```

If the condition evaluates to `True` (or a truthy value), the indented body is executed. If it evaluates to `False`, the block is bypassed entirely.
"""
    },
    {
        "slug": "elif-else",
        "title": "elif and else Clauses",
        "difficulty": 2,
        "prerequisites": ["if-statements"],
        "description": "Chained multi-way decision branches and default fallback handling.",
        "content_md": """## elif and else Clauses

To handle multiple mutually exclusive conditions, Python pairs `if` with one or more `elif` (else if) clauses and an optional trailing `else` fallback.

```python
score = 75
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

Conditions are tested top to bottom. The first condition that evaluates to `True` executes its block, after which execution leaves the entire chain. If no condition matches, the `else` block executes.
"""
    },
    {
        "slug": "while-loops",
        "title": "While Loops",
        "difficulty": 2,
        "prerequisites": ["if-statements"],
        "description": "Conditional iteration, termination conditions, and infinite loop prevention.",
        "content_md": """## While Loops

A `while` loop repeatedly executes a block of code as long as a specified condition remains `True`.

```python
count = 0
while count < 3:
    print(f"Count is {count}")
    count += 1
```

Care must be taken to ensure that the loop condition eventually becomes `False`, otherwise an infinite loop occurs. The optional `else` block on a `while` loop executes once the condition becomes false, provided the loop was not terminated prematurely by a `break`.
"""
    },
    {
        "slug": "range-function",
        "title": "The range() Function",
        "difficulty": 2,
        "prerequisites": ["integers"],
        "description": "Generating arithmetic progressions with range(start, stop, step).",
        "content_md": """## The range() Function

The `range()` built-in type generates an immutable arithmetic sequence of integers on demand without loading all elements into memory simultaneously.

```python
for i in range(5):          # 0, 1, 2, 3, 4 (stop is exclusive)
    pass

for i in range(2, 10, 2):   # 2, 4, 6, 8 (start, stop, step)
    pass
```

Because `range` produces items lazily as an iterator, `range(1000000)` consumes negligible memory ($O(1)$ space), making it ideal for large loop iterations.
"""
    },
    {
        "slug": "for-loops",
        "title": "For Loops",
        "difficulty": 2,
        "prerequisites": ["if-statements", "range-function"],
        "description": "Iterating over sequences, collections, and generators.",
        "content_md": """## For Loops

Python's `for` loop is a *for-each* loop that iterates over the elements of any iterable object (lists, strings, tuples, dictionaries, generators).

```python
languages = ["Python", "Rust", "Go"]
for lang in languages:
    print(f"Studying {lang}")
```

Under the hood, the `for` statement calls `iter()` on the target object to obtain an iterator, then repeatedly calls `next()` until `StopIteration` is raised, providing clean sequence traversal without manual index tracking.
"""
    },
    {
        "slug": "break-continue",
        "title": "Break and Continue",
        "difficulty": 2,
        "prerequisites": ["for-loops", "while-loops"],
        "description": "Controlling loop iteration flow with break and continue statements.",
        "content_md": """## Break and Continue

The `break` statement immediately terminates the innermost enclosing loop, skipping any remaining iterations and bypassing any loop `else` clause.

```python
for n in range(10):
    if n == 5:
        break       # Exits loop when n hits 5
    if n % 2 == 0:
        continue    # Skips even numbers, proceeding to next iteration
    print(n)
```

The `continue` statement skips the rest of the current iteration's code block and jumps directly to evaluating the condition for the next iteration.
"""
    },
    {
        "slug": "nested-loops",
        "title": "Nested Loops",
        "difficulty": 2,
        "prerequisites": ["for-loops"],
        "description": "Multi-dimensional iteration, matrix traversal, and algorithmic complexity.",
        "content_md": """## Nested Loops

A nested loop is a loop located inside the body of another loop. The inner loop executes all its iterations for each single iteration of the outer loop.

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
for row in matrix:
    for val in row:
        print(val, end=" ")
```

Nested loops are common when traversing multi-dimensional data structures or generating combinations. However, nesting loops increases time complexity (e.g., two nested loops over $N$ items yield $O(N^2)$ runtime).
"""
    },

    # Difficulty 2-3: Data Structures
    {
        "slug": "lists-basics",
        "title": "Lists - Creation and Access",
        "difficulty": 2,
        "prerequisites": ["variables-basics"],
        "description": "Ordered, mutable sequences with indexing, length, and mutability.",
        "content_md": """## Lists Basics

A list (`list`) is an ordered, mutable sequence of arbitrary objects. Lists are created using square brackets `[]` with comma-separated values.

```python
items = ["apple", 42, 3.14, True]
print(items[0])     # 'apple'
items[1] = 99       # Mutation in place
print(len(items))   # 4
```

Unlike arrays in C or Java, Python lists can hold heterogeneous types and dynamically resize as elements are appended or removed.
"""
    },
    {
        "slug": "list-methods",
        "title": "List Methods",
        "difficulty": 2,
        "prerequisites": ["lists-basics"],
        "description": "Mutating lists via append, pop, insert, remove, extend, and sort.",
        "content_md": """## List Methods

Python lists offer dedicated methods for modifying content in place:

```python
nums = [1, 2, 3]
nums.append(4)       # [1, 2, 3, 4] - O(1) amortized
nums.insert(0, 0)    # [0, 1, 2, 3, 4] - O(N)
popped = nums.pop()  # Removes and returns 4 - O(1)
nums.remove(2)       # Removes first occurrence of value 2
nums.sort()          # In-place Timsort - O(N log N)
```

Be aware that in-place methods like `sort()` and `reverse()` modify the existing list and return `None`, rather than returning a new list.
"""
    },
    {
        "slug": "list-slicing",
        "title": "List Slicing",
        "difficulty": 2,
        "prerequisites": ["lists-basics", "string-indexing"],
        "description": "Extracting sublists, copying, and slice assignment.",
        "content_md": """## List Slicing

List slicing shares the sequence syntax `list[start:stop:step]` to extract sublists into shallow copies.

```python
nums = [10, 20, 30, 40, 50]
sub = nums[1:4]      # [20, 30, 40]
shallow_copy = nums[:]
```

Python also supports slice assignment to replace or delete contiguous sub-segments in place: `nums[1:3] = [99, 100]` replaces the elements at indices 1 and 2.
"""
    },
    {
        "slug": "list-comprehensions",
        "title": "List Comprehensions",
        "difficulty": 3,
        "prerequisites": ["lists-basics", "for-loops"],
        "description": "Concise, declarative syntax for generating transformed and filtered lists.",
        "content_md": """## List Comprehensions

List comprehensions provide a concise syntax for transforming and filtering iterable data into a new list.

```python
numbers = [1, 2, 3, 4, 5, 6]
evens_squared = [x ** 2 for x in numbers if x % 2 == 0]
# Result: [4, 16, 36]
```

The general pattern is `[expression for item in iterable if condition]`. List comprehensions are generally faster than equivalent manual `for` loops with `append()` because the iteration is implemented at C-speed in bytecode.
"""
    },
    {
        "slug": "tuples",
        "title": "Tuples",
        "difficulty": 2,
        "prerequisites": ["lists-basics"],
        "description": "Ordered, immutable sequences and tuple packing / unpacking.",
        "content_md": """## Tuples

A tuple (`tuple`) is an ordered, immutable collection of elements enclosed in parentheses `()`.

```python
point = (10, 20)
# point[0] = 15  # TypeError: 'tuple' object does not support item assignment
x, y = point      # Tuple unpacking
```

Tuples are lighter weight in memory than lists and can serve as dictionary keys (provided all their contained elements are also hashable). They are commonly used to return multiple values from functions.
"""
    },
    {
        "slug": "sets",
        "title": "Sets",
        "difficulty": 3,
        "prerequisites": ["lists-basics"],
        "description": "Unordered collections of unique elements and mathematical set operations.",
        "content_md": """## Sets

A set (`set`) is an unordered collection of unique, hashable objects. Sets are defined using curly braces `{1, 2, 3}` or the `set()` constructor.

```python
s1 = {1, 2, 3, 3}    # {1, 2, 3} (duplicates discarded)
s2 = {3, 4, 5}
print(s1 | s2)       # Union: {1, 2, 3, 4, 5}
print(s1 & s2)       # Intersection: {3}
print(s1 - s2)       # Difference: {1, 2}
```

Sets are backed by hash tables, providing average $O(1)$ time complexity for membership testing (`x in s`), insertion, and deletion.
"""
    },
    {
        "slug": "dicts-basics",
        "title": "Dictionaries - Creation and Access",
        "difficulty": 2,
        "prerequisites": ["lists-basics"],
        "description": "Key-value hash maps, key constraints, and safe access with get().",
        "content_md": """## Dictionaries Basics

A dictionary (`dict`) is a mutable mapping of unique, hashable keys to arbitrary values. Dictionaries are created with curly braces `{}` containing `key: value` pairs.

```python
user = {"name": "Sara", "role": "engineer", "level": 3}
print(user["name"])               # 'Sara'
print(user.get("age", 25))        # 25 (default fallback, avoids KeyError)
```

Keys must be immutable and hashable (strings, numbers, tuples). Since Python 3.7, dictionaries preserve insertion order. Accessing a missing key via `[]` raises a `KeyError`, whereas `.get()` safely returns `None` or a supplied default.
"""
    },
    {
        "slug": "dict-methods",
        "title": "Dictionary Methods",
        "difficulty": 2,
        "prerequisites": ["dicts-basics"],
        "description": "keys(), values(), items(), update(), and pop() methods.",
        "content_md": """## Dictionary Methods

Python dictionaries provide essential methods for inspection and modification:

```python
d = {"a": 1, "b": 2}
for k, v in d.items():
    print(f"{k} => {v}")

d.update({"c": 3, "a": 10})  # Merges updates
removed = d.pop("b")         # Removes key 'b' and returns its value
```

The methods `.keys()`, `.values()`, and `.items()` return dynamic dictionary view objects that reflect modifications made to the underlying dictionary in real time.
"""
    },
    {
        "slug": "dict-comprehensions",
        "title": "Dictionary Comprehension",
        "difficulty": 3,
        "prerequisites": ["dicts-basics", "for-loops"],
        "description": "Creating and transforming mappings with {k: v for ...}.",
        "content_md": """## Dictionary Comprehension

Dictionary comprehensions construct new dictionaries by iterating over an iterable and evaluating key-value expressions.

```python
names = ["alice", "bob", "charlie"]
length_map = {name: len(name) for name in names}
# {'alice': 5, 'bob': 3, 'charlie': 7}

# Inverting an invertible dictionary:
inverted = {v: k for k, v in length_map.items()}
```

Conditions can be included to filter pairs: `{k: v for k, v in data.items() if v > 0}`.
"""
    },
    {
        "slug": "nested-data",
        "title": "Nested Data Structures",
        "difficulty": 3,
        "prerequisites": ["lists-basics", "dicts-basics"],
        "description": "Lists of dicts, nested dicts, deep vs shallow copies.",
        "content_md": """## Nested Data Structures

Real-world data such as JSON payloads typically consists of nested lists and dictionaries.

```python
users = [
    {"id": 1, "profile": {"name": "Dana", "skills": ["python", "sql"]}},
    {"id": 2, "profile": {"name": "Eli", "skills": ["rust"]}}
]
first_skill = users[0]["profile"]["skills"][0]  # 'python'
```

When copying nested structures, shallow copies (like `list.copy()` or `dict.copy()`) only duplicate top-level references. Modifying deeply nested mutable objects affects both copies. To create a completely independent copy, use `copy.deepcopy()`.
"""
    },

    # Difficulty 3: Functions
    {
        "slug": "functions-basics",
        "title": "Defining and Calling Functions",
        "difficulty": 3,
        "prerequisites": ["variables-basics"],
        "description": "The def statement, calling syntax, code reuse, and modularity.",
        "content_md": """## Defining and Calling Functions

Functions are reusable blocks of code defined using the `def` keyword, followed by the function name, a parameter list in parentheses, and a colon.

```python
def greet(name):
    \"\"\"Return a personalized greeting string.\"\"\"
    return f"Hello, {name}!"

msg = greet("Elena")
```

Functions encapsulate logic, prevent repetitive code, and establish clear programmatic boundaries. If a function reaches the end of its body without executing a `return` statement, it returns `None`.
"""
    },
    {
        "slug": "function-parameters",
        "title": "Function Parameters and Arguments",
        "difficulty": 3,
        "prerequisites": ["functions-basics"],
        "description": "Positional vs keyword arguments, formal parameters vs actual arguments.",
        "content_md": """## Function Parameters and Arguments

Parameters are the variables defined in a function's signature, while arguments are the actual values passed during invocation.

```python
def calculate_area(width, height):
    return width * height

# Positional arguments:
print(calculate_area(5, 10))
# Keyword arguments:
print(calculate_area(height=10, width=5))
```

Positional arguments are matched based on order, whereas keyword arguments specify the parameter name directly, allowing flexible ordering and clearer call sites.
"""
    },
    {
        "slug": "default-arguments",
        "title": "Default Arguments",
        "difficulty": 3,
        "prerequisites": ["function-parameters"],
        "description": "Default parameter values and the classic mutable default argument trap.",
        "content_md": """## Default Arguments

Parameters can define default values that are used if the caller omits that argument.

```python
def connect(host, port=5432, timeout=30):
    return f"Connecting to {host}:{port} (timeout={timeout}s)"
```

**Critical trap:** Default parameter expressions are evaluated once when the function is defined, not on each invocation. Never use a mutable object (like a list or dict) as a default value:

```python
# Dangerous:
def append_to(item, target=[]):
    target.append(item)
    return target

# Safe idiom:
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```
"""
    },
    {
        "slug": "keyword-arguments",
        "title": "Keyword Arguments",
        "difficulty": 3,
        "prerequisites": ["function-parameters"],
        "description": "Keyword arguments and keyword-only parameter constraints.",
        "content_md": """## Keyword Arguments

Keyword arguments clarify function call sites by explicitly naming each argument.

```python
def send_email(recipient, subject, body, *, urgent=False):
    pass

# The '*' forces all subsequent arguments to be keyword-only:
send_email("user@test.com", "Alert", "Disk full", urgent=True)
```

Enforcing keyword-only arguments using `*` prevents errors when calling functions with many boolean flags or configuration settings.
"""
    },
    {
        "slug": "return-values",
        "title": "Return Values",
        "difficulty": 3,
        "prerequisites": ["functions-basics"],
        "description": "The return statement, returning multiple values as tuples, early exit.",
        "content_md": """## Return Values

The `return` statement terminates function execution and sends a result back to the caller.

```python
def min_max(numbers):
    return min(numbers), max(numbers)  # Returns a tuple (min, max)

low, high = min_max([4, 1, 9, 2])
```

Returning multiple comma-separated values automatically packs them into a single tuple, which can be cleanly unpacked at the destination.
"""
    },
    {
        "slug": "variable-scope",
        "title": "Variable Scope (LEGB)",
        "difficulty": 3,
        "prerequisites": ["functions-basics"],
        "description": "Local, Enclosing, Global, and Built-in name resolution rules.",
        "content_md": """## Variable Scope and the LEGB Rule

Python resolves variable names using the **LEGB** rule, checking namespaces in this exact order:
1. **L**ocal: Inside the current function.
2. **E**nclosing: In any enclosing function closures.
3. **G**lobal: At the top level of the current module.
4. **B**uilt-in: In the built-in library (e.g. `len`, `range`).

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        # x refers to "enclosing"
        print(x)
    inner()
```

To rebind a global variable from inside a function, use the `global` keyword; to rebind an enclosing variable in a closure, use `nonlocal`.
"""
    },
    {
        "slug": "lambda-functions",
        "title": "Lambda Functions",
        "difficulty": 3,
        "prerequisites": ["functions-basics"],
        "description": "Anonymous single-expression functions for sorting and mapping.",
        "content_md": """## Lambda Functions

A `lambda` function is a small, anonymous function defined with the `lambda` keyword. It can take any number of parameters but contains only a single expression whose evaluated result is returned.

```python
square = lambda x: x ** 2
print(square(5))  # 25

pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
pairs.sort(key=lambda item: item[0])
```

Lambdas are commonly used as throwaway key functions for `sorted()`, `min()`, `max()`, and functional utilities.
"""
    },
    {
        "slug": "args-kwargs",
        "title": "*args and **kwargs",
        "difficulty": 3,
        "prerequisites": ["keyword-arguments", "default-arguments"],
        "description": "Arbitrary positional and keyword argument packing and unpacking.",
        "content_md": """## *args and **kwargs

The `*args` syntax allows a function to accept any number of positional arguments as a tuple, while `**kwargs` accepts arbitrary keyword arguments as a dictionary.

```python
def logger(level, *args, **kwargs):
    print(f"[{level}] Positional: {args}, Keywords: {kwargs}")

logger("INFO", "server started", 8080, port=8080, host="0.0.0.0")
```

The reverse operation unpacks sequences into arguments (`func(*my_list)`) and dictionaries into keyword arguments (`func(**my_dict)`).
"""
    },
    {
        "slug": "higher-order-functions",
        "title": "Higher-Order Functions",
        "difficulty": 3,
        "prerequisites": ["functions-basics", "lambda-functions"],
        "description": "Functions as first-class citizens: passing functions, map, and filter.",
        "content_md": """## Higher-Order Functions

In Python, functions are first-class citizens: they can be assigned to variables, passed as arguments to other functions, and returned from functions.

```python
def apply_twice(func, val):
    return func(func(val))

print(apply_twice(lambda x: x + 1, 5))  # 7
```

Built-in higher-order functions include `map(func, iterable)` which applies a transformation to each element, and `filter(predicate, iterable)` which extracts matching elements.
"""
    },
    {
        "slug": "recursion",
        "title": "Recursion",
        "difficulty": 3,
        "prerequisites": ["functions-basics", "if-statements"],
        "description": "Base cases, recursive calls, call stack limits, and RecursionError.",
        "content_md": """## Recursion

A recursive function solves a problem by calling itself with smaller sub-problems until reaching a terminating base case.

```python
def factorial(n):
    if n <= 1:
        return 1  # Base case
    return n * factorial(n - 1)  # Recursive step
```

Every recursive algorithm requires a valid base case to prevent infinite recursion. Python protects system memory with a default recursion limit (usually 1,000 frames), raising a `RecursionError` if exceeded.
"""
    },

    # Difficulty 3-4: Strings Advanced, IO, Exceptions
    {
        "slug": "regular-expressions-intro",
        "title": "Intro to Regular Expressions",
        "difficulty": 3,
        "prerequisites": ["strings-basics", "string-methods"],
        "description": "Pattern matching, extraction, and validation with the re module.",
        "content_md": """## Regular Expressions (re module)

Regular expressions provide a pattern-matching language for string search, validation, and extraction. Python supports regex via the built-in `re` module.

```python
import re

pattern = r"\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
text = "Contact support@example.com for help."
match = re.search(pattern, text)
if match:
    print(f"Found email: {match.group()}")
```

Always use raw strings (`r"..."`) for regex patterns to prevent Python from interpreting backslashes as string escape sequences. Key functions include `re.search()`, `re.match()`, `re.findall()`, and `re.sub()`.
"""
    },
    {
        "slug": "file-reading",
        "title": "Reading Files",
        "difficulty": 3,
        "prerequisites": ["strings-basics"],
        "description": "Opening file handles, read modes, read(), readline(), and readlines().",
        "content_md": """## Reading Files

Files are accessed using Python's built-in `open()` function, specifying the file path and mode (e.g. `'r'` for text reading).

```python
file = open("data.txt", "r", encoding="utf-8")
content = file.read()
file.close()
```

Reading methods include `read()` (reads entire file as a string), `readline()` (reads a single line), and iterating directly over the file object line-by-line (`for line in file:`), which is memory efficient for large files. Always specify `encoding="utf-8"` to avoid platform-dependent encoding bugs.
"""
    },
    {
        "slug": "file-writing",
        "title": "Writing Files",
        "difficulty": 3,
        "prerequisites": ["strings-basics", "file-reading"],
        "description": "Writing and appending text with 'w' and 'a' modes.",
        "content_md": """## Writing Files

To write to a file, open it in `'w'` mode (write / overwrite) or `'a'` mode (append to existing contents).

```python
f = open("log.txt", "w", encoding="utf-8")
f.write("System initialized\\n")
f.close()
```

Be cautious: opening an existing file with mode `'w'` truncates it to 0 bytes immediately, erasing prior content. Use `'a'` when you need to preserve existing data.
"""
    },
    {
        "slug": "file-context-managers",
        "title": "Context Managers (with statement)",
        "difficulty": 3,
        "prerequisites": ["file-reading", "file-writing"],
        "description": "Deterministic resource cleanup using the with statement.",
        "content_md": """## Context Managers (with statement)

The `with` statement guarantees that resources like file descriptors, sockets, or database connections are cleanly closed upon exiting the block, even if an exception occurs.

```python
with open("report.txt", "r", encoding="utf-8") as file:
    data = file.read()
# file is automatically closed here
```

Context managers implement the `__enter__()` and `__exit__()` dunder methods, eliminating the risk of resource leaks from forgotten `close()` calls.
"""
    },
    {
        "slug": "file-paths",
        "title": "File Paths (pathlib)",
        "difficulty": 3,
        "prerequisites": ["file-reading"],
        "description": "Cross-platform path manipulation using modern pathlib.Path.",
        "content_md": """## File Paths with pathlib

The modern `pathlib` module provides object-oriented, cross-platform path handling that replaces legacy `os.path` string operations.

```python
from pathlib import Path

data_dir = Path("data") / "raw"
file_path = data_dir / "records.csv"

if file_path.exists():
    text = file_path.read_text(encoding="utf-8")
```

The slash operator `/` joins path segments cleanly regardless of whether the operating system uses forward slashes (Linux/macOS) or backslashes (Windows).
"""
    },
    {
        "slug": "exceptions-basics",
        "title": "Understanding Exceptions",
        "difficulty": 3,
        "prerequisites": ["if-statements"],
        "description": "The exception lifecycle, tracebacks, and unexpected program termination.",
        "content_md": """## Understanding Exceptions

An exception is an event triggered during program execution that disrupts the normal flow of instructions. When an error occurs (such as dividing by zero or indexing past the end of a list), Python raises an exception object.

```python
# Raises ZeroDivisionError:
# result = 10 / 0
```

Uncaught exceptions bubble up the call stack and terminate the program, printing a traceback that details the sequence of calls leading to the failure.
"""
    },
    {
        "slug": "try-except",
        "title": "try/except Blocks",
        "difficulty": 3,
        "prerequisites": ["exceptions-basics"],
        "description": "Catching and handling runtime exceptions gracefully.",
        "content_md": """## try/except Blocks

The `try/except` construct allows applications to intercept exceptions and recover gracefully without crashing.

```python
try:
    num = int(input("Enter number: "))
    result = 100 / num
except ValueError:
    print("Invalid numeric format")
except ZeroDivisionError:
    print("Cannot divide by zero")
```

Always catch specific exception types rather than using a bare `except:`, which catches system exit signals and interrupts, masking real bugs.
"""
    },
    {
        "slug": "exception-types",
        "title": "Common Exception Types",
        "difficulty": 3,
        "prerequisites": ["try-except"],
        "description": "ValueError, TypeError, KeyError, IndexError, AttributeError, FileNotFoundError.",
        "content_md": """## Common Exception Types

Python provides a hierarchy of built-in exceptions derived from `BaseException` and `Exception`:
- `ValueError`: Received correct type but invalid value (e.g., `int("abc")`).
- `TypeError`: Operation applied to incompatible type (e.g., `'a' + 5`).
- `KeyError`: Mapping key not found in dictionary.
- `IndexError`: Sequence index out of range.
- `AttributeError`: Object has no such attribute or method.
- `FileNotFoundError`: Requested disk file does not exist.
"""
    },
    {
        "slug": "raising-exceptions",
        "title": "Raising Exceptions",
        "difficulty": 3,
        "prerequisites": ["try-except"],
        "description": "Signaling invalid states with the raise statement.",
        "content_md": """## Raising Exceptions

You can explicitly raise exceptions using the `raise` keyword to signal invalid inputs or broken invariants.

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age
```

Exceptions can be re-raised inside an `except` block using a bare `raise`, allowing logging while still letting the caller handle the failure.
"""
    },
    {
        "slug": "finally-else",
        "title": "finally and else in try Blocks",
        "difficulty": 3,
        "prerequisites": ["try-except"],
        "description": "Guaranteed cleanup with finally and error-free code separation with else.",
        "content_md": """## finally and else in try Blocks

The complete `try` statement includes optional `else` and `finally` clauses:

```python
try:
    f = open("data.txt")
except FileNotFoundError:
    print("File missing")
else:
    print("File opened successfully")
    data = f.read()
finally:
    print("Always executes, regardless of errors")
```

The `else` block executes only if NO exceptions were raised in `try`. The `finally` block executes unconditionally, making it the standard location for guaranteed cleanup.
"""
    },
    {
        "slug": "custom-exceptions",
        "title": "Custom Exception Classes",
        "difficulty": 4,
        "prerequisites": ["try-except"],
        "description": "Subclassing Exception to define domain-specific error hierarchies.",
        "content_md": """## Custom Exception Classes

Applications define domain-specific exceptions by subclassing the built-in `Exception` class.

```python
class InsufficientFundsError(Exception):
    \"\"\"Raised when account balance is too low for withdrawal.\"\"\"
    def __init__(self, balance, amount):
        super().__init__(f"Balance {balance} < withdrawal amount {amount}")
        self.balance = balance
        self.amount = amount
```

Custom exceptions make error handling informative and allow caller code to catch precise domain failures without relying on generic system exceptions.
"""
    },

    # Difficulty 4: OOP
    {
        "slug": "oop-concepts",
        "title": "OOP Concepts Overview",
        "difficulty": 4,
        "prerequisites": ["functions-basics", "dicts-basics"],
        "description": "Classes, objects, encapsulation, inheritance, and polymorphism in Python.",
        "content_md": """## OOP Concepts Overview

Object-Oriented Programming (OOP) is a paradigm that organizes software around data models (objects) that combine state (attributes) and behavior (methods).

The core principles of OOP are:
1. **Encapsulation**: Bundling data with methods that operate on that data.
2. **Abstraction**: Hiding internal implementation details behind clean interfaces.
3. **Inheritance**: Deriving new classes from existing ones to promote reuse.
4. **Polymorphism**: Allowing different classes to respond to the same interface or method call.
"""
    },
    {
        "slug": "classes-basics",
        "title": "Defining Classes",
        "difficulty": 4,
        "prerequisites": ["oop-concepts"],
        "description": "The class keyword, instantiating objects, and the self parameter.",
        "content_md": """## Defining Classes

A class serves as a blueprint for creating objects. Classes are defined using the `class` keyword with CapWords naming convention.

```python
class Robot:
    def speak(self):
        return "Beep boop!"

bot = Robot()        # Instantiation
print(bot.speak())   # Method invocation
```

When invoking `bot.speak()`, Python automatically passes the instance `bot` as the first argument (`self`), allowing the method to access instance state.
"""
    },
    {
        "slug": "constructors",
        "title": "__init__ Constructor",
        "difficulty": 4,
        "prerequisites": ["classes-basics"],
        "description": "Initializing instance state and attributes with __init__.",
        "content_md": """## The __init__ Constructor

The `__init__()` method is Python's initializer (constructor). It executes automatically whenever a new instance of a class is created.

```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.is_active = True

u = User("alex", "alex@example.com")
```

The `self` argument refers to the newly created instance. Attributes attached to `self` become instance variables unique to that specific object.
"""
    },
    {
        "slug": "instance-methods",
        "title": "Instance Methods and self",
        "difficulty": 4,
        "prerequisites": ["classes-basics", "constructors"],
        "description": "Writing methods that query and mutate instance attributes via self.",
        "content_md": """## Instance Methods and self

Instance methods are functions defined inside a class that take `self` as their first parameter.

```python
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        return self.balance
```

Through `self`, methods can inspect and mutate the state of the invoking instance, providing encapsulated operations.
"""
    },
    {
        "slug": "class-attributes",
        "title": "Class vs Instance Attributes",
        "difficulty": 4,
        "prerequisites": ["classes-basics"],
        "description": "Shared class-level state vs per-instance attributes.",
        "content_md": """## Class vs Instance Attributes

Attributes defined directly in the class body are **class attributes**, shared across all instances. Attributes attached to `self` in `__init__` are **instance attributes**.

```python
class Employee:
    company = "Acme Corp"  # Class attribute shared by all employees

    def __init__(self, name):
        self.name = name   # Instance attribute unique to each employee
```

Mutating a class attribute via `Employee.company = "NewCo"` updates the value for all instances. Modifying it via `emp.company = "Other"` creates a local instance attribute that shadows the class attribute.
"""
    },
    {
        "slug": "encapsulation",
        "title": "Encapsulation and Properties",
        "difficulty": 4,
        "prerequisites": ["classes-basics", "instance-methods"],
        "description": "Private attributes (_var, __var) and getters/setters via @property.",
        "content_md": """## Encapsulation and Properties

Python does not have strict `private` keywords. By convention, a leading underscore (`_name`) indicates an internal, non-public attribute. A double underscore (`__name`) triggers name mangling to avoid accidental subclass collisions.

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value
```

The `@property` decorator allows attributes to be accessed like normal fields (`t.celsius`) while routing through getter and setter validation methods.
"""
    },
    {
        "slug": "inheritance",
        "title": "Inheritance",
        "difficulty": 4,
        "prerequisites": ["classes-basics", "instance-methods"],
        "description": "Subclassing, code reuse, and delegating to parent via super().",
        "content_md": """## Inheritance

Inheritance allows a child class to inherit attributes and methods from a parent class, extending or overriding them as needed.

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # Delegate name initialization to Animal
        self.breed = breed
```

The `super()` function returns a proxy object that delegates method calls to a parent or sibling class, properly supporting Python's Method Resolution Order (MRO).
"""
    },
    {
        "slug": "method-overriding",
        "title": "Method Overriding",
        "difficulty": 4,
        "prerequisites": ["inheritance"],
        "description": "Redefining inherited methods in subclasses and polymorphic behavior.",
        "content_md": """## Method Overriding

A subclass can override a method defined in its parent class by defining a method with the exact same name and signature.

```python
class Shape:
    def area(self):
        return 0

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h
```

Method overriding enables polymorphism: caller code can iterate over a list of shapes and invoke `.area()` on each without knowing its concrete class.
"""
    },
    {
        "slug": "special-methods",
        "title": "Special (Dunder) Methods",
        "difficulty": 4,
        "prerequisites": ["classes-basics", "constructors"],
        "description": "Operator overloading with __str__, __repr__, __len__, __eq__.",
        "content_md": """## Special (Magic / Dunder) Methods

Special methods are prefixed and suffixed with double underscores (`__method__`). They allow custom classes to hook into Python's built-in operators and syntax.

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
```

Common dunder methods include `__str__` (user-friendly string), `__repr__` (unambiguous developer representation), `__len__` (length via `len()`), and `__eq__` (equality via `==`).
"""
    },

    # Difficulty 4-5: Algorithms & Complexity
    {
        "slug": "complexity-basics",
        "title": "Big O Notation and Complexity",
        "difficulty": 4,
        "prerequisites": ["for-loops", "lists-basics"],
        "description": "Time and space complexity: O(1), O(log N), O(N), O(N log N), O(N^2).",
        "content_md": """## Big O Notation and Complexity

Big O notation describes how the execution time or memory footprint of an algorithm scales as the input size $N$ grows toward infinity.

- **$O(1)$ Constant time**: Accessing a list element by index or a dict by key.
- **$O(\\log N)$ Logarithmic**: Binary search dividing the search space in half each step.
- **$O(N)$ Linear**: Single pass scanning through an unsorted list.
- **$O(N \\log N)$ Linearithmic**: Optimal comparison-based sorting (Timsort, Mergesort).
- **$O(N^2)$ Quadratic**: Naive nested loops comparing all pairs.
"""
    },
    {
        "slug": "linear-search",
        "title": "Linear Search",
        "difficulty": 4,
        "prerequisites": ["complexity-basics", "lists-basics", "for-loops"],
        "description": "Sequential scanning of unsorted collections in O(N) time.",
        "content_md": """## Linear Search

Linear search checks every element in a sequence sequentially from left to right until the target value is found or the end of the sequence is reached.

```python
def linear_search(items, target):
    for i, val in enumerate(items):
        if val == target:
            return i
    return -1
```

Because it makes no assumptions about data order, linear search works on any collection, operating in $O(1)$ best-case time and $O(N)$ worst-case time with $O(1)$ auxiliary memory.
"""
    },
    {
        "slug": "binary-search",
        "title": "Binary Search",
        "difficulty": 4,
        "prerequisites": ["linear-search", "list-slicing"],
        "description": "Divide-and-conquer search on sorted sequences in O(log N) time.",
        "content_md": """## Binary Search

Binary search locates a target value within a **sorted** sequence by repeatedly halving the search interval.

```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

At each step, binary search eliminates half the remaining elements, yielding $O(\\log N)$ time complexity. This makes searching a 1,000,000 element list take at most ~20 comparisons.
"""
    },
    {
        "slug": "bubble-sort",
        "title": "Bubble Sort",
        "difficulty": 4,
        "prerequisites": ["complexity-basics", "nested-loops", "lists-basics"],
        "description": "Adjacent element swapping algorithm with O(N^2) complexity.",
        "content_md": """## Bubble Sort

Bubble Sort repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
```

In each pass, the largest unsorted element \"bubbles up\" to its correct position. The algorithm runs in $O(N^2)$ average and worst-case time, but achieves $O(N)$ best-case runtime on already-sorted arrays when using an early exit flag.
"""
    },
    {
        "slug": "selection-sort",
        "title": "Selection Sort",
        "difficulty": 4,
        "prerequisites": ["complexity-basics", "nested-loops", "lists-basics"],
        "description": "Finding minimums and placing them in sorted order with O(N^2) complexity.",
        "content_md": """## Selection Sort

Selection Sort divides the input list into a sorted sublist and an unsorted sublist. In each pass, it finds the smallest element in the unsorted portion and swaps it with the leftmost unsorted element.

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

Selection Sort makes $O(N^2)$ comparisons regardless of whether the input is already sorted, but makes at most $O(N)$ swaps.
"""
    },
    {
        "slug": "insertion-sort",
        "title": "Insertion Sort",
        "difficulty": 4,
        "prerequisites": ["complexity-basics", "nested-loops", "lists-basics"],
        "description": "Building a sorted array one item at a time, optimal for small or nearly sorted arrays.",
        "content_md": """## Insertion Sort

Insertion Sort builds the final sorted array one item at a time by repeatedly taking the next element and inserting it into its correct position within the already sorted prefix.

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

Insertion Sort is adaptive: it runs in $O(N)$ time on nearly sorted lists and has minimal overhead, making it the algorithm of choice for small arrays (and the base case in Python's hybrid Timsort).
"""
    },
    {
        "slug": "recursion-algorithms",
        "title": "Recursive Algorithms",
        "difficulty": 4,
        "prerequisites": ["recursion", "complexity-basics"],
        "description": "Classic divide-and-conquer and backtracking problems.",
        "content_md": """## Recursive Algorithms

Recursive algorithms divide complex problems into identical, smaller sub-problems. Classic examples include the Fibonacci sequence, tree traversal, and Tower of Hanoi.

```python
def fibonacci(n, memo=None):
    if memo is None:
        memo = {0: 0, 1: 1}
    if n not in memo:
        memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]
```

Naive recursion without memoization often exhibits exponential $O(2^N)$ time complexity due to redundant calculations. Storing subproblem solutions (memoization) reduces complexity to linear $O(N)$ time.
"""
    },
    {
        "slug": "two-pointer",
        "title": "Two-Pointer Technique",
        "difficulty": 5,
        "prerequisites": ["lists-basics", "while-loops"],
        "description": "Optimizing search and reversal in sorted arrays from O(N^2) to O(N).",
        "content_md": """## Two-Pointer Technique

The two-pointer technique uses two indices that traverse a sequence toward each other or in the same direction, typically reducing an $O(N^2)$ brute-force approach to $O(N)$ linear time.

```python
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        current = numbers[left] + numbers[right]
        if current == target:
            return left, right
        elif current < target:
            left += 1
        else:
            right -= 1
    return None
```

This pattern is fundamental for solving problems involving palindromes, target sums in sorted arrays, and in-place sequence partitioning.
"""
    },
    {
        "slug": "sliding-window",
        "title": "Sliding Window Technique",
        "difficulty": 5,
        "prerequisites": ["lists-basics", "while-loops"],
        "description": "Subarray and substring problems with dynamic or fixed size windows.",
        "content_md": """## Sliding Window Technique

The sliding window technique maintains a contiguous range of elements over a sequence that expands and contracts as it moves forward.

```python
def max_sub_array_sum(arr, k):
    if len(arr) < k:
        return 0
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(len(arr) - k):
        window_sum = window_sum - arr[i] + arr[i + k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

By computing the change incrementally (subtracting the element exiting the window and adding the element entering), sliding window solves contiguous subarray problems in $O(N)$ time rather than $O(N \\times K)$.
"""
    },

    # Difficulty 5: Advanced Python
    {
        "slug": "generators",
        "title": "Generators and yield",
        "difficulty": 5,
        "prerequisites": ["functions-basics", "for-loops"],
        "description": "Lazy evaluation, memory-efficient streams, and generator expressions.",
        "content_md": """## Generators and yield

A generator is a function that produces a sequence of values on demand using the `yield` keyword instead of `return`.

```python
def count_up_to(max_val):
    count = 1
    while count <= max_val:
        yield count
        count += 1

gen = count_up_to(3)
print(next(gen))  # 1
print(next(gen))  # 2
```

When a generator function yields, its local state and instruction pointer are suspended until the caller requests the next item. This enables processing arbitrarily large data streams with $O(1)$ memory consumption.
"""
    },
    {
        "slug": "decorators",
        "title": "Decorators",
        "difficulty": 5,
        "prerequisites": ["higher-order-functions"],
        "description": "Syntactic sugar (@decorator) for modifying and wrapping functions.",
        "content_md": """## Decorators

A decorator is a callable that accepts a function as an argument and returns an augmented wrapper function, applied using the `@decorator_name` syntax.

```python
import functools
import time

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"{func.__name__} took {duration:.4f}s")
        return result
    return wrapper

@timing_decorator
def compute():
    return sum(i * i for i in range(100000))
```

Decorators are widely used for cross-cutting concerns like logging, authentication, caching (`@lru_cache`), and route declaration in web frameworks.
"""
    },
    {
        "slug": "modules-packages",
        "title": "Modules and Packages",
        "difficulty": 5,
        "prerequisites": ["functions-basics"],
        "description": "Importing code, module namespaces, __name__ == '__main__', and __init__.py.",
        "content_md": """## Modules and Packages

A **module** is a single Python file (`.py`) containing definitions and statements. A **package** is a directory of modules that includes an `__init__.py` file.

```python
# Importing from a module:
import math
from datetime import datetime, timezone

# Standard entry point idiom:
if __name__ == "__main__":
    print("Executed directly as script")
```

The `__name__` variable allows code to differentiate whether it was invoked directly as the main script or imported as a library by another module.
"""
    },
    {
        "slug": "standard-library",
        "title": "Key Standard Library Modules",
        "difficulty": 5,
        "prerequisites": ["modules-packages"],
        "description": "Essential modules: collections, itertools, json, os, sys, math, random.",
        "content_md": """## Key Standard Library Modules

Python's philosophy of \"batteries included\" is reflected in its comprehensive standard library:
- `collections`: Specialized container datatypes like `Counter`, `defaultdict`, and `deque`.
- `itertools`: Combinatoric and fast iterator building blocks (`cycle`, `combinations`).
- `json`: Parsing and serializing JSON payloads.
- `math`: Mathematical functions, constants (`pi`, `e`), and trigonometry.
- `random`: Pseudo-random number generation and sequence sampling.
- `sys` and `os`: System parameters, arguments, and low-level environment interaction.
"""
    }
]

def dump_yaml_concepts(concepts):
    out = ["# Python Concepts Database v0 - PROJECT-EVOLVE", ""]
    for c in concepts:
        out.append(f"- slug: \"{c['slug']}\"")
        out.append(f"  title: \"{c['title']}\"")
        out.append(f"  difficulty: {c['difficulty']}")
        out.append(f"  domain: \"{c['domain']}\"")
        out.append(f"  description: \"{c['description']}\"")
        prereqs = c.get('prerequisites', [])
        if prereqs:
            out.append("  prerequisites:")
            for p in prereqs:
                out.append(f"    - \"{p}\"")
        else:
            out.append("  prerequisites: []")
        out.append("  content_md: |")
        for line in c['content_md'].strip().splitlines():
            out.append(f"    {line}")
        out.append("")
    return "\n".join(out)

def main():
    print(f"Total concepts defined: {len(CONCEPTS_DEF)}")
    for c in CONCEPTS_DEF:
        c["domain"] = "python_fundamentals"
        assert "slug" in c
        assert "title" in c
        assert "difficulty" in c
        assert "description" in c
        assert "content_md" in c
        assert "prerequisites" in c

    output_path = r"e:\hackathon\content\python\concepts.yaml"
    yaml_text = dump_yaml_concepts(CONCEPTS_DEF)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(yaml_text)

    print(f"Wrote {len(CONCEPTS_DEF)} concepts to {output_path} ({len(yaml_text)} bytes)")

if __name__ == "__main__":
    main()

