from markdown.util import etree
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

import nltk

import hashlib
from base64 import b64decode, b64encode

class SemanticTreeprocessor(Treeprocessor):
    def checksum(self, string):
        the_hash = hashlib.sha224(string.encode('UTF-8')).hexdigest()
        return the_hash

    def handle_li(self, element):
        text = element.text
        element.text = ''
        span = etree.SubElement(element, 'span')
        span.text = text
        span.set('hash', self.checksum(text))
        span.set('semantic_type', 'bulletpoint')

    def handle_paragraph(self, element):
        text_temporary = element.text
        element.text = ''
        for sentence in nltk.sent_tokenize(text_temporary):
            span = etree.SubElement(element, 'span')
            span.text = sentence + ' '
            span.set('hash', self.checksum(sentence))
            span.set('semantic_type', 'sentence')

    #TODO: More elegant conditionals, involve XPath
    def run(self, root):
        for child in root:
            if child.tag == 'ul':
                for subchild in child:
                    if subchild.tag == 'li':
                        self.handle_li(subchild)
            if child.tag == 'p':
                self.handle_paragraph(child)

class SemanticMarkdown(Extension):
    def makeExtension(*args, **kwargs):
        return ConfigExtension(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
       md.registerExtension(self)
       treeprocessor = SemanticTreeprocessor()
       treeprocessor.ext = self
       md.treeprocessors['semantic'] = treeprocessor
