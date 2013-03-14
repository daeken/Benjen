#title Reversing The Pokerstars Protocol, Part 1: Compression and transport 	basics
#date 2009-08-19

Let me start with a little background. I got into poker botting after reading James Devlin's great series on [Coding The Wheel](http://www.codingthewheel.com/). I tried a few different attempts at the IO layer (hooking the poker client directly, screenscraping (wrote a cool little library), etc) before settling on hacking the protocol directly. However, I also started getting into actually playing poker heavily, and I realized a little while ago that there's no way this bot will be profitable (including my time) unless I throw years of work at it, so I've decided to release my knowledge publicly. I've not seen anyone reversing the PStars (or any other service, in fact) protocol publicly, so I'm hoping to help out there.

The likelihood of things staying the same after this is released is very slim, so for reference my work is being done on the latest client as of today, 8/19/09, version 3.1.5.8. All code is available on the [Github repo](http://github.com/daeken/PSReverse/tree/master), and I'll be doing code releases to correspond with the parts of this guide. This stuff will only work on Windows with Python 2.6 . 

First things first, we have to go into this with a game plan. We need to end up with a client, but what's the best way to get there, since we need to be able to adapt quickly to changes? I cut my teeth on server emulators for MMOs, and I've found that building a server can allow you to find changes quickly. However, we also need to be able to see traffic, so we need a way of sniffing and displaying traffic. Therefore, I think the best route is to build the following: an MITM proxy with a web interface for viewing packets, a server emulator, and a client library. 

Now that we have a plan, we can to dive right in. I made the assumption that everything was done over SSL, and quickly confirmed this with Wireshark. There's a lot of traffic and it indeed uses SSL. 

I decided to implement everything for Python 2.6, to take advantage of the *ssl* library. With this, I built a simple MITM to display traffic both ways. But here's the first snag: the PokerStars client checks the server's certificate. However, this was an easy fix. I generated a keypair for the MITM (can also be used for the server emulator) and found that they stored the normal server cert in plaintext in the client binary. A quick patch script later and the MITM works like a charm, dumping raw data. A quick look over, and it became clear that there's a static initialization field (42 bytes) at the beginning of both the server and client transmissions, and then packets sent with a 16-bit (big endian) size in front of them. 

Time to start looking at the client to figure out what it is. Breaking out my handy dandy IDA Pro and loading PokerStars into it, I started searching through the strings list for compression- and crypto-related strings. I stumbled upon a few interesting strings, the clearest of which was: "_CommCompressedCommunicator: LZHL frame is too long". Googling around a bit, I found that LZHL is a lightweight compression algorithm intended for high-performance network situations. 

Next stumbling block: the original implementation of LZHL has fallen off the Internet, and the only remaining implementation I can find is buried in a big, unmaintained library. Cue 2 days of attempting to reimplement the algorithm in Python with no actual verification that it is the only thing in play. For those of you playing the home game, this is a **Bad Idea**. After a day of debugging, I gave up and simply beat the C code into submission, utilizing the ctypes library in Python to wrap it into a usable form. 

Tying this into the MITM, I can now see the decompressed frames coming across the wire, complete with nice clean plaintext. However, there is a clear header on the packets, so that has to be reversed next. 

Here are some choice packets from the beginning of a connection:

    -> 106 bytes:
    0000 00 6a c1 06 00 00 38 33 60 10 02 69 70 3a 36 36| .j....83 `..ip:66
    0010 2e 32 31 32 2e 32 32 35 2e 31 37 3a 32 36 30 30| .212.225 .17:2600
    0020 32 00 41 6c 74 31 4c 6f 62 62 79 53 65 72 76 65| 2.Alt1Lo bbyServe
    0030 72 49 6e 73 74 61 6e 63 65 00 53 68 61 64 6f 77| rInstanc e.Shadow
    0040 54 6f 75 72 6e 61 6d 65 6e 74 73 50 75 62 6c 69| Tourname ntsPubli
    0050 73 68 65 72 30 00 00 00 00 00 00 00 00 00 00 00| sher0... ........
    0060 00 00 00 00 00 00 00 00 00 00                  | ........ ..

    <- 2048 bytes:
    0000 08 00 81 00 0d 6a 54 06 00 00 39 33 60 10 02 d7| .....jT. ..93`...
    0010 4e 7c e2 06 00 00 00 00 02 95 f3 10 30 00 00 1b| N|...... ....0... 
    0020 18 4a 72 d0 48 eb 65 b3 2d 00 00 00 00 00 02 00| .Jr.H.e. -....... 
    0030 00 00 00 01 02 95 f3 10 11 5b 00 00 e3 61 43 02| ........ .[...aC. 
    0040 8f fd 1b 00 02 ff 00 e3 61 44 00 e3 61 44 ff 00| ........ aD..aD.. 
    0050 00 00 85 0b 0b 60 df 69 70 3a 36 36 2e 32 31 32| .....`.i p:66.212 
    0060 2e 32 32 35 2e 31 37 3a 32 36 30 30 32 00 00 00| .225.17: 26002... 
    0070 00 00 00 00 00 00 00 00 00 00 06 e0 00 00 00 f0| ........ ........ 
    0080 00 00 00 00 00 00 80 32 30 20 50 4c 20 42 61 64| .......2 0.PL.Bad 
    0090 75 67 69 00 00 00 00 00 00 00 00 00 00 08 44 60| ugi..... ......D` 
    00a0 02 d0 01 00 02 00 00 00 03 00 00 00 10 ff ff ff| ........ ........ 
    00b0 ff 00 40 00 00 00 00 00 00 00 00 00 00 00 00 00| ..@..... ........ 
    00c0 00 00 00 00 00 00 00 00 08 00 00 00 00 00 00 09| ........ ........ 
    00d0 45 55 52 00 00 00 00 00 ff 00 e3 61 45 02 8f fd| EUR..... ...aE... 
    00e0 1b ff 00 00 00 08 00 00 01 80 00 00 00 01 00 00| ........ ........ 
    00f0 e3 61 46 02 71 f0 93 00 02 ff 00 e3 61 47 00 e3| .aF.q... ....aG.. 
    0100 61 47 ff 00 00 00 85 0b 0b 60 e0 69 70 3a 36 36| aG...... .`.ip:66 
    0110 2e 32 31 32 2e 32 32 35 2e 31 37 3a 32 36 30 30| .212.225 .17:2600 
    0120 32 00 00 00 00 00 00 00 00 00 00 00 00 00 0a 6e| 2....... .......n 
    0130 00 00 01 4a 00 00 00 00 00 00 80 33 30 20 50 4c| ...J.... ...30.PL 
    0140 20 42 61 64 75 67 69 00 00 00 00 00 00 00 00 00| .Badugi. ........ 
    0150 00 08 44 60 02 d0 01 00 02 00 00 00 03 00 00 00| ..D`.... ........ 
    --snip--

    <- 2048 bytes: 
    0000 08 00 01 06 44 00 02 d7 02 00 03 00 00 00 09 00| ....D... ........ 
    0010 00 00 10 ff ff ff ff 80 00 00 00 00 00 00 00 00| ........ ........ 
    0020 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00| ........ ........ 
    0030 00 00 00 00 00 09 45 55 52 00 00 00 00 04 ff 00| ......EU R....... 
    0040 e3 61 9f 02 7e 31 23 ff 00 00 00 08 00 00 01 80| .a..~1#. ........ 
    0050 00 00 00 00 00 00 e3 61 a3 02 8d 14 01 00 02 ff| .......a ........ 
    0060 00 e3 61 a4 00 e3 61 a4 ff 00 00 00 b5 0b 0b 61| ..a...a. .......a 
    0070 05 69 70 3a 36 36 2e 32 31 32 2e 32 32 35 2e 31| .ip:66.2 12.225.1 
    0080 37 3a 32 36 30 30 32 00 00 00 00 00 00 00 00 00| 7:26002. ........ 
    0090 00 00 00 00 24 40 00 00 02 d0 00 00 00 00 00 00| ....$@.. ........ 
    00a0 80 31 30 30 20 4e 4c 20 48 6f 6c 64 27 65 6d 20| .100.NL. Hold'em. 
    00b0 5b 48 65 61 64 73 2d 55 70 20 3c 62 3e 54 75 72| [Heads-U p.Tur...
    00c0 62 6f 3c 2f 62 3e 20 31 36 20 50 6c 61 79 65 72| bo.1.... 6.Player 
    00d0 73 5d 00 80 31 30 30 20 54 69 63 6b 65 74 00 00| s]..100. Ticket..
    --snip--

I've truncated two of these, because the actual data doesn't much 
matter here. First and foremost, look at the first two bytes of each 
packet. It's a 16-bit value corresponding to the packet size. At 
first, I believed they had the compressed size (outside) and 
decompressed size (inside) for verification purposes, but a little 
later I discovered that they'd combine packets where possible. A 
single compressed packet can contain multiple packets, and they'll 
push it up to the 65536 bytes before compression (no logic for 
combining more intelligently).

Next up comes a flags byte. This I determined by guess and check 
largely. The breakdown is:

- Flags & 0xC0 == 0x80: Beginning of a message chain. If the next byte is 0, there are 4 unknown bytes following.
- Flags & 0x40 == 0x40: End of a message chain.

If the flags byte is anything else, it's a message in the chain (if 
it's placed in a chain) or a self-standing message. From here, we'll 
refer to 'message' as the raw data inside the transport stream. That 
is, everything from the flags byte+1 (or +5, in the case of it being 
the start of a message chain and the flags+1 byte being 0 as indicated 
above) onward, including additional messages in the chain.

Looking at the messages, we'll see some repetition in byte 2. I 
guessed that this was the opcode field indicating the type of message, 
and some quick verification shows this is most likely the case. One 
other interesting thing is that there's an incrementing ID that is 
shared by the client and server. With a little detective work, you 
can see that if byte 1 is 0, the ID is from 3-7 (exclusive), otherwise 
it's 1-5. By looking at the plaintext that's sent, you can see that 
the ID is incremented by the client when creating a new request chain, 
and is used by both sides for the duration of that chain. For 
instance, you can see that the ID in the packets above is 0x33601002. 
You can also see that the second packet is a new chain and the third 
packet is a continuation (it's not the final packet).

Now that we have all this, a clear picture of the transport itself is 
beginning to form, but here's something unusual: most packets have the 
same opcodes. Lots of 0x38s, 0x11s, etc. This baffled me for a 
little while, before I went back and looked at the initial packets, 
where it was requesting 'server instances' and such. After this, a 
light clicked on in my head, and I realized that the entire PokerStars 
protocol is a series of client-server connections funneled through one 
of a long line of frontend load-balancing servers.

A little bit more digging around told me the following about these 
connections: (note the --> and -<- conventions for 
client->server and vice versa)

- -> 0x10: A sort of async method call, only used initially.
- -> 0x38: Establish a connection to a service provider, from which streaming lobby, tournament, table, etc data is received.
- <- 0x39: Response to a connection. Seems to have some sort of header with connection info before the data starts streaming in.

From this, I began to piece together the protocol and how the 
client/server could be implemented. I wrote a web-based protocol 
viewer and started pouring over logs.

In the [Github repo](http://github.com/daeken/PSReverse/tree/master) you'll find the following:

- LZHL: VC++ source tree, compiled dll, and Python wrapper.
- PSHooker and runpstars.bat: This is an application using my [Nethooker](http://www.assembla.com/wiki/show/nethooker) library to redirect the PokerStars connection to the MITM/emulator. You'll likely need to edit the binary path in runpstars.bat, and you need to add a HOSTS entry pointing 'pshack.com' to 127.0.0.1 to make it work.
- pmitm.py: This is the meat of the codebase. It writes out log.txt containing the raw packet data for consumption by the web interface and gives hex dumps of the packets over stdout.
- patchCerts.py: This patches the PokerStars binary to use the unofficial certs. Run with: python26 patchCerts.py path/to/PokerStars.exe path/to/newpokerstars.exe officialcert.pub mitmcert.pub
- WebPoker: Pylons project to view the packets. Edit WebPoker/webpoker/lib/Protocol.py to point it at the location of logs.txt from pmitm.

I hope this was clear and that you got something out of it. There's a 
lot more to rip apart, and I hope to give more (and better) examples 
in the future.

Thanks for reading, and happy hacking,  
- Cody Brocious (Daeken)
