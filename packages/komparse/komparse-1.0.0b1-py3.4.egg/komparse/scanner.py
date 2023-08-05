from collections import namedtuple
from .token_stream import TokenStream

Token = namedtuple('Token', 'type value')

class Scanner(object):
    
    def __init__(self, grammar):
        self._grammar = grammar
        
    def find_tokens(self, source):
        tokens = []
        remaining = source
        while remaining:
            for name, regex in self._grammar.get_token_patterns():
                m = regex.match(remaining)
                if m:
                    text = m.group(1)
                    if name not in [self._grammar.WHITESPACE, self._grammar.COMMENT]:
                        tokens.append(Token(name, text))
                    remaining = remaining[len(text):]
                    break
            else:
                break
        if remaining:
            raise Exception("Code could not be resolved: {}".format(remaining))
        return TokenStream(tokens)