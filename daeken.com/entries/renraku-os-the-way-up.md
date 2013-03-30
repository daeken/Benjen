title: Renraku OS: The Way Up
date: 2009-08-06

![][1]   
   
It's now been just over a month since this iteration of the Renraku   
project began. In that time, we've made monumental progress in   
effectively every way. We're up to 4 developers and a designer (see   
the pretty logo?), we've started to solidify the actual design of the   
codebase and how it's going to function in the future, and we're   
steadily pushing toward being a usable OS. We have a very long path   
ahead of us, but we're iterating quickly.   
   
Today, we're proud to announce the release of Renraku OS version 0.2   
alpha, codenamed "The Way Up".   
   
What's new:

 [1]: http://i30.tinypic.com/xo1ts8.jpg

*   Services – allow the interface to be decoupled from the implementation and provide a model for drivers, filesystems, network servers, etc.
*   Contexts – allow applications (Capsules, in Renraku terminology) to access services, and allows nesting such that you can run a Capsule in a sandbox where you provide filtered services, e.g. transparent proxying, nested windows, etc.
*   Mouse support – Renraku now supports PS/2 mice via a simple service interface.
*   VGA and general video interface – We can now use the latest in video technology (320x200 VGA, of course) in Renraku applications, even features double buffering. Progress is underway by one of our developers to build a basic GUI, but we have a few example apps.
*   BCL improvements – We've been gradually implementing various collections (ArrayList, Queue), text helpers (StringBuilder), and other pieces of the BCL, as we make the development process higher and higher level.
*   Compiler improvements – Inheritance, enums, interface implementation, method overloading, and many other things now work perfectly. There are now only a few key components (reflection and generics being the two big ones) missing before the compiler is effectively functionally complete.
*   Bootable ISO building – You can now build bootable ISOs along with the kernel image.
*   New apps to test out our new functionality: 
    *   'exclaim' – Example nested Context application, turning your '1's into '!'s by hooking the keyboard service. [Screenshot][2]
    *   'draw' – Simple bouncing box VGA demo. [Screenshot][3]
    *   'mouse' – Control a box cursor with your mouse, changing the colors with the click of a button. [Screenshot 1][4] [Screenshot 2][5]
    *   'logo' – Renders our logo in beautifully dithered 256 color VGA. [Screenshot][6]

 [2]: http://picasaweb.google.com/lh/photo/Un03CN2sHJXFXqHMTnFgUg?feat=directlink
 [3]: http://picasaweb.google.com/lh/photo/e0OPtDis4Z2WpSaEoAH7UA?feat=directlink
 [4]: http://picasaweb.google.com/lh/photo/0ED8e_GYY_oWKht5kLyvWA?feat=directlink
 [5]: http://picasaweb.google.com/lh/photo/3p-nTvKdyEJo5ZjkOnbqAA?feat=directlink
 [6]: http://picasaweb.google.com/lh/photo/cyzRtL-aHYqZ65Da1NRpnw?feat=directlink

  
   
You can get a [bootable ISO][7] or check out the [tree at Github][8]. We'd love to hear what you think; drop by our IRC   
channel, [#renraku on irc.freenode.net][9]. If you run into   
any bugs, feel free to throw them on our [issue tracker][10].   
   
You can also see the [complete screenshot gallery][11] as well as a few shots of Renraku [running on real hardware][12].   
   
We've had fun building it, I hope you have fun playing around with it.   
   
Happy Hacking,   
- Cody Brocious (Daeken)

 [7]: http://cloud.github.com/downloads/daeken/RenrakuOS/Renraku_v0_2a.iso
 [8]: http://github.com/daeken/RenrakuOS/tree/master
 [9]: irc://irc.freenode.net/renraku
 [10]: http://github.com/daeken/RenrakuOS/issues/#list
 [11]: http://picasaweb.google.com/cody.brocious/RenrakuV02alpha#
 [12]: http://picasaweb.google.com/nrreindl/Renraku#
