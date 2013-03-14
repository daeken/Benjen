#title Renraku OS: It Lives!
#date 2009-07-09

This is a follow-up to my previous post, [Renraku: Future OS][1].   
   
I got the latest incarnation of Renraku booting yesterday, based on the code base I started the same day I wrote the previous article. There's not much to it, but development is progressing very, very quickly since I have plenty of knowledge of what not to do from previous attempts. What's there (in the [GitHub repo][2]) now supports very basic functionality: multiple function compilation, a good number of "Base instructions" (from the ECMA CIL spec), static fields, pointer intrinsics, and string intrinsics (get_Chars for now).   
   
The test kernel is available [here (GitHub)][3] and this boots as expected. Obviously, it doesn't do much, but that's coming. What needs to be done in the short term:

 [1]: http://daeken.com/renraku-future-os
 [2]: http://github.com/daeken/RenrakuOS/tree/master
 [3]: http://github.com/daeken/RenrakuOS/blob/master/TestKernel/Main.boo

*   Struct support
*   Struct pointers
*   Basic object manager

  
   
That's it. Once those are done, there's a primitive object model which means actual functionality can be written. A few more days of work, and we should be able to see a simple shell come up.   
   
Happy Hacking,   
- Cody Brocious (Daeken)
