title: Distributed Balance
date: 2013-02-21

So, I've been quiet for long enough and it's time to discuss my plan. I've long said that we need a revolution, but that I didn't know the form in which it would come; I know that now. This is Distributed Balance.

# Background

Despite their major flaws, we've seen the edges of the revolution for years -- forces pushing us to transparency: Wikileaks, Anonymous, etc. But the inherent problem is that we have a tiny portion of society helping out with these things; only a tiny portion has the skills to gain access to confidential documents or works in roles where that sort of access is possible. At the same time, we're in a position where we have so much data that it's impossible to catalogue and index it all.

In addition, centralized organizations such as Wikileaks are an inherent bottleneck when it comes to document releases, making it difficult for information to propagate effectively. This does, however, have the benefit of allowing them to redact names and the like from documents; whether this is desirable/acceptable to you may vary. Aside from that, it's very easy to strangle such an organization -- the US government has done so very effectively by cutting off their donations. This is not an acceptable risk.

# What's Next

I'm designing a next-generation platform for distributing, indexing, and tagging large data dumps. Because the nature of such data may be objectionable to many, the platform is being designed with the assumption that it will be under constant attack legally, technologically, socially, and economically; it must defend against all of these points.

To this end, I'm going to discuss each of the design decisions and their purpose separately.

## Federated

The system is designed to be inherently federated. By this, I mean that there will never be a central system containing data, receiving leaks, or hosting content. Rather, anyone will be able to set up a system to connect to the network, anyone will be able to add or tag documents, and anyone can publicly host the content.

This solves a few problems at once:

*   No centralized choke point for leaks. Since anyone can push content into the system, it makes it significantly harder to track who is leaking what.
*   The cost of distributing the content is spread out over a large number of hosts, rather than a single organization; this means that even if donations were sought out, it'd be far harder to shut down all of those payment endpoints. That said, because of the distributed nature, it's unlikely that any one host will end up with costs that are too high.
*   It becomes far easier for innovative thinkers to build new interfaces to data.

## Web of Trust

Because of the federated nature of the system, some trust protocol needs to exist; without it, anyone could poison the well by distributing illegal and off-topic content. As such, the design calls for each system to be linked to others and given trust ratings. The exact meaning of these trust ratings is still up in the air, but the concept is straightforward:

*   Trust is ranked for each peer 
    *   How much you trust what they're adding
    *   How much you trust what they're deleting
    *   How much you trust what they're tagging/annotating
*   Trust is transitive, e.g.: 
    *   There are three peers, A B C, with A connected to B, B connected to C
    *   Peer A trusts peer B 50%
    *   Peer B trusts peer C 75%
    *   Because of the transitive trust, this means that A trusts C 37.5% (50% of 75%)

Details on this are still very much in the air.

## Volunteer Mobilization

As mentioned earlier, part of the goal is to get volunteers involved. Right now there are a lot of people willing to sign petitions and all that, but what if we took that energy and got people actually organizing data?

In the first incarnation, volunteers will simply go to a node and receive a random document. They'll read through it and tag it appropriately, to the best of their abilities. One thought is that a short questionnaire might be the best way to go, with the tags being derived from those answers; the questionnaire would simply be written ahead of time by the leak uploaders, to make it situationally appropriate.

Getting volunteers to share documents and rope others into helping catagorize documents would be a big, big win for the platform; this is something that really hasn't been seen before. The people are there, they just need something to do, whether for 5 minutes or a week.

## Search Engine

Journalists in particular have expressed the difficulties they have with dealing with the massive troves of information released by the likes of Wikileaks. As Google can tell you, organizing data into a form that people can drill down into to find what they want is very, very important. As such, everything in the system will be full-text searchable, as well as being able to filter by tags and things like that.

The technology for this is fairly straightforward, especially when you're talking about searching individual leak troves; there's a lot of data for humans, but not for computers.

## Global Changelogs

To keep everything in check, we really need a system by which we can see all the changes across the system, at least for a few hops on the web of trust. This may not happen for v1, but this will be necessary as things scale up. Something akin to Wikipedia's vandalism bots would not go amiss here as well.

# Problems

Below are the problems I see at the moment:

*   How do we keep one node from becoming the canonical reference for the network? This will drive up costs for that node, make them a large target, and add a single point of failure for trust.
*   How do we stop things like music, movies, and pornography from being stored on the network? The purpose is not general file-sharing, but specifically document storage and indexing.
*   How do nodes find each other? One idea that has been bounced around is using IRC to match up nodes.
*   How do we stop rogue nodes from flooding the network? One way is to use trust ratings to determine how big a change a given node can make in a certain period of time.

# "Competition"

Services like Freenet enable people to publish and share documents at the moment. However, due to the nature of the system: documents are immutable, searching isn't possible without pulling down the contents of the archive, and annotations have to be external.

The same tradeoffs exist when, say, publishing a torrent full of leaks. A federated system like this is complex, but it allows for these fundamental issues to be dealt with.

# Getting Involved

Simply put, things are very early stage. If you want to get involved, join #distributedbalance on irc.freenode.net. Design is underway, and bodies are needed.

There's also a [Github repo][1], primarily for tracking issues and designing in the wiki.

 [1]: https://github.com/daeken/DistributedBalance

Happy hacking,   
- Cody Brocious (Daeken)
