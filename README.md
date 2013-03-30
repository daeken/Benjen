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

	title: Entry Title Goes Here
	date: YYYY-MM-DD

Date must be in the YYYY-MM-DD form; however, you can optionally append '.X' to the end of the date, to signify which post it is in a given day.  **Note**: This format has changed as of v1.2, from the `#title` and `#date` format.  The included 'benjen-upgrade' utility will, when run from within your blog root (or given the path to the root), automatically update your entries from <=1.1 to the new format.

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
- root_url -- Root URL for your blog
- rss_title -- (Optional) Title for your blog for RSS; without this, your RSS feed will not be generated
- rss_description -- (Optional) Description for your blog for RSS.

Git Hook
--------

If you want to generate your blog automatically on your server when you push updates, you can set up a Git repo and hook to do this.

Basic steps:

- On your server, initialize a bare repository
	- `mkdir barerepo && cd barerepo`
	- `git init --bare`
- Push your blog to that git repository (see [http://git-scm.com/book/en/Git-on-the-Server-Setting-Up-the-Server](http://git-scm.com/book/en/Git-on-the-Server-Setting-Up-the-Server) if you need more info than that)
- Again on your server, clone the bare repository
	- `git clone barerepo realrepo`

Once you've done this, you need to add a file called post-receive to barerepo/hooks/ and make it executable.
Sample hook:

	#!/bin/bash
	unset GIT_DIR
	cd /path/to/realrepo/blog/directory/
	git pull origin master
	benjen

When you push to the server's repository, it will automatically pull the latest contents into realrepo and then run Benjen.
Make sure you change the repository names/paths accordingly.

That's all!
-----------

If you have issues, contact me at [cody.brocious@gmail.com](mailto:cody.brocious@gmail.com) or use Github's issue tracker.
