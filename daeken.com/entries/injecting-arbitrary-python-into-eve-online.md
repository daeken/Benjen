title: Injecting Arbitrary Python Into EVE Online
date: 2009-09-23

I finally broke down and installed EVE Online and registered for a trial, since quite a few of my friends have been talking about it nonstop. Being the dork I am, I looked through the binaries that were installed, and I immediately noticed that they shipped Stackless Python 2.5 as a separate binary (python25.dll). Of course, this led me to an investigation of what I could accomplish with respect to modifying the client without actually patching any code. A few hours later, I was able to run any Python code inside of EVE. 
All of the code is available from the Github repository here: 

# Injector

First, you have to get some sort of code into the game process. My favorite tool for this stuff is [EasyHook][1], as it lets you inject .NET code into processes. 
EasyHook, as the name implies, is very easy. You don't even need to hook anything here, just get some code running in the process. With a simple boilerplate NAnt build file and the source of an earlier hooking project, it only takes a few minutes to strip it down to what we need. EveInjector.cs finds the 'exefile' process for EVE and reads the given Python file into a string. It then uses RemoteHooking to inject EIInject.dll into the process. 
In EIInject.boo, you can see what exactly is going on. In the Run method, the following are called: Py\_Initialize, PyRun\_SimpleString, and RemoteHooking.WakeUpProcess. The Initialize call should've already happened, but this prevents the client from crashing if the injection happens very early in the load process. The PyRun call runs the code you gave, and the WakeUpProcess call causes the EVE process to come back to life, although it never seems to actually go to sleep. 
We now have control over the EVE process.

 [1]: http://www.codeplex.com/easyhook

# Logging

If you notice, there's a LogServer.exe binary in the EVE directory. This will display all sorts of interesting information from the EVE client. We need to be able to write to this. 
In my early experimentation, I noticed that traceback.print_exc() would go to the log server, so it was clear that stderr was tied to the log. By doing the following, you can print to the log directly: ` import sys sys.stdout = sys.stderr `

# Modules from compiled.code

All Python code in the client is Stackless Python bytecode and split up into a few files: lib/corelib.ccp, lib/corestdlib.ccp, lib/evelib.ccp, script/compiled.code. You can read about the details of these files on the [EVEmu Wiki][2] if you want to play with them. Anyway, the compiled.code file holds the bulk of the game code, but if you inspect sys.modules, you won't see anything from there. That's because it's handled by the 'nasty' module in libccp. 
To expose these modules to sys.modules (and thus make it easy to import them): ` import sys import nasty for key, value in nasty.nasty.mods.items():  sys.modules[key] = value `

 [2]: http://wiki.evemu-project.co.cc/eveFileFormats

# Services

In the 'svc' module, you can see all the service classes available on the client, but you can't directly instantiate any of them. Instead, you have to use the 'eve' instance. The 'eve' instance is the center of everything, client-wise. To get to services: ` from eve import eve gameui = eve.LocalSvc('gameui') ` 
You can see the methods available in the gameui instance via the svc module: ` from svc import gameui print dir(gameui) `

# Future

From here, getting to the bytecode of the functions is fairly easy, so it'd be nice to have an in-process decompiler that dumps the code of all modules, without having to mess around with the files directly. There are also a large number of bugs in the current injector, which I think stem from this code running in another thread from the normal Python interpreter. I'm fairly sure there's some way to acquire the GIL for the duration of the injected code running, which should fix it. 
All that said, I think there's some fun stuff that can be done with this. From here, it wouldn't take a huge amount of work to build something akin to Macroquest, where you can extend the UI, automate tasks, and generally make life better inside the client. With some tweaking, it's possible to make this fairly difficult to detect, but I'd be careful using this on an account you really care about early on. 
Happy Hacking,  
- Cody Brocious (Daeken)
