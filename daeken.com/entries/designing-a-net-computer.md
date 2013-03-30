title: Designing a .NET Computer
date: 2009-11-19

Developing Renraku has led me to some interesting thoughts, not the least of which is the feasibility of a .NET computer.

# Concept

Existing computers know only a few core things:

*   Move to/from memory and registers
*   Branch
*   Perform arithmetic

All the other smarts are built on top of that, leaving us with layer upon layer of complexity. What if we were to add some logic to the hardware and introduce a thin software layer on top of that?

# Design

## CPU

The CPU will execute raw CIL blobs and exposes hardware interfaces and interrupts. The most likely route is to keep the stack in a large on-die cache, doing a small lookahead in decoding to prevent multiple stack hits in arithmetic.

Since the CPU is going to be executing CIL directly, it's going to have to deal with object initialization, virtual method lookups, array allocation, memory manager, and many other tasks that existing systems handle purely in software. This is achieved by splitting the task between the CPU and a hypervisor.

## Hypervisor

The hypervisor, like everything else, will be built completely in managed code. However, it will be a raw blob of CIL, instead of the normal PE container. The hypervisor will handle most of the high-level tasks in general, but it's up to the specific hardware manufacturer to determine what goes in the CPU and what goes in the hypervisor. The hypervisor will come up when the machine is booted, much like a BIOS. After performing hardware initialization, it will look for the bootloader.

The hypervisor provides a standardized interface to talk to drivers and memory, which are verified. In this interface, it will also provide hooks for the memory manager, allowing the OS to handle it in a nice way. Interrupts will also be hooked via this interface. The hypervisor instance will be passed to the bootloader, which then passes it on to the OS.

## Bootloader

The bootloader is a standard .NET binary, and its job is simply to hand control off to the OS. Its function is effectively identical to that of a bootloader on an existing system.

## OS

The OS will look very similar to existing managed OSes, with a few exceptions. Obviously, there's no need to write your own .NET implementation, and no need to write a compiler.

Because it exclusively talks through the hypervisor interface, it's possible to nest OSes as deep as you want, you simply have to expose your own mock hypervisor. You can handle resource arbitration here and run them very efficiently.

Unlike most OSes, it won't get free reign over the system. To access devices, it'll have to use verified channels with the hypervisor, to ensure that consistency is upheld. This is similar to the way that Singularity functions.

# Is it a good idea?

Maybe, maybe not. I don't know how efficient a CIL chip would be or how much of the .NET framework can really be pushed onto a chip, but the core idea is really an extension of Renraku. A pure-managed system would be very powerful if done properly, but it's a pretty drastic change.

A nice middle ground would be utilizing an existing processor and using the hypervisor in place of the existing BIOS/EFI. With some code caching magic, the CIL->X compilation could be done at this level and be completely transparent to the OS. This may well be a better route than a CIL CPU, but it's tough without having more information on the hardware challenges involved with such a thing.

Happy hacking,   
- Cody Brocious (Daeken)
