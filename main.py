from parser import pg
from lexer import Lexer

parse = pg.build()

out = parse.parse(Lexer(open("example.mdp").read()))

with open("out.html", "w") as wf:
    wf.write(out)
