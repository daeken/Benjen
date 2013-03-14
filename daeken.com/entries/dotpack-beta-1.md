#title Dotpack Beta 1
#date 2010-04-09

# 

Edit: Due to a high troll rate on this post, I've temporarily disabled commenting.  If you'd like to leave feedback, please email me at cody.brocious@gmail.com or drop a comment on the Hacker News thread  .

I'm proud to announce the first beta of Dotpack, a packer for .NET executables. I've been working on this for the last week or so and finally have something fit for public eyes. It started out of my desire to build 64k demos on .NET and for that reason it's very small -- as of this writing, it's sitting at 5331 bytes overhead. It also achieves high compression ratios due to its use of LZMA; average size reduction for the files I've tested has been 60-80%.

At the moment it's fairly straightforward, not tampering with the original binary at all, but future versions will bring obfuscation and an array of code transformations to drop the filesize even further.

This version has several known issues I simply didn't have time to deal with: Silverlight packing is there (you can pass it a .xap and get one back), but it's very finicky and not particularly good so far. Packing binaries that use System.Reflection.Assembly.GetExecutingAssembly().Name will get back an empty string due to the way assemblies are loaded after unpacking, which can cause major issues. I'm going to fix these for the next release.

Other future features which will be coming, in no particular order:

*   Merging of assemblies. I was originally planning on releasing with ILmerge support as a stopgap until I finished my own prelinker, but licensing issues and a generally poor API made that less appealing. I'm working on a prelinker which, in addition to just merging assemblies, will perform dead code analysis to strip unused portions of the code away.
*   Obfuscation. Not only will this make it more difficult to analyze your binaries, but you'll get the benefit of less space being taken up by names. This can be quite substantial in a large binary.
*   Visual Studio integration. You'll be able to easily tie Dotpack into your Visual Studio workflow to produce packed binaries from your release builds.

Dotpack is freely distributable, but is under a non-commercial license. If you're using it in a commercial environment, even if you're not distributing your binaries, please purchase a commercial license. In addition to supporting Dotpack's development, you will also get builds ahead of the non-commercial users.

You can get the current beta build of Dotpack here: . To use it, simply run: `dotpack.exe input.exe/.xap output.exe/.xap` and you're off.

During the beta, a one-year single-user license is available at a discounted price of $250; once this goes gold, the price will go up to $500. Note that the year doesn't begin until the final release, so you're getting quite a deal. If you'd like to purchase a volume license, please contact me at . (Before the final release, I plan on getting a site up, but you know what they say about minimum viable products.)

Try it out, let me know how it works for you, and let me know if there are any features you'd like to see.

Happy Hacking,   
- Cody Brocious (Daeken)
