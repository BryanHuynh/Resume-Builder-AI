from pylatex.base_classes import Container
from pylatex import Command, MiniPage, Package
from pylatex.utils import NoEscape, bold, escape_latex

horizontal_line = NoEscape(r"\noindent\rule{\textwidth}{0.5pt}")

class SectionDivider(Container):
    def __init__(self, bottom_space='0.03cm'):
        super().__init__()
        self.append(NoEscape(r"\noindent\rule{\textwidth}{0.5pt}"))
        self.append(NoEscape(r"\par"))
        if bottom_space:
            self.append(Command('vspace', NoEscape(bottom_space)))

    def dumps(self):
        return self.dumps_content()
    
class SectionTitle(Container):
    def __init__(self, section_title: str, section: MiniPage):
        super().__init__()
        title = escape_latex(section_title)
        section.append(NoEscape(rf"\noindent{{\Large\textbf{{{title}}}}}\\[-0.19cm]"))
        section.append(SectionDivider())
            
    def dumps(self):
        return self.dumps_content()
    
    
class DocumentFont:
    SERIF_FONTS = {'ebgaramond', 'times', 'palatino', 'charter', 'mathptmx'}
    FONT_OPTIONS = {
        'ebgaramond': 'lining',
    }

    def __init__(self, font_name: str):
        self.font_name = font_name

    def add_to_document(self, doc):
        options = self.FONT_OPTIONS.get(self.font_name.lower())
        doc.preamble.append(Package(self.font_name, options=options))
        if self.font_name.lower() in self.SERIF_FONTS:
            doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\rmdefault}'))
        else:
            doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))
