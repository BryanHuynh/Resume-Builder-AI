from pylatex.base_classes import Container
from pylatex import Command, NewLine, MiniPage, LargeText, LineBreak, Package
from pylatex.utils import NoEscape
from pylatex.utils import bold

horizontal_line = NoEscape(r"\noindent\rule{\textwidth}{0.5pt}")

class SectionDivider(Container):
    def __init__(self, top_space='-0.25cm', bottom_space='0.05cm'):
        super().__init__()
        if top_space:
            self.append(Command('vspace', NoEscape(top_space)))
        self.append(NewLine())
        self.append(NoEscape(r"\noindent\rule{\textwidth}{0.5pt}"))
        if bottom_space:
            self.append(Command('vspace', NoEscape(bottom_space)))

    def dumps(self):
        return self.dumps_content()
    
class SectionTitle(Container):
    def __init__(self, section_title: str, section: MiniPage):
        super().__init__()
        section.append(LargeText(bold(section_title)))
        section.append(SectionDivider())
        self.append(NewLine())
            
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