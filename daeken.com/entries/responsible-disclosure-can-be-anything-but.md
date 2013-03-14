#title Responsible Disclosure Can Be Anything But
#date 2012-12-06

The last few weeks were full of mixed emotions for me. Reliable reports of [hotel break-ins][1] seemingly utilizing the vulnerability [I disclosed at BlackHat][2] are coming out, and I'm both horrified and vindicated.

 [1]: http://www.forbes.com/sites/andygreenberg/2012/11/26/security-flaw-in-common-keycard-locks-exploited-in-string-of-hotel-room-break-ins/
 [2]: http://daeken.com/blackhat-paper

As I explained in my paper, the decision to release this information in the way I did was not an easy one. I've been full of doubt ever since I first made the call, and while I was inclined to think I did the right thing, I really couldn't tell for sure. But now, my doubt is gone.

Ever since the first story broke about these issues, I've taken significant flak from the security community and others for my lack of adherence to Responsible Disclosure. Hopefully this post will show that that's not always the responsible approach.

# Background

When I set out to reverse-engineer the Onity HT system, my goal wasn't to examine or undermine its security at all. Rather, the goal was to understand how it works and create a replacement for the Onity front desk system (primarily the encoder that makes the keycards). In the course of developing that, I found the vulnerabilities but didn't think much about them for a while.

In 2010, we (the startup I was running with friends at the time, UPM) decided to license the opening technology to a locksmithing company for law enforcement purposes. Quite honestly, I don't know what I can or can't say beyond that, due to contracts; at some point I'll be able to talk more openly about it.

# Going Public

In 2012, we decided that it was time to make these vulnerabilities public, but we were unsure how.

## Concerns

These were the characteristics of the vulnerability that were considered when weighing the release:

### Severity and Impact

The vulnerability itself, in a vacuum, is quite severe. Any Onity HT lock can be opened in less than a second with a piece of hardware costing effectively nothing. The hardware can be built by someone with no special skills for only a few dollars and utilized with no real 'training'.

Combine this with the fact that there are 4-10 million of these locks (Onity's own estimates -- my guess is that this is locks in use versus locks shipped) in use protecting people for 20 years now, and you have the perfect storm.

### Mitigation

Since the locks are not flashable, the only real way to fix them is to either prevent access to the jack (a non-solution) or replace the circuit boards in the locks. Either way, you're talking tens of millions of dollars to fix all the locks. Neither the individual hotels -- primarily independently owned with very low margins -- nor Onity can afford this.

### Ease of Discovery

The major vulnerability (the memory read) is trivial to discover -- it's used as part of the normal operations of the lock. That combined with the time these locks have been on the market gave me a strong feeling that I was not the first to discover it. In fact, it's blindingly obvious to anyone looking at the way the lock's communication functions that this vulnerability would be present; how did Onity not know of it?

I've since heard from various people that someone inside of Onity may have built an opening device themselves at one point, but I can't confirm that, let alone that it operated on the same principles as mine.

## Release Scenarios

### Contact Onity

The standard 'Responsible Disclosure' approach would be to notify Onity and give them X months to deal with the issue before taking it public. While this is tried and true, there are several issues with this approach.

Onity, after 20 years and 4-10M locks, has a vested interest in this information not getting out, as it makes them look bad and costs them a significant amount of money. As such, it's likely that without public pressure -- which we've seen in the form of unrelenting press coverage -- they would have attempted to cover this up. Cases of security researchers being sued by vendors are well known in the industry and not uncommon.

Due to the difficulty in mitigating the issue, it's entirely possible that only a tiny fraction of hotels would've been fixed by the publication deadline, and without such a deadline applying pressure, there's no reason for Onity to continue to make strides to fix the issue.

### Don't Release

This was a genuine option for a long while. While it's likely that it's been discovered and exploited long before I even looked at these locks, it was not a well-known attack.

However, I decided that the long-term benefits of this being fixed outweighed the problems certain to be faced in the short term while the flaws were being mitigated.

### Full Public Disclosure

The last approach is to simply release all information to the public in the most visible way possible. This dramatically increases the odds that someone will use the attack for malicious purposes, which is why it was always a big concern for me.

However, by making it as visible as possible, it puts significant pressure on Onity and the hospitality industry as a whole to fix the issues and get hotel guests back to a safe position. At the end of the day, this seemed like the approach most likely to get a swift response to the problem.

# Priorities

The key problem with Responsible Disclosure -- aside from the implication that any other means of disclosing vulnerabilities is irresponsible -- is that it puts the focus on security researchers' responsibility to vendors rather than customers. In most cases, the vendor of a vulnerable product is not the victim of attacks against that product, which makes this focus misguided in many cases.

In the case of the Onity vulnerabilities, the vendor (Onity) is not the victim, and neither are the hotel owners (Onity's customers). In this case, the hotel's customers are the true victims. While hotels or Onity could be liable in certain cases as a result of these vulnerabilities, hotel guests are the ones with their property and lives on the line.

Putting the focus on responsibility to the vendor, as nice a situation as it may be for vendors in many cases, can leave the true victims in a dangerous spot.

The focus for security researchers should *always* be on the customers, not the vendor; this is what Responsible Disclosure gets wrong. While it's true that in the majority of cases -- especially when dealing with software -- the quickest way to make customers safe is to work with the vendor to fix the issue, Responsible Disclosure advocates tend to ignore the edge cases in favor of a dogmatic adherence to this method.

# When Is Responsible Disclosure Irresponsible?

This is a hard one, as Responsible Disclosure is *usually* the best approach and knowing when it falls short is tough. In general, I'd say that if the majority of the conditions below are met, Responsible Disclosure might not be the best way to minimize customer risk:

*   The product is widespread (note: in-house software almost always immediately merits Responsible Disclosure)
*   A fix for the vulnerability/vulnerabilities is costly or difficult to implement
*   The risk to customers is severe 
    *   This must not simply be the vulnerability's rating, but the risk rating weighted with the impact to customers and the payoff for malicious actors
*   The likelihood of independent discovery is high
*   Replication of the attack requires little skill relative to the payoff of exploitation
*   The vendor is likely to have severe damage to their reputation or customer base as a result of the vulnerability becoming public knowledge

In cases where all or most of these are met, Responsible Disclosure may not be a responsible approach and may lead to customers remaining insecure and unsafe for years to come.

# Response

The response to the Onity HT vulnerabilities has been bigger than I ever thought it would be. The press has been unrelenting for months -- it was even featured on the Today Show this morning (December 6th, 2012), more than 4 months since the original release.

Onity has been vague on how and when they're fixing the issue. In August they published a plan for mitigating the flaws, which I [responded to][3]; Forbes picked up on this and Onity subsequently removed all trace of this plan from their site. They are now [stating][4] that they are paying for/heavily subsidizing their fix, only after months of battering from the press.

 [3]: http://daeken.com/onitys-plan-to-mitigate-hotel-lock-hack
 [4]: http://www.forbes.com/sites/andygreenberg/2012/12/06/lock-firm-onity-starts-to-shell-out-for-security-fixes-to-hotels-hackable-locks/

This would never have happened without public pressure; hotel guests would have remained vulnerable for a long time, rather than a few months. When all is said and done, disclosing this fully and publicly will have lead to increased safety for hotel guests the world over.

# Takeaway

Cases like this are never easy. In fact, it downright sucks to have to go through this with a vulnerability that could cause severe harm to customers. But at the end of the day, you have to decide one thing: is the customer more important than the vendor? In most cases, I'd say that they are.

The world is not black and white, and a dogmatic adherence to Responsible Disclosure makes us less secure and less safe as a whole. I urge all security researchers to think long and hard about how to disclose vulnerabilities, for the sake of everyone impacted, not just the vendor.

Happy Hacking,   
- Cody Brocious (Daeken)
