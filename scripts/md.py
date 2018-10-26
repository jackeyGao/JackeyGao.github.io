# -*- coding: utf-8 -*-
'''
File Name: markdown.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 五  8/12 09:59:17 2016
'''
import sys, re
import misaka as m
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

reload(sys)
sys.setdefaultencoding('utf-8')

cleanr =re.compile('<.*?>')


class HighlighterRenderer(m.HtmlRenderer):
    def blockcode(self, text, lang):
        if not lang:
            return '''<div class="code-wrapper">
          <div class="lang-label">Raw</div>
        \n<div class="highlight"><pre>{}</pre></div></div>\n'''.format(
                text.strip())


        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            language = lexer.name
        except ClassNotFound:
            lexer = get_lexer_by_name('text', stripall=True)
            language = lang
            
        formatter = HtmlFormatter()
        content = highlight(text, lexer, formatter)
            
        langDiv = '<div class="lang-label">' + language + '</div>'
        return '<div class="code-wrapper">' + langDiv + content + '</div>'


    def blockquote(self, content):
        _real = re.sub(cleanr,'', content).strip()
        if _real.startswith('%center\n'):
            content = content.replace('%center', '')
            className = "blockquote-center"
        elif _real.startswith('%warning'):
            content = content.replace('%warning', '')
            className = "blockquote-warning"
        elif _real.startswith('%error'):
            content = content.replace('%error', '')
            className = "blockquote-error"
        else:
            content = content
            className = "blockquote-normal"
        
        content = content.replace('\n', '<br/>')
        content = content.replace('</p><br/>', '</p>')
        content = content.replace('<p><br/>', '<p>')

        return '''<blockquote class="%s">
                %s</blockquote>''' % (className, content)

    def image(self, link, title="", alt=''):
        #link = link.replace('/uploads', 'https://o8uou7r4o.qnssl.com')

        if title == 'cover':
            self.cover = link

        if alt == 'hidden':
            return '<p style="display: none;"></p>'

        if alt:
            return  '''
                    <p class="hassubimage"><img src="%s"></p>
                    <p class="img-title"><span class="symbol">#</span>%s</p>''' % (link, alt)
        else:
            return '<p class="hassubimage"><img src="%s"></p>\n' % (link)

    def table(self, content):
        return '<div class="code table-wrapper"><table class="ui selectable celled table">'\
                + content + '</table></div>'


markdown = m.Markdown(
    HighlighterRenderer(),
    extensions=\
    m.EXT_FENCED_CODE |\
    m.EXT_TABLES |\
    m.EXT_QUOTE
)

#toc = m.Markdown(m.HtmlTocRenderer())

def markrender(content):
    md = markdown(content)
    print(dir(markdown))
    return md

if __name__ == '__main__':
    print markrender('''> %center''')
