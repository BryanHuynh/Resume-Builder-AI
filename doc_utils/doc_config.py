from pylatex.utils import NoEscape

geometry_options = {
    "top": "0.13in",
    "right": "0.5in",
    "bottom": "0.29in",
    "left": "0.5in",
}

enum_item_package = NoEscape(r"\usepackage{enumitem}")
hyperref_package = NoEscape(r"\usepackage[hidelinks]{hyperref}")
no_par_indent = NoEscape(r"\setlength{\parindent}{0pt}")

font_sizes = {
    'small': (9.5, 11),      # SmallText
    'normalsize': (10.5, 12),
    'large': (11.5, 13),      # LargeText
}

def get_font_size_preamble():
    lines = []
    for cmd, (size, skip) in font_sizes.items():
        lines.append(rf'\renewcommand{{\{cmd}}}{{\fontsize{{{size}}}{{{skip}}}\selectfont}}')
    return NoEscape('\n'.join(lines))

itemize_options = NoEscape(r'nosep, topsep=2pt, partopsep=0pt, leftmargin=*, itemsep=1.5pt, parsep=0pt')
additionals_itemize_options = NoEscape(r'nosep, topsep=0pt, partopsep=0pt, leftmargin=*, itemsep=1.5pt, parsep=0pt')
sub_itemize_options = NoEscape(r'nosep, topsep=2pt, partopsep=0pt, leftmargin=*, itemsep=1.5pt, parsep=0pt')
