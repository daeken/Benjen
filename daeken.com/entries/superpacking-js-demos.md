#title Superpacking JS Demos
#date 2011-08-31

# Background

The techniques I'm going to be describing here were created and/or implemented to pack my entry to the [Mozilla Demoparty][1]: [Magister][2]. Huge thanks to my friend Nicolás Alvarez for helping squeeze every last byte out of this.

 [1]: https://demoparty.mozillalabs.com/
 [2]: http://pouet.net/prod.php?which=57308

# Getting started

So you have a demo in JS. It's pretty. It's perfect. It's 3k in a 1k competition. Well, damn.

You start with the obvious and run it through a minifier and you shorten all your variable names to a single character, you get it to 2500 bytes. Great, that's progress, but you've still got 1476 bytes to go. You merge some functions together, fold a couple loops into each other, and soon you're at 2200 bytes. Long way to go.

Rule #1 of shrinking demos: removing a byte becomes more difficult every time you remove a byte. It starts off trivial and runs very quickly into a brick wall.

# Quick wins

These are a couple useful techniques to trim the fat at this point.

    var a = g.getAttribLocation(x, 'pos');
    g.uniform1f(g.getUniformLocation(x, 'time'), t);
    g.vertexAttribPointer(a, 2, g.FLOAT, 0, 0, 0);
    g.enableVertexAttribArray(a);

What's wrong with this picture? Well, if we ignore whitespace (minification takes care of that): we're using `var` (pfft, correctness), we have a shader attribute with a 3-byte name and a uniform with a 4-byte name, we're using g.FLOAT (more on this in a moment), and we've got a lot of zeros.

    g.vertexAttribPointer(
        a = g.getAttribLocation(x, 'p'), 
        2, 
        5126, 
        g.uniform1f(g.getUniformLocation(x, 't'), z), 
        0, 
        0
    )

Much better! We killed `var` removing 4 bytes, we removed 2 bytes by inlining the assignment to `a` in the first use and killing the semicolon, we eliminated a zero (the return of uniform1f is treated as a zero by the WebGL API in this case) and a semicolon for a savings of 2 bytes, we changed our shader attributes/uniforms to have 1-byte names (saving 5 bytes), and we inlined the FLOAT constant for a savings of 3 bytes. That's 16 bytes removed from a block of 151 (after whitespace removal), or a reduction by 10.59%! Let's do it again.

Before we move on, I just want to make a note that WebGL constants really are just that. You can inline them and trust them not to change.

# Abusing globals

Look at the latest code above. Count the instances of 'g.'. Four instances just in that tiny little snippet. If we could get rid of those in a small way, this could be a huge win, so let's do it.

What is the global namespace in JS? Normally, it comes from the `window` object. So when you call `foo()`, it's going to look in `window` if you haven't declared it locally. So why don't we shove our methods into the `window` object? Or even better, into `top` (in our case, they're identical)?

Right now the declaration of `g` is as such:

    g = z.getContext('experimental-webgl')

But let's change it to:

    for(k in g = z.getContext('experimental-webgl'))
        top[k] = g[k].bind && g[k].bind(g);

So we walk over every key in the WebGL context and put it into `top`, but only if it has the bind method and we can bind it to the WebGL context. Without that, it tries to treat the window as a WebGL context. The window doesn't like this.

At this point, we just cut all instances of 'g.' out of the picture. This was a win of around 30 bytes (counting the cost of the globalization code) in my demo's case, but we can go much, much further.

# What's in a name?

Let's look at a list of all the WebGL methods I called in my demo:

    attachShader
    createProgram
    linkProgram
    createBuffer
    bindBuffer
    bufferData
    viewport
    createShader
    shaderSource
    compileShader
    useProgram
    getAttribLocation
    getUniformLocation
    uniform1f
    uniform2f
    vertexAttribPointer
    enableVertexAttribArray
    drawArrays

Holy moly, that's a lot of bytes! But these are defined in WebGL, how can we change this?

Welllll... let's look back at our globalization code. We get a name, `k`, and then bind `g[k]` into `top[k]`. But we control what `k` goes into `top`. Having a map of long name into short name would be expensive, but what about a regex? I'm going to spare you the gory details, but after a while of tinkering with it, I determined that the optimal code for this is:

    t[k.slice(1, -5).replace(/[ntalruicoh]/ig, '')] = 
        t[k] = g[k].bind && g[k].bind(g);

In this case, `t` is `top` (because hey, 4 bytes!). We still assign the original name into `t`, but we also put the sliced and diced name into it. Why? Because this mangles two names we need to disambiguate: `uniform1f` and `uniform2f`. But that's fine.

So what do the names look like after this?

    S
    eeP
    kP
    eeB
    dB
    ffe
    e
    eeS
    deS
    mpeS
    seP
    eb
    efm
    f
    f
    eexbP
    beVeexb
    w

Night and day difference, as you can see. You'll obviously want to change the regex if you do this yourself, since your code will have different balances.

# Other random wins

Arrays of digits tend to be pretty wasteful:

    new Float32Array([0,0,2,0,0,2,2,0,2,2,0,2])

What about this instead?

    new Float32Array('002002202202'.split(''))

The more digits you have, the bigger the win from this replacement is. Until we get to compression and everything changes.

# Compression

Ok, we all know HTTP requests are trivially compressible, and this can improve load times and blah blah blah. Doesn't matter when it comes to demos: if the size on the wire is 1k and the size on disk is 3k, your demo is 3k.

In the past, people have compressed their demos into images. This is an easy way to get a good size reduction -- PNGs are just zlib'd data with a little header, basically. But these demos all had a PNG and an HTML JS file that would load the PNG, draw it to a canvas, pull the pixels out of the canvas as a string, and eval that string. How can you make this into a single file demo?

## Introduction to PNGs

The PNG file has an 8-byte signature followed by a series of simple chunks. The chunk format is as follows:

    4 byte length
    4 byte chunk type
    X byte chunk data
    4 byte CRC

Most of these are pretty clear, except chunk type. Chunk type is a FourCC, e.g. 'IHDR', which is mostly generic, with some exceptions which I'll talk about shortly.

I'm not going to go into detail on the IHDR chunk (we can't really mess with it, but I will say I use greyscale for simplicity purposes), but here's what we start with.

    8 byte signature
    13 byte IHDR with 12 byte chunk header
    X byte IDAT (covered below) with a 12 byte chunk header

The IDAT format is dead simple: 1 byte filtering method followed by your zlib deflated data.

## Abusing PNGs

We start by defining our own chunk type (we're allowed to do that!) before the IDAT chunk.

    4 byte length
    4 byte "jawh" (Just Another WebGL Hacker (TM))
    X byte bootstrap
    4 byte CRC

What is the bootstrap? Well, it's what turns our PNG into code and runs it. Here's the one I use:

    

The 4968 here is really the size of the decompressed data in bytes times 4 -- there are 4 components to each pixel (red, green, blue, alpha) but we're only using grayscale, so we need to offset that. If you look carefully, you'll also notice that it walks backwards across the data, which should create a string in reverse, but I compensate for that when I compress the data, and reverse it before doing so. This saves a couple bytes. The image source is also important: rather than hard-coding the image filename and wasting space, it uses `#`, enabling it to treat itself as a PNG.

So what do we have now? We have a PNG containing some HTML. The browser first opens it as HTML (file extension is important here), then sniffs the MIME type and figures out it's a PNG when it gets loaded into the image tag. We have a self-extracting PNG. But we can do better.

## Why specs don't matter

We're currently using a chunk type of "jawh". Clever and a nice little insider reference, but that's 4 wasted bytes! The chunk type comes right before the data, so why don't we make the chunk type into `<img` instead?

The spec says on the subject:

> Four bits of the type code, namely bit 5 (value 32) of each byte, are used 
> to convey chunk properties. This choice means that a human can read off the 
> assigned properties according to whether each letter of the type code is 
> uppercase (bit 5 is 0) or lowercase (bit 5 is 1). However, decoders should 
> test the properties of an unknown chunk by numerically testing the specified 
> bits; testing whether a character is uppercase or lowercase is inefficient, 
> and even incorrect if a locale-specific case definition is used.

It then goes on to tell you that bit 5 of each of the bytes is:

> First byte: 0 = critical, 1 = ancillary
> Second byte: 0 = public, 1 = private
> Third byte: reserved
> Fourth byte: 0 = unsafe to copy, 1 = safe to copy

Since we could call it `<iMg` or `<imG` or any other combination of uppercase and lowercase, clearly we only care about the impact of `<` on the first byte. But if we look at bit 5 of `<`, we see that it's already set high, so it's an ancillary chunk -- we're in the clear and just saved 4 bytes!

Wait, no, neither Chrome nor Firefox load the image anymore. What the hell? This is the point where you realize: the spec doesn't matter. No browser out there follows the PNG spec, whatsoever. Perfectly to-the-spec images won't work, and horribly broken images will work. So let's horribly break it. Note: Both Chrome and Firefox use libpng for image parsing, so you could go through the code and look for ways in which it's mishandling data and go down that path, but for my purposes I found that just experimentally changing things and seeing how they break was Good Enough (TM).

## Breaking PNG for fun and profit

Messing with the chunk type is out due to browser incompatibility, so what other options do we have? Well, who cares about CRCs.

Set the CRC to `c=#>`, save, refresh. Hey, it works in Chrome and Firefox! 4 bytes saved.

Well, we can't push back towards the front due to the chunk type, and we can't push forwards towards the `IDAT` chunk because of the size. But how do browsers handle chunk size mismatches?

If we set the size of the `IDAT` atom to `c=#>`, that unpacks to a size of 1042496867, which is obviously more than the size of the `IDAT` chunk. We shift `) sr` into the CRC and set the IDAT size to `c=#>`, save, refresh. All browsers will set `size = min(reportedSize, endOfFile - startOfChunk)`! That saves us another 4 bytes.

So sure, we couldn't get rid of `jawh`, but who cares? We just saved 8 bytes!

## Compression caveats

Now you know how to make the PNG container small, but this says nothing about actually making your demo small. A few of the tips above are actually harmful in the context of compression. Why? Because repetitive data compresses really, really well. For instance, the Float32Array trick is nice when you're dealing with uncompressed data, but ends up eating a couple extra bytes after compression. Reusing function and variable names is also very, very important. The more repetition you can introduce, the better off you'll generally be.

## Wrapping up

All in all, these tips (and general insanity) will let you build really small demos. My demo, Magister, went from around 3k down to just over 900 bytes when all was said and done. I ended up adding a message in the demo ("1k should be enough for anybody.") to get it up to exactly 1024 bytes, which was my goal. Feels good to have to work up rather than down.

I hope this helped shine some light on the subject.

Happy Hacking,  
- Cody Brocious (Daeken)