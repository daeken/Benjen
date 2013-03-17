Benjen
======

Benjen is a tiny static blog generator.  At its heart is a <100 line Python script, which takes in your templates and blog entries and produces a static site.

Installation
------------

    easy_install benjen

Usage
-----

From within a blog directory, simply run `benjen` and your site's output will be in the directory specified in your config file.

Creating a new blog
-------------------

Create a new directory with the following structure:

- yourblog/
  - entries/
  - static/
  - templates/
  - config.yaml

The `entries` directory contains all your blog entries as [Markdown](http://daringfireball.net/projects/markdown/) files.
These should, however, contain the following lines at the beginning:

	#title Entry Title Goes Here
	#date YYYY-MM-DD

The `templates` directory contains [Mako templates](http://www.makotemplates.org/).  There are three templates in use, with the following parameters passed in.

- index.html -- Used for index pages
	- page -- Current page number
	- pages -- Total number of pages
	- prev -- `None` or filename to the previous page
	- next -- `None` or filename to the next page
	- posts -- List of post objects for this page
	- recent_posts -- List of the most recent posts
- post.html
	- post -- Current post object
- archive.html
	- posts -- List of all posts

Post objects are dicts containing the following values:

- title -- Entry title
- date -- Entry date
- raw -- Markdown text
- html -- HTML version
- link -- Filename for the post

The `static` directory contains any static data to copy into the output path.  This is where you'll want to put your CSS.  Note: the Markdown output will be using Pygments for [code highlighting](http://pythonhosted.org/Markdown/extensions/code_hilite.html), so you'll need to add the appropriate CSS rules for it (see also: [https://github.com/richleland/pygments-css](https://github.com/richleland/pygments-css)).

The `config.yaml` file describes a dict with the following values:

- path -- Path for Benjen to output files (this can be absolute or relative from the blog directory)
- per_page -- How many posts to show per index page
- recent_posts -- How many elements to put in the recent_posts list for index pages

That's all!
-----------

If you have issues, contact me at [mailto:cody.brocious@gmail.com](cody.brocious@gmail.com) or use Github's issue tracker.
