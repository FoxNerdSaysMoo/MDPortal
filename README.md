# MDPortal
## A module to convert a md-eqsue lang to html
### Basically I ruined md in an attempt to convert it to html

## Overview

Here is a demo file
```py
from parser import pg
from lexer import Lexer  # Custom lexer

parse = pg.build()  # Parser generator

out = parse.parse(Lexer(open("example.mdp").read()))  # Parse and lex it

with open("out.html", "w") as wf:  # Write the html to a file
    wf.write(out)
```

## Syntax

View `example.mdp` for an example of most features.

### Metadata

```
meta{ name: content }
```

### Title

```
title{ page title }
```

### Text

```
# Normal text

# Text
can
also
span
downwards

# but
with
blank
lines
in
between
```

### Headings

```
## header 1
### header 2
#### header 3
##### header 4
```

### Class

```
[myclass]# I'm in a class![/]
```

### Italic, bold, bold-italic

```
# *italic*

# **bold**

# ***bold AND italic***
```

### Inline css

```
{ font-family: Roboto }# I am roboto

{ font-family: Verdana;
background-color: #f0f0f0;
border-radius: 0.3em }# I am Verdana with a light grey and rounded corner
```

### Comments

```
// Single line

/*
multi
line
*/
```

### Line break

```
# I am\ntwo-\nno, three lines
```

### Standard md stuff

```
# ~~deleted~~ [link](https://example.com) `code`
# ```
code block
\```
```

### Out-of-line css

```
{css}
body {
    margin: auto
}
{/css}
```

### HTML

```
{html}
<script src="/index.js"></script>
{/html}
```
