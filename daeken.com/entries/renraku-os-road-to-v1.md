#title Renraku OS: Road to v1
#date 2010-01-23

# 

Renraku has seen a renewed surge of energy in the past few weeks, and has made big strides. Here's what's going on.

# Where we are

Renraku now runs in hosted mode on top of MS.NET/Mono. This enables a much, much quicker development/debugging cycle, and allows us to start working on the GUI while the low level details are still being worked out. There's still work to be done here, but it's a good start. We've also made the leap to Rake from NAnt; dealing with the bulky, inflexible build files just got to be too much. A few hours of hacking and Rake now fits our purposes perfectly.

After hosted mode came up, we made a push to get video/mouse services built on top of SDL, enabling us to start developing the GUI. You can see an initial GUI coming up and displaying our logo here: [![Media_httpdldropboxco_jixvb][2]][2] 

 []: http://getfile2.posterous.com/getfile/files.posterous.com/daeken/FvbyctonlgtijpcHdJrrwIopBlumGohGFnHsdejqGprhnGJlFenzeuGDrFBt/media_httpdldropboxco_Jixvb.png.scaled1000.png

In addition, Capsules (check out this blog post if you don't know what this is: [Renraku OS: Networking, Hosted Mode, Moving Forward][2]) are in progress and are taking shape; the implementation is still rapidly changing, but we seem to have a solid idea of what they're supposed to look like and how they interact with each other.

 [2]: http://daeken.com/renraku-os-networking-hosted-mode-moving-forw

# Where we're going

The project is now moving in parallel on two efforts: Userspace (GUI, applications, storage), and native (kernel, compiler, drivers). This will all converge over the next 6 months.

We're aiming to make two releases between now and July 4th, which will serve to get the code in the hands of developers leading up to v1.0. We now have a solid roadmap for Renraku v1.0, which we aim to release on July 4th, the one-year aniversary of the project. The roadmap is as follows:

## Goal

The project goal is that v1.0 should go out on July 4, 2010. This marks the first anniversary of the project and will be the first major release.

## What should it do?

You should be able to start Renraku in hosted or native mode (IA32 native only) and bring up a usable GUI. You should be able to browse files, start applications, edit configuration, and run UI tests. Depending on time constraints, we may or may not have additional applications (and a game?)

## What needs to be done?

Compiler:

*   Exceptions
*   Generics
*   Array bounds checking
*   Emit proper class data for reflection

Gui:

*   Basic toolkit for controls
*   Image rendering
*   Font rendering
*   Vector support?

Graphical shell:

*   Window management
*   Desktop icons
*   Some sort of system tray/menu

Kernel:

*   Tracebacks on exceptions
*   Garbage collection
*   Memory management
*   Storage 
    *   Low level storage service (hard drive access)
    *   FAT32 filesystem service
*   Networking 
    *   TCP
    *   IP and UDP supporting fragmenting
    *   More robust DHCP
    *   DNS
    *   Routing
    *   Transparent object remoting
*   Video driver on IA32 (better than VGA)

Services:

*   Capsule implementation
*   Service documentation

BCL:

*   Migrate to Mono BCL
*   Implement more of the BCL, if migrating to the Mono BCL isn't possible/practical

Applications:

*   GUI console
*   File browser
*   Basic text editor
*   Image viewer
*   Some basic GUI game?

Build System:

*   Allow portions of the code to be tagged as platform-specific, rather than the large file lists in the Rakefile
*   Integrate building a LiveCD with a complete Renraku system.
*   Build Renraku installer (XXX: May get pushed back to v2)

# How you can get involved

At this point, we need a few things: Application developers, service developers, kernel developers, and compiler developers. Want to write the first Doom port to run on a managed OS, a Twitter client, a completely new web browser, or a sane networking stack? Here's your chance.

No matter how you want to help out, or if you just want to ask some questions, join us at [#renraku on Freenode IRC][3].

 [3]: irc://irc.freenode.net/renraku

Points of contact:

*   Daeken (Cody Brocious, ) -- Kernel lead; Kernel, services.
*   ircubic (Daniel Bruce, ) -- Userspace lead; GUI, applications, storage. Documentation lead. Build system.
*   nrr (Nathaniel Reindl, ) -- BCL lead. Memory management lead.
*   dublindan (Daniel Kersten, ) -- Capsule lead.

Happy Hacking,   
- Cody Brocious (Daeken)
