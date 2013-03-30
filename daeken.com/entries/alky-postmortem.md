title: Alky Postmortem
date: 2009-12-27

A lot of people have asked me what happened to the Alky project. The short answer is that we made a lot of bad business moves, but that answer glances over a lot of the fun little details. Having gained considerable knowledge from other stories of failed startups, I figure I'll throw one of my own into the ring.

# History

The Alky project's history can be split into a few phases:

## Conception

Alky began as an experiment to see how easily I could convert Windows PE files to run natively on Mac OS X (x86). If it were to work, it may make it possible for me to convert Windows games to run natively on OS X, which was my primary focus. I started by writing a converter that ripped the segments out of the original file and throw them into a Mach-O binary, then linking it against 'libalky'.

LibAlky was a reimplementation of the Win32 API. At first, I tested with files that just called a few simple things, like user32:MessageBoxA, and it worked spectacularly. It was at this point that I realized the basic concept was not only sound, it made a whole lot of sense.

## Actual project creation

Once the initial prototype worked, it was time to get people interested. I went to Michael Robertson (who was my employer at the time) and gave him a rundown. He offered to buy the domain, host the project, and get some resources behind it, primarily PR-wise. Within a few days, the project started actually feeling real. We got the site up, wrote some copy to explain what we were doing, and then put it out on Slashdot.

Unsurprisingly, we received three types of responses:

1.  This is impossible, it simply can't work from a technical point of view. (This was especially hilarious coming from a Transitive engineer, considering that what they did is considerably more complicated.)
2.  This is possible, but it won't happen due to the immense amount of work involved. (Half right -- more on this later.)
3.  Wine sucks, I hope you guys can do it better. (We couldn't -- more on this later.)

But more importantly than anything else, we got some developers involved. However, they ended up being driven away.

## Mismanagement of the open source project

Alky was the first open source project I'd ever managed that consisted of more than myself and a few friends, and as a result it was mismanaged at every possible turn. It was unclear what people should've been working on, no effort was made to document the project, and no real effort was made to include the developers that were so interested in working on the project.

This was compounded by a rewrite and redesign, which I decided (foolishly) to take on entirely by myself. Some of the design was done as a group, but none of it ever left my hard drive, so work stalled on the existing codebase and the project started to wither.

Shortly thereafter, Falling Leaf Systems was incorporated to back the development of Alky. This further increased the rift between the open source developers and the "core" group (consisting of myself and one of the cofounders of the company). Originally, we planned to dual-license the codebase, but as we got more into discussions of the goals of the business, it became clear that closing the source was the right move. However, we couldn't have picked a poorer way to do it.

Rather than be upfront about the move to closing the source, we simply killed the IRC channel and took down the site. The open source developers were left wondering what happened, while we moved on the rewrite.

## Prey and the Sapling Program

Alky was completely rewritten with the new design, and work quickly moved forward on getting the first game running. We released a converter for the demo of Prey (Mac OS X only at first), as part of our new Sapling Program. The Sapling Program was created as a way to get some upfront money for the company, so we could get needed hardware, go to the GDC (which was a horrendous waste of money, for the record), etc. We sold memberships for $50, which gained access to the Prey converter and all future converters. Of course, after we finished Prey for Linux, there were no more converters.

## Loss of focus

After Prey was done, we'd planned on implementing DirectX 9 with hopes of running Oblivion, but we lost sight of this goal. Instead, we decided to go after DirectX 10. Along with this shift in focus came an even bigger one: we were no longer targeting Mac OS X and Linux primarily, but Windows XP. We saw that Vista was tanking, and DirectX 10 was only available there, so we decided that we only had a limited window to make money off of that.

Shortly after we made the change, we released a library to allow a few of the DX10 SDK demos to run on Windows XP via OpenGL, albeit with serious missing features (e.g. no shaders). It got some attention, but few people were able to actually get it working. After this was out, I started work on reverse-engineering the shader format and writing a recompiler that would allow Direct3D 10 shaders to work with OpenGL, and even more importantly, without DX10-class hardware. Geometry shaders were planned to run on the CPU if the hardware wasn't available to handle it, and work progressed quickly.

## Alky for Applications

We discovered a project known as VAIO to allow Vista applications (non-DX10) to run on Windows XP, and after some talks with the developers, they (or more specifically, one of them -- we'll call him Joe) were sucked into Falling Leaf. We rebranded VAIO and it was released as Alky for Applications. After this, Joe was tasked with making Halo 2 and Shadowrun -- Vista-exclusive but non-DX10 games -- run on Windows XP. We were so confident in our ability to do this, we set up an Amazon referral system and made it such that anyone who purchased either game through us would get a copy of the converter for free.

At this point, I was working heavily on DX10 stuff, and was under tight deadlines to show things off to a company that was interested in our technology, but the clock was ticking. About a week before the planned release of the Halo 2 and Shadowrun compatibility system, Joe came to us and told us that he'd not been able to get anything working, and had very little to show for the time spent. In retrospect, it was my fault for not checking up on him (my job as his manager), but at that point it just made me realize there was no way it was going to be done in time.

I picked it up -- dropping DX10 in the process -- and attempted, feebly, to get it done. Of course, I picked the most difficult way to approach it; reverse-engineering the Windows application compatibility system. By the time I got anything remotely close to working, we'd already missed our deadlines for both the DX10 work and the Halo 2/Shadowrun converter.

## The death of Falling Leaf

After all this went down, I fell into a bit of a depression. I became demoralized to the point of just not wanting to go on anymore, in the face of repeated failures, very much in public. Despite us not walking away with a dime -- we made approximately $7000 in total, none of which went to any of the founders of the company -- I felt that we'd ripped people off, despite the best of intentions. It wasn't long after this that Brian (one of my co-founders) stepped down as CEO, and I closed the doors on the company. The source to Alky and Philosopher (the compiler framework used in the shader work) were released at the same time.

# Lessons Learned

1.  If you're going to run an open source project, make it easy for people to contribute. Not only that, make it worthwhile for them to contribute and make them a part of the project, not just free workers.
2.  If you're going to kill an open source project, be up front with the people involved. It's not only dishonest not to do so, you lose people who may well go to bat for you even if you are commercial. This is especially important for a project like Alky, where we faced nearly universal negativity.
3.  If you're going to change focus, be clear with your users as to what's going on, and make sure you make it clear that the old stuff is dead and gone. If you don't, you come off looking terrible in the press, and it just makes you look like amateurs (which we were).
4.  Make sure your employees are actually doing what they're supposed to be doing, especially if they're working remotely. This was really the final nail in the coffin for Falling Leaf.

# Alky Reborn

Now, with all of that said, there's a light at the end of the tunnel perhaps. The source for Alky has been pulled into [Github][1] and it seems that development is picking up again. Perhaps I can shed some light into what design decisions were made, how it was implemented, and how I'd do it now if I were so inclined. I don't plan on working on Alky again (that time has passed), but I'd still love to see it succeed.

 [1]: http://github.com/callen/Alky-Reborn

## The old Alky design

Alky's original prototype had a very simple design, library-wise. There was one big LibAlky which contained all of the Win32 API implementations, each talking directly to native APIs. This design very quickly became unworkable, as we had tons of duplicated, unmaintainable code.

## The new Alky design

Alky was redesigned such that we had the Nucleus and the Win32 APIs. The Nucleus was intended to abstract away the platform-specific details and expose a universal API that the Win32 APIs could sit on cleanly. While a good idea, it quickly broke down in implementation. I ended up writing code that straddled the Nucleus and the Linux/OS X APIs, rather than abstracting everything away. This led to slower development and an even more complicated code base.

## Potential new design

Having done two implementations of Alky and quite a few other projects that relate to it in concept (IronBabel, Renraku (OS design plays a factor here), etc), I think I'm at a place where I can perhaps come up with a workable design.

The key point where both Alky implementations (and Wine, IMHO) failed is in maintainability. The codebase was a rats nest, much like the real Win32 APIs, and neither implementation managed to help this at all. I think this needs to be the absolute top priority, above performance, compatibility, and all else. If your code is maintainable, all the rest can happen.

With that focus in mind, here are the things I'd do with a new design.

*   Implement the APIs on top of Mono, taking advantage of the flexible marshalling that P/Invoke gives you. This will allow you to simplify things greatly, and will only have a marginal performance hit in most cases.
*   In cases where performance is critical, drop down and implement things in C, C , or assembly. If this chunk of the project is greater than 10% of the codebase, you've got bigger problems.
*   Abstract, abstract, abstract. Break things into the smallest chunks possible and reuse them. This is what we tried to do with the Nucleus idea, but it was easy to just ignore it for complex pieces.
*   Write thorough unit tests for every API that's implemented (public and internal). Regression testing would also make things really nice.
*   Rather than trying to get real games/applications running immediately, write your own simple applications that test specific chunks. This would've cut down considerably on the development time in the old revisions of Alky.
*   Write a great debugger to be able to step through applications cleanly. In the old days, I'd break out IDA Pro and step through a game on Windows, then compare the behavior to the Alkified version, but this was just downright painful.
*   Make it work on Windows, to allow easy side-by-side comparisons.

The suggestion that this should be built on top of Mono/.NET sounds ridiculous, I'm sure, but I do think it'd give the project a shot.

# In Closing

I hope this has given you some insight into what went down with Falling Leaf, some ideas of what not to do (obviously, it's easy to completely overlook these things when you're down in the trenches, as we did), and where Alky could one day go. I wish the Alky Reborn folks the best of luck, and I hope some of my advice helps.

Happy Hacking,   
- Cody Brocious (Daeken)
