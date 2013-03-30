#!/usr/bin/env python

from glob import glob
import codecs, os, sys

def main(path='.'):
	if not os.path.isdir('%s/entries' % path):
		if path == '.':
			print 'No `entries\' directory in the current directory. Are you in your blog root?'
		else:
			print 'No `entries\' directory in the indicated path (%s). Are you pointing to your blog root?' % path
		return 1

	for fn in glob('%s/entries/*.md' % path):
		with codecs.open(fn, 'r', 'utf-8') as fp:
			entry = fp.read()

		try:
			title, date, rest = entry.split('\n', 2)
		except:
			continue

		if not title.startswith('#title ') or not date.startswith('#date '):
			continue

		print 'Upgrading entry: %s (%s)' % (title[7:], fn.rsplit('/', 1)[1])
		with codecs.open(fn, 'w', 'utf-8') as fp:
			print >>fp, 'title:', title[7:]
			print >>fp, 'date:', date[6:]
			print >>fp, rest.rstrip('\n')

if __name__=='__main__':
	sys.exit(main(*sys.argv[1:]))
