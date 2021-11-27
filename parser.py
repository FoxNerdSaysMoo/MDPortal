from rply import ParserGenerator
import re
from lexer import exp_rev, features_rev

pg = ParserGenerator(list(exp_rev.keys()),
                     precedence=[("left", [])], cache_id="mdp")


@pg.production("main : doc")
def main(p):
    return open("template.html").read() % p[0]


@pg.production("doc : doc meta")
@pg.production("doc : doc text")
@pg.production("doc : doc html")
@pg.production("doc : doc class")
@pg.production("doc : doc other")
@pg.production("doc : meta")
@pg.production("doc : text")
@pg.production("doc : html")
@pg.production("doc : class")
@pg.production("doc : other")
def doc(p):
    return p[0] + "\n\t" + p[1] if len(p) > 1 else ""


@pg.production("html : HTML")
def html(p):
    return p[0].value[0]


@pg.production("other : CSS")
def css(p):
    return f"<style>{p[0].value[0]}</style>"


@pg.production("other : COMMENT")
def comment(p):
    return f"<!-- {p[0].value[0]} -->"


@pg.production("class : CLASS_START")
def class_start(p):
    return f"<div class='{p[0].value[0]}'>"


@pg.production("class : CLASS_END")
def class_end(p):
    """Favorite part of the day"""
    return "</div>"


@pg.production("meta : META VALUE")
def meta(p):
    return f'<meta name="{p[1].value[0]}" content="{p[1].value[0]}">'


@pg.production("other : TITLE")
def title(p):
    return f"<title>{p[0].value[0]}</title>"


def asterisks(start, end, preserve=True):
    c = -1

    def add_format(g):
        nonlocal c
        c += 1
        chars = [i for i in g.groups() if i]
        print(chars)
        if c % 2 == 0:
            return start + (chars[0] if preserve else '')
        else:
            return (chars[0] + chars[1] if preserve else '') + end
    return add_format


@pg.production("text : TEXT")
@pg.production("text : header TEXT")
def text(p):
    text_style = p[0] if len(p) > 1 and p[0] else ''
    content = p[0].value[0] if len(p) == 1 else p[1].value[0]
    content = re.sub(exp_rev["CLASS_START"], "", content)
    content = re.sub(exp_rev["CLASS_END"], "", content)
    content = re.sub(exp_rev["COMMENT"], "", content)
    content = re.sub(features_rev["ITALIC"], asterisks("<i>", "</i>"), content)
    content = re.sub(features_rev["BOLD"], asterisks("<b>", "</b>"), content)
    content = re.sub(features_rev["ITALIC_BOLD"], asterisks("<i><b>", "</b></i>"), content)
    content = re.sub(features_rev["CODE"], asterisks("<code>", "</code>"), content)
    content = re.sub(features_rev["CODE_BLOCK"], asterisks("<pre><code>", "</code></pre>"), content)
    content = re.sub(features_rev["LINK"], r"<a href='\2'>\1</a>", content)
    content = re.sub(features_rev["DELETED"], asterisks("<del>", "</del>"), content)
    content = content.replace("\\n", "<br>")
    return f"<p style='{text_style}'>{content}</p>"


@pg.production("header : style header")
@pg.production("header : style")
def header(p):
    return p[0] + (p[1] if len(p) > 1 else "")


@pg.production("header : HEADER header")
@pg.production("header : HEADER")
def header_size(p):
    size = len(p[0].value[0])
    class_str = "' class='h" + str(size-1)
    return (class_str if size > 1 else "") + (p[1] if len(p) > 1 else "")


@pg.production("style : style VALUE")
@pg.production("style : STYLE")
def style(p):
    if len(p) > 1:
        return p[0]
    else:
        return p[0].value[0]
