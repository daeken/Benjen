#title Benjen v1
#date 2013-03-17

I've just released the first version of [my new blog engine](https://github.com/daeken/Benjen) -- powering this site! -- for public consumption.
It's a super simple Python script, allowing for a huge amount of customization without so much as touching the actual blog engine.

This was built in response to Posterous' announcement to shut down, which I had been using for this blog previously.

How it works
============

At its heart is [92 lines of Python code](https://github.com/daeken/Benjen/blob/master/benjen.py) which reads in entries from your blog directory, splits them into index pages, and runs everything through Mako templates that you provide.

This all enables a lot of flexibility and power, despite that it can fit on a single sheet of paper.

Example
=======

You can see this blog on Github here: [daeken/benjen](https://github.com/daeken/Benjen/tree/master/daeken.com)

Next Steps
==========

I'm hoping to package this nicely as a git post-receive hook, so that you can just push your blog to a repository and have it automatically rebuilt on the server.
(**Update**: This is now done and documented in the README.)

If anyone has other ideas, shoot me an email and let me know: [cody.brocious@gmail.com](mailto:cody.brocious@gmail.com)

Happy Hacking,  
- Cody Brocious (Daeken)
