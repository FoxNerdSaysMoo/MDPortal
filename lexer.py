from rply import Token
import re


features = {
    r"([^/\\*])\*([^/*])|^\*([^/*])|([^/\\*])\*$": "ITALIC",
    r"([^/\\*])\*\*([^/*])|^\*\*([^/*])|([^/\\*])\*\*$": "BOLD",
    r"([^/\\*])\*\*\*([^/*])|^\*\*\*([^/*])|([^/\\*])\*\*\*$": "ITALIC_BOLD",
    r"([^`\\])```([^`])|([^`\\])```$|^```([^`])": "CODE_BLOCK",
    r"([^`\\])`([^`])|([^`\\])`$|^`([^`])": "CODE",
    r"\[(.*?)\]\((.*?)\)": "LINK",
    r"([^~\\])~~([^~])|([^~\\])~~$|^~~([^~])": "DELETED",
}

features_rev = {v: k for k, v in features.items()}

exp = {
    r"meta\{ (.*?) \}": "META",
    r"}(#+)|\n(#+)|^(#+)": "HEADER",
    r"\n{ ((?:.*?\n*?)*?) }|^{ ((?:.*?\n*?)*?) }": "STYLE",
    r"(\S+)\: (.*?);+|(\S+)\: (.*?) }": "VALUE",
    r"(?:})?(?:#)+ ((?:.+?(?:\n)?)+)": "TEXT",
    r"{html}((?:.*\n)*?){/html}": "HTML",
    r"\[(\w+)\]": "CLASS_START",
    r"\[/\]": "CLASS_END",
    r"title{ (.*?) }": "TITLE",
    r"{css}((?:.*\n)*?){/css}": "CSS",
    r"// (.*)|/\*((?:.*\n)*?)\*/": "COMMENT",
}

exp_rev = {v: k for k, v in exp.items()}


class Lexer:
    def __init__(self, inp: str):
        self.string = inp
        self.matches = {}
        self.current = 0

        for pat, tkn in exp.items():
            for match in re.finditer(pat, self.string):
                start = match.start()
                if start in self.matches:
                    self.matches[start].append((tkn, match.groups()))
                else:
                    self.matches[start] = [(tkn, match.groups())]

        self.matches = sorted(self.matches.items())
        self.matches = [item for _, sublist in self.matches for item in sublist]

    def next(self):
        if self.current+1 > len(self.matches):
            return None
        item = self.matches[self.current]
        token = Token(item[0], [i for i in item[1] if i], self.current)
        print(token)
        self.current += 1
        return token

    __next__ = next
