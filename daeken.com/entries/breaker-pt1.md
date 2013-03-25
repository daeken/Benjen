#title So You Want To Be A Breaker, Pt. 1: Web Security
#date 2013-03-17.1

In my opinion, there's nothing more interesting and challenging than the security field.
When you come toe to toe with a particularly strong piece of software and you just *have* to break it, the only thing I can liken it to is a good game of Go.
Every time you make a move, your opponent -- the designers and developers, by proxy -- will respond in kind.
You know there's a way to win and it will take every part of your brain firing on all cylinders to find the weak link in the chain.

I live for the moment when I strike the right point and the whole system comes tumbling down.
You will too.

Preamble
========

The goal of this blog post is not to be comprehensive; in fact, the opposite is true.
My goal is to teach you enough about security -- specifically software security -- that you can go forward and learn the other parts on your own.
To ease in that learning, I've sprinkled links to resources throughout the post; Google is also very much your friend here, as there are a million resources out there for most of these topics.

Once you read the General section, you can jump to any of the others (including the other blog posts, as they come out) as you see fit as they're written independently.

This post is focusing on web security.  Posts on native security and crypto will be coming soon.

General
=======

Prerequisites
-------------

It's rather difficult to come up with a list of prereqs for security, simply due to the breadth of the field.
However, the following are the must-haves:

- Know how to program in one or more languages at a fair degree of competency (no one would expect you to edit a novel if you couldn't write the language yourself).  If native security is your interest, at least one of these languages must be low-level; C is best.
- Understand what a computer does and how it does it.  You don't need to be able to put together a CPU with tin cans and string, but you should be able to explain:
	- (Web) How HTML is parsed and how JS interacts with the page.
	- (Web) How HTTP works.
		- In fact, write a proxy.  You'll end up doing a lot of that. (This is actually important enough that I'll probably write a blog post about this one day.)
	- (Native) How pointers work, how the stack is laid out, what the heap is, and (for bonus points) how syscalls work.

Where needed, I'll talk about more specific prerequisites.

Mindset
-------

Before I can continue, I have to touch on the mindset of a breaker.
Your goal is not to preserve user interactions or the intended flow of data through a program.
Rather, your goal is to answer one simple question: Under what circumstances does this not do what it's intended to do?

Perhaps the best example of this is the cross-site scripting attack that's nearly everpresent in web apps; an attacker is able to output content to the page without proper filtering, allowing her to insert arbitrary HTML content and run scripts in the context of the page.
The normal flow is preserved -- the data makes it from the user to the page -- but because that data contains HTML, the page is completely compromised.

The difference between intended and real behavior is what you're looking for in every case, whether that's a standard bug as described in the next sections, or a logic flaw unique to the problem domain you're testing.

Web Security
============

Must-have Tools
---------------

Below is a list of tools that you should have in your arsenal.  Some of them are categories with more than one tool -- unless explicitly mentioned, they're roughly interchangable.

- HTTP(S) proxy -- This you will use constantly, as it will allow you to analyze and modify data in-flight
	- [Burp Proxy](http://portswigger.net/burp/proxy.html) -- Unless you have good reason not to, you should use this.  It's the industry standard and by far the shallowest learning curve.
	- [mitmproxy](http://mitmproxy.org/)
	- [Charles Proxy](http://www.charlesproxy.com/) (UI is terrible -- only use it for [AMF](http://en.wikipedia.org/wiki/Action_Message_Format))
- [DirBuster](https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project) -- Useful for finding 'hidden' files/directories
- [PadBuster](https://github.com/GDSSecurity/PadBuster) -- Useful for exploiting padding overflow vulnerabilities
- [Python](http://python.org/) or [Ruby](http://ruby-lang.org/) -- For general automation of tasks

Cross-Site Scripting (XSS)
--------------------------

XSS vulnerabilities are among the most common you'll see in web applications.
The concept is simple: data from an attacker is put into a page without proper filtering, allowing the attacker to execute code in the context of the page.

Reflected XSS is when data from an attacker (e.g. passed in the query string) is directly output on the page.
This is the most common form and is frequently used in conjunction with CSRF attacks (see next section).
They are protected against by default in many modern web frameworks.

Stored XSS is when data from an attacker is stored -- generally in the database -- and then output without filtering at a later point in time.
These are less common than Reflected XSS vulnerabilities but have a higher impact normally, due to the ease with which they can be used to target other users.
Like Reflected XSS, these are protected against by default in many modern web frameworks.

DOM-based XSS is when data is inserted by JavaScript on the browser side without filtering.
These are fairly uncommon but are not protected against by most web frameworks; they are becoming more common relative to the other forms of XSS vulnerabilities due to the protections afforded those.

In all cases, they are protected against by filtering user data before output, but it's important to encode for the right case.
For example, HTML encoding won't serve to protect anything if the data is being output inside of a script tag; in such cases, JS string output encoding is needed.

- [OWASP](https://www.owasp.org/index.php/Top_10_2010-A2-Cross-Site_Scripting_(XSS))
- [Wikipedia](http://en.wikipedia.org/wiki/Cross-site_scripting)

Cross-Site Request Forgery (CSRF)
---------------------------------

CSRF vulnerabilities are simple but highly effective and common.
The basic idea is that an attacker points the victim (automatically with a redirect, or manually with a simple link e.g. in an email) to a page on the target website.
The link to that page contains request data to perform an action, e.g. make a bank transaction.
To the server, this looks just like a legitimate request and it's performed as if the victim had done it themselves.

Protection against CSRF takes the form of random tokens that are put into the form bodies of pages and then submitted with each request; the server checks the token and ensures it's a match for the user's current random token in the session and rejects requests that don't match.
Most modern web frameworks have built-in CSRF protection but it remains a very common vulnerability.

- [OWASP](https://www.owasp.org/index.php/Top_10_2010-A5)
- [Wikipedia](http://en.wikipedia.org/wiki/Cross-site_request_forgery)

SQL Injection
-------------

SQL injection is, at this point, one of the most well-known and prevalent vulnerabilities present in web applications today.
The premise is that data from an attacker will end up being put into a SQL query without proper escaping.
This leads to the attacker being able to break out of a string (most commonly) and add their own code to the query.

Depending on the code and the database configuration, this can range from bad (blind injection allowing slow retrieval of data) to super critical (arbitrary code execution, file access, data destruction, etc).
Most modern frameworks are protected from this due to their use of an ORM; everything else should use parameterized queries where possible.
When a raw query with attacker data mixed in is the only route, proper escaping *must* be used.

- [OWASP](https://www.owasp.org/index.php/Top_10_2010-A1)
- [Wikipedia](http://en.wikipedia.org/wiki/SQL_injection)

Shell Injection
---------------

Shell injection is fairly uncommon but almost always critical when it happens.
When user data is fed into a shell command without filtering, it's possible -- through the use of backticks, semicolons, ampersands, etc -- to execute other commands at the same time.

Code calling out to a shell command using user data should always prefer execution methods where an array of arguments is provided (this is naturally immune), and use the appropriate shell escaping functions when raw command strings are built.

- [Wikipedia](http://en.wikipedia.org/wiki/Code_injection#Shell_injection)

Directory Traversal
-------------------

The most common forms of directory traversal are those where user data is directly used to construct a path to a file on the system.
Without proper filtering in such cases, it's possible to insert a reference to the ".." directory entry, to walk up the directory tree.
This can allow arbitrary reading/writing/deletion of files and is very frequently a critical vulnerability.

- [Wikipedia](http://en.wikipedia.org/wiki/Directory_traversal_attack)

Insufficient Authorization
--------------------------

Insufficient authorization refers to cases where access controls are not put on certain pieces of functionality or data.
A good example is a properly access-controlled administration console which has links to admin-only functions that do not have proper controls.

This is often seen in conjunction with forced browsing, in the case of improper controls on data.

- [OWASP](https://www.owasp.org/index.php/Top_10_2010-A8)

Forced Browsing
--------------

Forced browsing -- also known as direct object reference -- is a class of vulnerabilities where an implementation detail is exposed to users in a modifiable way.
Most commonly, this takes the form of an easily modifiable `id` parameter in requests, allowing an attacker to simply enumerate all possible identifiers to access/modify data.

- [OWASP](https://www.owasp.org/index.php/Top_10_2010-A4)

Others
------

The topics above are a great starting place and they're things that I see *constantly* in testing real-world applications.
However, the list is less than comprehensive, so here's a list of a bunch of other topics that you should read up on:

- [XML External Entity Injection (XXE)](https://www.owasp.org/index.php/XML_External_Entity_(XXE)_Processing)
- [Session Fixation](http://en.wikipedia.org/wiki/Session_fixation)
- [Unchecked Redirects](https://www.owasp.org/index.php/Top_10_2010-A10-Unvalidated_Redirects_and_Forwards)

Practice
========

I've recently been pointing everyone with an interest in websec to [Natas](http://www.overthewire.org/wargames/natas/).
That wargame will let you use a good number of the exploitation techniques mentioned in this article, and some more advanced techniques that I didn't mention here.
It also happens to be a whole lot of fun.

Other good resources include:

- [Stripe CTF 2.0](https://github.com/stripe-ctf/stripe-ctf-2.0/)
- OWASP's [WebGoat](https://www.owasp.org/index.php/Category:OWASP_WebGoat_Project) and [Vicnum](https://www.owasp.org/index.php/Category:OWASP_Vicnum_Project)
- Maven's [Web Security Dojo](http://www.mavensecurity.com/web_security_dojo/)
- [Peruggia](http://peruggia.sourceforge.net/)

Going Further
=============

Done practicing and want to dig your teeth into something real?
Well, many companies are now running bug bounty programs where you can not only legally test their software, but get paid for the bugs you find.
You can find a list of such programs [here](http://blog.bugcrowd.com/list-of-active-bug-bounty-programs/).

Happy hacking,  
- Cody Brocious (Daeken)
