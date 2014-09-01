#!/usr/bin/python2.7
#
# Copyright (c) 2014 deathspawn
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

# This was ported from a sex command from Linux. Not exactly sure where the source went.

# Import the necessary modules.
import random

# All the nice sex replies...
faster = "\"Let the games begin!\"", "\"Sweet Jesus!\"", "\"Not that!\"", "\"At last!\"", "\"Land o' Goshen!\"", "\"Is that all?\"", "\"Cheese it, the cops!\"", "\"I never dreamed it could be\"", "\"If I do, you won't respect me!\"", "\"Now!\"", "\"Open sesame!\"", "\"EMR!\"", "\"Again!\"", "\"Faster!\"", "\"Harder!\"", "\"Help!\"", "\"Fuck me harder!\"", "\"Is it in yet?\"", "\"You aren't my father!\"", "\"Doctor, that's not *my* shou\"", "\"No, no, do the goldfish!\"", "\"Holy Batmobile, Batman!\"", "\"He's dead, he's dead!\"","\"Take me, Robert!\"", "\"I'm a Republican!\"", "\"Put four fingers in!\"", "\"What a lover!\"", "\"Talk dirty, you pig!\"", "\"The ceiling needs painting,\"", "\"Suck harder!\"", "\"The animals will hear!\"", "\"Not in public!\""

said = "bellowed", "yelped", "croaked", "growled","panted", "moaned", "grunted","laughed","warbled", "sighed", "ejaculated", "choked", "stammered","wheezed","squealed", "whimpered","salivated","tongued", "cried","screamed", "yelled", "said"

the = "the"

fadj = "saucy","wanton", "unfortunate", "lust-crazed","nine-year-old","bull-dyke", "bisexual", "gorgeous", "sweet", "nymphomaniacal", "large-hipped", "freckled", "forty-five year old","white-haired", "large-boned", "saintly","blind","bearded", "blue-eyed","large tongued","friendly", "piano playing","ear licking","doe eyed", "sock sniffing","lesbian","hairy"

female = "baggage","hussy","woman", "Duchess","female impersonator","nymphomaniac", "virgin", "leather freak","home-coming queen", "defrocked nun","bisexual budgie","cheerleader", "office secretary", "sexual deviate", "DARPA contract monitor", "little matchgirl", "ceremonial penguin", "femme fatale", "bosses' daughter", "construction worker","sausage abuser", "secretary","Congressman's page", "grandmother", "penguin","German shepherd","stewardess", "waitress", "prostitute", "computer science group", "housewife"

asthe = "as the"

madjec = "thrashing","slurping", "insatiable", "rabid","satanic","corpulent", "nose-grooming","tripe-fondling", "dribbling", "spread-eagled","orally fixated", "vile", "awesomely endowed","handsome", "mush-brained", "tremendously hung","three-legged", "pile-driving", "cross-dressing", "gerbil buggering", "bung-hole stuffing", "sphincter licking","hair-pie chewing", "muff-diving", "clam shucking","egg-sucking","bicycle seat sniffing"

male = "rakehell", "hunchback","lecherous lickspittle", "archduke", "midget", "hired hand", "great Dane", "stallion", "donkey", "electric eel", "paraplegic pothead", "dirty old man", "faggot butler","friar","black-power advocate", "follicle fetishist", "handsome priest","chicken flicker", "homosexual flamingo","ex-celibate","drug sucker", "ex-woman", "construction worker","hair dresser", "dentist","judge","social worker"

diddled = "diddled","devoured", "fondled", "mouthed","tongued","lashed", "tweaked","violated", "defiled", "irrigated","penetrated", "ravished", "hammered", "bit","tongue slashed", "sucked", "fucked", "rubbed", "grudge fucked","masturbated with", "slurped"

her = "her"

titadj = "alabaster","pink-tipped","creamy", "rosebud","moist","throbbing", "juicy","heaving","straining", "mammoth","succulent","quivering", "rosey","globular", "varicose", "jiggling", "bloody", "tilted", "dribbling","oozing", "firm", "pendulous","muscular", "bovine"

knockers =  "globes", "melons", "mounds", "buds", "paps", "chubbies", "protuberances","treasures","buns", "bung", "vestibule","armpits", "tits", "knockers", "elbows", "eyes", "hooters","jugs", "lungs","headlights", "disk drives", "bumpers","knees","fried eggs", "buttocks", "charlies", "ear lobes", "bazooms","mammaries"

andd = "and"

thrust = "plunged","thrust", "squeezed", "pounded","drove","eased", "slid", "hammered", "squished", "crammed","slammed","reamed", "rammed", "dipped", "inserted", "plugged","augured","pushed", "ripped", "forced", "wrenched"

his = "his"

dongadj = "bursting", "jutting","glistening", "Brobdingnagian", "prodigious", "purple", "searing","swollen","rigid", "rampaging","warty","steaming", "gorged", "trunklike","foaming", "spouting", "swinish","prosthetic", "blue veined","engorged", "horse like", "throbbing","humongous","hole splitting", "serpentine", "curved", "steel encased", "glass encrusted","knobby", "surgically altered", "metal tipped", "open sored", "rapidly dwindling", "swelling", "miniscule","boney"

dong = "intruder", "prong","stump", "member", "meat loaf","majesty", "bowsprit", "earthmover", "jackhammer", "ramrod", "cod","jabber", "gusher", "poker","engine", "brownie","joy stick","plunger", "piston", "tool", "manhood", "lollipop", "kidney prodder", "candlestick", "John Thomas","arm","testicles", "balls","finger", "foot", "tongue", "dick", "one-eyed wonder worm", "canyon yodeler", "middle leg", "neck wrapper", "stick shift","dong", "Linda Lovelace choker"

intoher = "into her"

twatadj = "pulsing","hungry", "hymeneal", "palpitating","gaping", "slavering", "welcoming","glutted","gobbling", "cobwebby", "ravenous", "slurping", "glistening", "dripping", "scabiferous", "porous", "soft-spoken","pink", "dusty","tight","odiferous", "moist","loose","scarred", "weapon-less","banana stuffed", "tire tracked", "mouse nibbled","tightly tensed", "oft traveled", "grateful", "festering"

twat = "swamp.", "honeypot.","jam jar.", "butterbox.", "furburger.", "cherry pie.", "cush.","slot.","slit.", "cockpit.", "damp.","furrow.", "sanctum sanctorum.", "bearded clam.","continental divide.", "paradise valley.", "red river valley.","slot machine.", "quim.","palace.","ass.", "rose bud.","throat.","eye socket.", "tenderness.","inner ear.", "orifice.", "appendix scar.", "wound.", "navel.", "mouth.", "nose.","cunt."

# End of replies.

altogethernow = random.choice(faster) + " " + random.choice(said) + " " + the + " " + random.choice(fadj) + " " + random.choice(female) + " " + asthe + " " + random.choice(madjec) + " " + random.choice(male) + " " + random.choice(diddled) + " " + her + " " + random.choice(titadj) + " " + random.choice(knockers) + " " + andd + " " + random.choice(thrust) + " " + his + " " + random.choice(dongadj) + " " + random.choice(dong) + " " + intoher + " " + random.choice(twatadj) + " " + random.choice(twat)

print altogethernow