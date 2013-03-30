title: Renraku OS: Networking, Hosted Mode, Moving Forward
date: 2009-11-19

There hasn't been any news on Renraku in a while, so I figured I'd throw up an update on what's going on.

# Where we are

Not a whole lot has changed since the last post. We have a clear direction on where we're moving and we're making progress, albeit more slowly than in the first few months.

The biggest new thing is networking. We have Ethernet, IP, UDP, DHCP, and ARP, although the IP and UDP implementations still need some love. We also have a driver for the AMD PCnet card used in VMware, so testing is fairly easy.

Outside of this, most of the work has been in design, where we're solidifying the way the system works.

# Where we're going

## Hosted mode

Renraku is soon going to be able to run on top of any existing .NET implementation, allowing considerably simpler development and debugging. The primary goal with hosted mode is to allow developers to tackle higher-level tasks (GUI work, filesystems, etc) while our .NET implementation, kernel, and drivers are built.

When you have a hosted Renraku kernel, you'll run the kernel like any other application, then all of Renraku's services will start up just like on the bare metal. At that point, you'll be able to run other applications inside it, with the benefit of the drivers being dealt with by the underlying OS. This should significantly lower the barrier to entry to hacking on Renraku, while making our code considerably better.

To achieve this, we're splitting Renraku into several pieces:

*   Compiler
*   Kernel
*   .NET Base Class Library
*   Services
*   Applications

When we do this, we need to split platform-specific details away from the rest of the code. Hosted mode will just be another platform to the OS, so this also gives us much-needed platform independence. (This will make it possible to write targets for ARM, x64, etc in the near future -- more on this soon.)

In hosted mode, certain services will run as-is, but others will talk to the host OS. For networking, a driver will be implemented that uses raw sockets, utilizing our stack above it. For storage, we can create a virtual disk in a file. For video and input (and sound, eventually), we'll likely backend to SDL.

Whenever possible, we'll use more Renraku services (e.g. not just implementing the 'tcp' service as a wrapper around the .NET TCP classes), which will keep the code from fragmenting too much.

## Utilizing Mono's BCL

In the early days of Renraku, I pushed hard against the idea of using Mono's BCL, preferring that we write our own. While I'd like to go with our own BCL that's tightly tied to the Renraku kernel, cracks are quickly appearing in that idea. With us launching our hosted mode initiative, it's clear that the BCL needs to be separated as much as possible. At this point, it's starting to look like going with a modified Mono BCL may be the best route; at the very least, it's worth investigating.

This is simpler than writing our own BCL of course, but it's no trivial task itself. Integrating it with the Renraku kernel is going to be tough; most likely, the right way to do it is to strip the BCL down to the core components that we use and implement now, then move up from there. The other big challenge is compiler support; we currently don't support exceptions and several other things that the BCL uses heavily.

Regardless of the difficulty, this may well prove to be the right way for us to go. Hopefully it will work out, as it'll accelerate Renraku's development significantly.

## Capsules

Capsules are our answer to the application and process concept in most OSes. A Capsule holds running tasks, connected events, and the service context. When a Capsule starts, its main class is initialized, which will set up services, throw up a GUI, or whatever. Unlike a process on most OSes, a Capsule does not have to have a thread (task) running at all times, acting much like TSRs did in the old days. Once initialization is completed, the main task can die off, leaving all its delegates and services up. Because of the design of the system, most Capsules will not have a main task, leading to a more nimble system.

The strength of Capsules is most apparant with a GUI or networking app. In a GUI, the main task will put up the GUI and connect events, then die off. When an event occurs, the GUI service calls the Capsule's delegate, which spawns a task inside the Capsule to deal with it.

A network service will work similarly, dying off after it registers itself, waking up only to accept a new client, then it'll wake up when communication happens. This makes writing network applications very, very simple and efficient.

One outstanding problem is how to handle a Capsule being force killed. We need to handle this in a way that guarantees that the system remains consistent, which is tough. Anyone have a proof debunking the halting problem?

## Formal design documents

Currently the Renraku documentation is, to put it nicely, sparse. Code isn't commented at all and there's no documentation on how anything works. I've started writing real design docs, which will go live on this blog over the coming weeks. Here are the primary documents that are being worked on:

*   Capsule architecture
*   Input chain of command (how input gets from the hardware to the right place)
*   Storage architecture
*   Networking
*   Graphics
*   Compiler
*   Security

Capsules will definitely be the first to go out, as it's the most important (it blocks the most other elements of the system); the order on the rest is up in the air.

# Closing notes

The work I've done on Renraku OS so far has been some of my best and certainly some of the most rewarding. I'd like to thank everyone who's contributed or just cheered on the team. Even if this never takes off (the likelihood is quite small), Renraku will be an OS we can all be proud of, because of you guys.

Happy hacking,   
- Cody Brocious (Daeken)
