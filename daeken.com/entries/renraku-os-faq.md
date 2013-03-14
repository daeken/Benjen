#title Renraku OS: FAQ
#date 2009-11-19

This is the current Renraku OS FAQ. If you have a question that's not answered here, feel free to join us in #renraku on irc.freenode.net.

## What is Renraku OS?

Renraku is a pure managed code operating system, written in Boo from the ground up. The goal is to produce a high-quality operating system without the traditional security, performance, and flexibility issues.

## Is Renraku open source?

Yes, Renraku is distributed under the CDDL (Common Development and Distribution License).

## Why not use X in place of .NET?

The .NET infrastructure is fairly simple, powerful, (very) easy to compile, and flexible enough for our purposes. Another tool may be better suited to the task, but we've found it to be a good match.

## Why use Boo instead of C#?

Although C# is the more traditional choice for .NET work, it lacks macros and is simply much more verbose. Boo is very easy to pick up and significantly more powerful. However, our choice of Boo doesn't mean that the rest of the OS has to be written in Boo. Services, Capsules, and drivers can all be written in any .NET language.

## Is it POSIX compatible?

No, by design. POSIX was great in 1989, but times have changed and we need to move forward.

## What about legacy applications?

Virtualization is the only planned route for legacy code at the moment, as it's the most efficient and lowest cost. Perhaps we'll support running certain types of legacy applications in a more direct route in the future, but it's doubtful.

## Won't this be slow?

For a while, yes. However, compilers are rapidly getting considerably better and compilers like Microsoft's Bartok are paving the way toward faster code. In addition, our lack of separate address spaces and privilege levels make system calls and task switches dramatically cheaper than on existing OSes.

## No separate address spaces? What keeps applications apart?

Because we use pure managed code, we're guaranteed that applications cannot touch memory they aren't directly given. This means that the compiler has the last word on all memory access in the code, reducing the attack surface of the OS considerably.

## Does it run X?

Unless the application you have in mind is playing with our shell, looking at our logo, or acquiring an IP address via DHCP, probably not. Renraku is still in its infancy, but we hope it'll be useful someday.
