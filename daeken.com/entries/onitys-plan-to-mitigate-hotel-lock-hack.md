title: Onity's Plan To Mitigate Hotel Lock Hack
date: 2012-08-17

# Onity responds

On August 13th, 2012, Onity released their plan to mitigate the vulnerabilities in the Onity HT hotel lock line that I released at BlackHat this year. My previous post on the subject is available at .

Their statement is available at  and is reproduced below in case future edits are made:

> August 13, 2012 - This is an update to Onity's previous communications regarding the hacking of certain models of Onity hotel locks. We want to assure you that Onity is working on providing you with a solution that will address any potential risks related to the alleged vulnerability of these locks.
> 
> Onity is going to implement a two tiered approach. The first approach will include providing a mechanical cap, free of charge, to our customers, who have the Onity HT series locks. This mechanical cap will be inserted into the portable programmer plug of the HT series locks. With the existing battery cover in place the mechanical cap will not be removable without partial disassembly of the lock. This will prevent a device emulating a portable programmer from hacking the lock. To further enhance the security of this fix, we will also supply a security TORX screw with each mechanical cap to further secure the battery cover in the lock. This solution is currently going to production, and should be ready for deployment starting the end of August. The second solution Onity will offer to our customers, if they choose to use this option, is to upgrade the firmware of the HT and ADVANCE series locks. The firmware is currently complete for the HT24 lock, and by early next week should be complete for the entire HT series of locks. By the end of August we should have the firmware complete for the ADVANCE lock as well. The deployment of this second solution, for HT series locks, will involve replacement of the control board in the lock. For locks that have upgradable control boards, there may be a nominal fee. Shipping, handling and labor costs to install these boards will be the responsibility of the property owner. For locks that do not have upgradable control boards, special pricing programs have been put in place to help reduce the impact to upgrade the older model locks. If you are interested in pursuing this solution, have additional questions or require further information, please contact Onity at 1-800-924-1442. Thank you again for your business and your trust in Onity over the past many years of our relationship.
> 
> July 25, 2012 - At the Black Hat conference on Tuesday July 24, a hacker presented alleged vulnerabilities of certain models of Onity hotel locks.
> 
> The hacker showed an open-source hardware device that he built, which mimics a portable programming device. He claimed that by using this device a plug can be inserted into the locks’ DC port, which may result in opening the lock.
> 
> Onity understands the hacking methods to be unreliable, and complex to implement. However to alleviate any concerns, we are developing a firmware upgrade for the affected lock-type. The upgrade will be made available after thorough testing to address any potential security concerns that you may have.
> 
> Onity places the highest priority on the safety and security provided by its products.
> 
> For additional questions or for further information, please contact our office. See below for your nearest location.
> 
> Thank you for your continued business!

Before going further, I want to say this: Onity should get credit for responding to these issues and taking steps to mitigate them. This situation is not a simple one, and taking steps to secure their hardware could not have been easy.

However, I feel I must throw in my two cents on the mitigation plan as it stands, as I do have serious concerns.

# Physical security

Onity plans to provide a mechanical solution to the problem to all customers, in the form of a mechanical cover on the inside of the battery compartment. This cover will be mounted inside the battery compartment, covering the portable programmer port, and they plan to switch the screw on the battery panel with a TORX screw for added protection.

This -- as much as it *is* security-through-obscurity -- is actually a great temporary fix. Don't get me wrong, it will not take long at all to open the panel and use an opening device to pop the lock open, but it will raise the bar and make it more likely that the attacker is caught in the process.

However, I wonder how they're going to do this for the ADVANCE series locks; I don't have one handy, but as far as I can recall, the portable programmer port stands on its own and could not be covered up in this way -- they even say the HT locks are the only ones the cover is for. This seems to leave the ADVANCE lock owners (who are admittedly few) in the rain.

# "Firmware update"

In addition to the port cover, Onity is working on what they are calling a "firmware update" for the locks. This is where things get hairy.

## Not a firmware update

This is not really a security issue, but it *is* a credibility and honesty issue. I feel it's very deceptive to say to customers "we are preparing a firmware update" when you really mean that you're preparing a hardware update. They may be changing *the firmware* on the lock, but to make use of this, customers are required to replace the whole main circuit board.

This is equivalent to Apple telling customers "we're releasing a software solution for this issue" and then going on to say that they're doing it by replacing your laptop's motherboard.

## Issue mitigation

I have not seen nor tested the updated locks in any way, shape, or form; what follows here is speculation based on my knowledge of their system and the vulnerabilities in question, and what they announced in their statement above.

At BlackHat, I announced two vulnerabilities: an arbitrary memory read and initial work into their flawed cryptography for key cards. The important thing to keep in mind is that neither of these sit in isolation; the arbitrary memory read happens as part of the protocol between the portable programmer and the lock, and the crypto is flawed between the encoder and the lock.

As such, I cannot imagine a fix for both of these issues which does not consist of replacing not only the lock circuit boards, but that of the portable programmer and the encoder.

If the protocol on the lock is changed in any substantial way -- as would be needed to fix the arbitrary memory read -- then the portable programmer would no longer communicate with the lock, causing the system as a whole to fail to function. Likewise, the cryptography cannot be changed on the lock side without also changing it on the encoder side.

I would absolutely love to be wrong about the lock protocol issue; if they can fix this at the lock level alone, and fix it well, then the impact on customers will be lower and the chances of the issue being fixed are higher. However, I find this highly doubtful. It seems far more likely to me that they have mitigated this issue at the lock level simply by shifting data around in memory or something along those lines, which would serve to break existing opening devices but not hold up to even the slightest scrutiny.

# Responsibility

While it's great that Onity seems to be taking these issues seriously, the fact remains that such blatant vulnerabilities existed in their massively distributed product line for nearly a decade. As such, I believe that Onity has a greater responsibility to their customers than they are currently taking on.

## Fix cost

Onity plans to distribute the mechanical caps free of charge to HT customers, but the cost of fixing the actual vulnerabilities will fall to the customers. Even if this were to cost only $5 per lock (between the hardware itself, shipping, and installation), at 4-10 million locks in the wild that means a cost of $20-50MM to the hotel industry as a whole; this will not be insignificant, given that the majority of hotels are small and independently owned and operated. Given that it won't be a low cost endeavour, it's not hard to imagine that many hotels will choose not to properly fix the issues, leaving customers in danger; this is on top of those that will simply not have heard of the fix, if Onity does not contact all of their customers directly -- I do not know if they plan to do this or not.

If such a significant issue were to exist in a car, customers would likely expect a complete recall at the expense of the manufacturer. I can't help but feel that Onity has the same responsibility to their customers, and to customers staying in hotels protected by Onity locks. Whether they have such a responsibility from a legal point of view or not, I can't say; but from an ethical point of view I believe they do.

## Auditing

Releasing a fix for such a serious vulnerability without having the complete system (fix and all) audited by independent security professionals is merely asking for the issue to persist, or even new issues to come up. For the safety of hotel guests everywhere, Onity must have an audit performed; it's simply the only way to know that they aren't releasing another horribly vulnerable product onto the market.

This isn't a panacea -- things can and do slip by security audits every day -- but it's the best solution we have right now to at least catch the low hanging fruit, which I would very much consider the vulnerabilities announced to be.

# Closing

The plan announced is not perfect, but it's absolutely a step in the right direction. I look forward to seeing it put into action and hope that the issues I raised in this post will be addressed.

As always, Happy Hacking,   
- Cody Brocious (Daeken)
