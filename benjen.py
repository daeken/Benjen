#!/usr/bin/env python

from glob import glob
import codecs, datetime, re, shutil, sys, yaml
from markdown import Markdown
from functools import partial
from mako.lookup import TemplateLookup
from PyRSS2Gen import RSS2, RSSItem, Guid

trailing_slash = lambda x: x if x.endswith('/') else x+'/'

class Benjen(object):
    def __init__(self):
        self.lookup = TemplateLookup(directories=['templates'])

        self.config = yaml.load(file('config.yaml'))
        self.root_url = trailing_slash(self.config['root_url'])
        self.out = trailing_slash(self.config['path'])
        shutil.rmtree(self.out, ignore_errors=True)
        shutil.copytree('static', self.out)

        self.load_entries()
        self.generate_indexes()
        map(self.generate_post, self.entries)
        self.generate_rss()
    
    def render(self, name, **kwargs):
        return self.lookup.get_template('/' + name + '.html').render(**kwargs)

    title_sub = partial(re.compile(r'[^a-zA-Z0-9_\-]').sub, '_')
    def load_entries(self):
        md = Markdown(extensions=['codehilite(guess_lang=False)', 'meta'])
        raw = (file(fn, 'r').read().decode('utf-8') for fn in glob('entries/*'))

        self.entries = []
        for entry in raw:
            html, meta = md.convert(entry), md.Meta
            if 'title' not in meta or 'date' not in meta:
                continue
            title, date = meta['title'][0], meta['date'][0]
            print 'Processed', title

            self.entries.append(dict(
                title=title,
                date=date,
                raw=entry,
                html=html,
                link=date + '_' + self.title_sub(title) + '.html'
            ))

        self.entries.sort(lambda a, b: cmp(b['date'], a['date']))

    def generate_indexes(self):
        per = self.config['per_page']
        recent = self.entries[:self.config['recent_posts']]
        genFn = lambda i: 'index.html' if i == 0 else 'index_%i.html' % (i / per)
        for i in xrange(0, len(self.entries), per):
            with codecs.open(self.out + genFn(i), 'w', 'utf-8') as fp:
                fp.write(self.render('index',
                    page=(i / per) + 1,
                    pages=(len(self.entries) + per - 1) / per,
                    prev=None if i == 0 else genFn(i - per),
                    next=None if i + per >= len(self.entries) else genFn(i + per),
                    posts=self.entries[i:i+per],
                    recent_posts=recent
                ))

        with codecs.open(self.out + 'archive.html', 'w', 'utf-8') as fp:
            fp.write(self.render('archive', posts=self.entries))

    def generate_post(self, post):
        with codecs.open(self.out + post['link'], 'w', 'utf-8') as fp:
            fp.write(self.render('post', post=post))

    def generate_rss(self):
        if 'rss_title' not in self.config or 'rss_description' not in self.config:
            return
        RSS2(
            title=self.config['rss_title'], 
            link=self.root_url, 
            description=self.config['rss_description'], 
            lastBuildDate=datetime.datetime.now(), 
            items=[
                RSSItem(
                    title=entry['title'], 
                    link=self.root_url + entry['link'], 
                    description=entry['html'], 
                    guid=Guid(self.root_url + entry['link']), 
                    pubDate=datetime.datetime.strptime(entry['date'][:10], '%Y-%m-%d')
                ) for entry in self.entries
            ]
        ).write_xml(file(self.out + 'feed.xml', 'wb'), encoding='utf-8')

def main():
    Benjen()

if __name__=='__main__':
    Benjen()
