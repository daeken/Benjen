#title Renraku OS: Initial Release
#date 2009-07-17

![][1]   
   
The Renraku OS team is proud to announce the first release, 0.1alpha.   
Major strides have been made in the two weeks since the new codebase   
was started, and we're very happy with where things are.   
   
We now have:

 [1]: http://i30.tinypic.com/xo1ts8.jpg

*   Initial compiler with support for vtables, a good chunk of the CIL instruction set, string object constants, etc.
*   Initial memory manager (real memory manager is in progress).
*   Basic object manager.
*   The start of System.Array/String/Console.
*   Keyboard driver and US English keymap.
*   Basic shell that can execute applications.
*   Basic HAL and interfaces for timer, keyboard, and network drivers.
*   Initial PCI base class.
*   A few simple applications: 
    *   'echo' – Echo terminal
    *   'reverse' – Reverses the arguments passed to it
    *   'halstatus' – Prints the status of loaded drivers
    *   'pci' – Scans for PCI devices and dumps the vendor and device IDs
    *   'shell' – Creates a subshell

  
   
We've also created an IRC channel, [#renraku on Freenode][2] where   
the developers are generally available. If you want to give it a   
spin, grab the [kernel image][3] and boot it with GRUB. If you run into any problems, drop   
us a line on the channel.   
   
For the curious, you can check out this [gallery of screenshots][4] of the various commands. And as always, the   
codebase is on [Github][5].   
   
Give it a shot and let us know what you think.   
   
Happy hacking,   
- Cody Brocious

 [2]: irc://irc.freenode.net/renraku/
 [3]: http://cloud.github.com/downloads/daeken/RenrakuOS/Renraku_v0_1a.bin
 [4]: http://picasaweb.google.com/cody.brocious/RenrakuV01alpha#
 [5]: http://github.com/daeken/RenrakuOS/tree/master
