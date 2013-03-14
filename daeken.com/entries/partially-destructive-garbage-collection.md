#title Partially Destructive Garbage Collection
#date 2009-07-02

While lying in bed and trying to sleep last night, I had an idea I'd 
like some feedback on. The idea is partially destructive garbage 
collection, which allows the runtime to handle caching, instead of the 
programmer. With PDGC, the runtime is allowed to destroy an object 
and keep only the relevant data for recreation around. If you're 
running a photo management application, for instance, you may want to 
keep JPEGs and thumbnail bitmaps in memory, while not keeping the full 
bitmap around. In theory, this is a problem that PDGC can solve for 
you. 
 
At compile-time, the compiler can look at your class and determine 
whether or not your object's creation has side-effects, or depends on 
factors outside of its control (e.g. IO), and make a determination if 
it's partially destroyable. If it is, then the compiler embeds code 
into the constructor (and other relevant methods*) to save the data 
needed to recreate the object. At run-time, the frequency of access, 
object creation time, etc will be tracked, and the PDGC can make the 
decision to destroy the object or keep it around. If the object is 
destroyed, it doesn't entirely go away; rather, it's replaced with a 
stand-in object that stores the relevant data for recreation. 
 
Further ideas:

* You could allow the PDGC to only destroy certain object properties, rather than the full object
* A more general approach to language-level caching would allow the objects to be saved to disk and loaded lazily. This is something I plan to explore as part of my Renraku research kernel, the details of which I'll be posting on soon.


 
General open questions:

* What research has been done on this previously? What were the findings?
* How much of this belongs in the compiler and how much in the runtime? This obviously comes down to the implementation, but I believe there needs to be research into good, general approaches.


 
Implementation questions:

* Should this be involved with the GC at all? In my mind, they're related, but in a specific implementation they may well be completely separated.
* What factors are used in determining whether or not an object persists? Factors I can think of are: frequency of access, cost of object recreation, size, amount of free memory, amount of free swap space.
* Should this be behind-the-scenes compiler magic, or should it be more user controllable? E.g. should the user be able to decide if an object is destroyable at a given point? Should the user be able to override the object recreation portion, rather than letting the constructor do its thing?


 
I'd love to hear your take on it.

Happy Hacking,  
- Cody Brocious (Daeken)
