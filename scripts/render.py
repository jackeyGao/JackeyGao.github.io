# -*- coding: utf-8 -*-
import jinja2
import os
import sys
from os.path import splitext
from datetime import datetime
from md import markrender

reload(sys)
sys.setdefaultencoding('utf-8')

template_loader = jinja2.FileSystemLoader(searchpath="templates")
template_env = jinja2.Environment(loader=template_loader)
WORD_TEMPLATE_FILE = "word.html"
WORDS_TEMPLATE_FILE = "index.html"
RSS_TEMPLATE_FILE = 'rss.xml'
GALLERY_TEMPLATE_FILE = 'gallery.html'

markdown_files = os.listdir('markdown')

#albums = os.listdir('uploads/album')

words = []

for file in markdown_files:
    with open("markdown/%s" % file) as f:
        content = f.read()

    title = ' '.join(word.title() for word in file[:-3].split('-'))
    filename = splitext(file)[0]

    headers = content.split('---')[0]
    content = '---'.join(content.split('---')[1:])

    for line in headers.splitlines():
        if line.startswith('title'):
            title = ':'.join(line.split(':')[1:]).strip()
        if line.startswith('date'):
            date = ':'.join(line.split(':')[1:]).strip()

    if not title or not date:
        print("%s 头信息解析失败" % filename)
        continue

    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    words.append({
        'filename': filename,
        'title': title,
        'date': date
    })
    
    md = markrender(content)

    template = template_env.get_template(WORD_TEMPLATE_FILE)
    output = template.render(title=title, content=md, date=date, filename=filename)

    html_filename = splitext(file)[0] + '.html'
    with open('words/%s' % html_filename, 'w') as f:
        f.write(output)


words = sorted(words, key=lambda x: x["date"], reverse=True)
template = template_env.get_template(WORDS_TEMPLATE_FILE)
output = template.render(words=words)
with open('index.html', 'w') as f: f.write(output)


template = template_env.get_template(RSS_TEMPLATE_FILE)
output = template.render(words=words)
with open('rss.xml', 'w') as f: f.write(output)


#imgObjs = []
#for album in albums:
#    
#    album_dir = os.path.join('uploads/album/', album)
#
#    imgs = os.listdir(album_dir)
#
#    imgObj = {}
#    imgObj["album"] = album
#
#    subimg_list = []
#    for img in imgs:
#        img_path = os.path.join(album, img)
#
#        if img.startswith('^'):
#            imgObj["first"] = img_path
#
#        subimg_list.append(img_path)
#
#    imgObj["sub_imgs"] = subimg_list
#
#    if not imgObj.get('first', None):
#        imgObj["first"] = subimg_list[0]
#        
#    
#    imgObjs.append(imgObj)
#
#
#template = template_env.get_template(GALLERY_TEMPLATE_FILE)
#output = template.render(albums=imgObjs)
#with open('gallery.html', 'w') as f: f.write(output)
