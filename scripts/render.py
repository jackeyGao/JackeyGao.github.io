# -*- coding: utf-8 -*-
import jinja2
import os, json
import sys
from uuid import uuid4
from os.path import splitext
from collections import defaultdict
from datetime import datetime
from md import markrender, new_markdown
from pagination import Pagination

version = uuid4().hex

reload(sys)
sys.setdefaultencoding('utf-8')

template_loader = jinja2.FileSystemLoader(searchpath="templates")
template_env = jinja2.Environment(loader=template_loader)
WORD_TEMPLATE_FILE = "word.html"
WORDS_TEMPLATE_FILE = "index.html"
RSS_TEMPLATE_FILE = 'rss.xml'
SITEMAP_TEMPLATE_FILE = 'sitemap.xml'
GALLERY_TEMPLATE_FILE = 'gallery.html'
markdown_files = os.listdir('markdown')
friends_file = os.path.join('config/friends.json')



if os.path.exists(friends_file):
    with open(friends_file, 'r') as f:
        friends = json.loads(f.read())
else:
    friends = []

gs = {}
gs['friends'] = friends

sets = defaultdict(list)

#albums = os.listdir('uploads/album')

words = []
pages = []

for file in markdown_files:
    with open("markdown/%s" % file) as f:
        content = f.read()

    title = ' '.join(word.title() for word in file[:-3].split('-'))
    filename = splitext(file)[0]

    headers = content.split('---')[0]
    content = '---'.join(content.split('---')[1:]).strip().strip('\n')



    title, date, set_name, isPage = '', '', None, ''

    for line in headers.splitlines():
        if line.startswith('title'):
            title = ':'.join(line.split(':')[1:]).strip()
        if line.startswith('date'):
            date = ':'.join(line.split(':')[1:]).strip()
        if line.startswith('set'):
            set_name = ':'.join(line.split(':')[1:]).strip()
        if line.startswith('isPage'):
            isPage = ':'.join(line.split(':')[1:]).strip()

    if not title or not date:
        print("%s 头信息解析失败" % filename)
        continue

    markdown = new_markdown()

    md = markdown(content)
    
    cover = getattr(markdown.renderer, 'cover', None)
    links = getattr(markdown.renderer, 'links', [])

    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    word = {
        'filename': filename,
        'title': title,
        'date': date,
        'cover': cover,
        'set': set_name,
        'content': md,
        'links': links,
        'is_page': isPage
    }

    word.update(gs)

    if isPage:
        pages.append(word)
    else:
        words.append(word)


    if set_name:
        sets[set_name].append(word)
        sets[set_name].sort(key=lambda x: x["date"])



PER_PAGE = 15

gs['sets'] = sets

all_words = sorted(words, key=lambda x: x["date"], reverse=True)

for page in pages:
    template = template_env.get_template('%s.html' % page["filename"])
    output_file = 'r/%s.html' %  page["filename"]

    output = template.render(version=version, sets=sets, **page)
    with open(output_file, 'w') as f:
        f.write(output)


# Pagination
page = 1
for start in range(0, len(all_words), PER_PAGE):
    words = all_words[start:start + PER_PAGE]

    for word in words:
        template = template_env.get_template(WORD_TEMPLATE_FILE)
        output_file = 'r/words/%s.html' % word["filename"]
        output = template.render(version=version, sets=sets, **word)
        with open(output_file, 'w') as f:
            f.write(output)

    pagination = Pagination(page, PER_PAGE, len(all_words))

    template = template_env.get_template(WORDS_TEMPLATE_FILE)
    output = template.render(words=words, version=version, pagination=pagination, **gs)
    if page == 1:
        with open('index.html', 'w') as f: f.write(output)

    if not os.path.exists('r/page/%s/' % page):
        os.mkdir('r/page/%s/' % page)

    with open('r/page/%s/index.html' % page, 'w') as f: f.write(output)
    page = page + 1


template = template_env.get_template('links.html')
output = template.render(**gs)
with open('r/links.html', 'w') as f: f.write(output)

template = template_env.get_template('sets.html')
output = template.render(**gs)
with open('r/sets.html', 'w') as f: f.write(output)

exit()
# rss.xml
template = template_env.get_template(RSS_TEMPLATE_FILE)
output = template.render(words=all_words, **gs)
with open('rss.xml', 'w') as f: f.write(output)

# sitemap.xml
template = template_env.get_template(SITEMAP_TEMPLATE_FILE)
output = template.render(words=all_words, **gs)
with open('sitemap.xml', 'w') as f: f.write(output)

template = template_env.get_template('sets.html')
output = template.render(sets=sets, **gs)
with open('sets.html', 'w') as f: f.write(output)


template = template_env.get_template('donation.html')
output = template.render(**gs)
with open('donation.html', 'w') as f: f.write(output)

template = template_env.get_template('tweet.html')
output = template.render(**gs)
with open('tweet.html', 'w') as f: f.write(output)

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
