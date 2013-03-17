from glob import glob
import codecs, re, shutil, sys, yaml
from markdown import markdown
from functools import *

from mako.lookup import TemplateLookup

def load_all(dir):
    return {fn[len(dir)+1:] : file(fn, 'r').read() for fn in glob(dir + '/*')}

class Benjen(object):
    def __init__(self):
        self.lookup = TemplateLookup(directories=['templates'])

        self.config = yaml.load(file('config.yaml'))

        self.out = self.config['path']
        if self.out[-1] != '/':
            self.out += '/'
        shutil.rmtree(self.out, ignore_errors=True)
        shutil.copytree('static', self.out)

        self.load_entries()

        self.generate_indexes()
        map(self.generate_post, self.entries)

    def render(self, name, **kwargs):
        return self.lookup.get_template('/' + name + '.html').render(**kwargs)

    title_sub = partial(re.compile(r'[^a-zA-Z0-9_\-]').sub, '_')
    def load_entries(self):
        raw = load_all('entries')

        self.entries = []
        for entry in raw.values():
            entry = entry.decode('utf-8')
            title = None
            date = None
            while True:
                if not entry or entry[0] != '#':
                    break
                line, entry = entry.split('\n', 1)
                type, rest = line[1:].split(' ', 1)
                if type == 'title':
                    title = rest
                elif type == 'date':
                    date = rest
                else:
                    assert False

            print title

            fn = date + '_' + self.title_sub(title) + '.html'
            self.entries.append(dict(
                title=title,
                date=date,
                raw=entry,
                html=markdown(entry, extensions=['codehilite(guess_lang=False)']),
                link=fn
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

def main():
    Benjen(*sys.argv[1:])

if __name__=='__main__':
    main()
