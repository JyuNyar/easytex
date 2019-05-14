import re

_latex_special_chars = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\^{}',
#     '\\': r'\textbackslash{}',
#     '\n': '\\newline%\n',
    '-': r'{-}',
    '\xA0': '~',  # Non-breaking space
    '[': r'{[}',
    ']': r'{]}',
}

def clean_tex(tex):
    
    tex = str(tex)
    
    pattern = '|'.join(sorted(re.escape(k) for k in _latex_special_chars))
    
    return re.sub(pattern, lambda m: _latex_special_chars.get(m.group(0)), tex)