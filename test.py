import markdown

from markdown_nlp import MarkdownNLP
sample_text = open('test.txt', 'r').read()

print(markdown.markdown(sample_text, extensions=['markdown_nlp:MarkdownNLP']))
