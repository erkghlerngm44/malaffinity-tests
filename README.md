# malaffinity-tests
Comparing affinity from MALAffinity against the value from MAL.

I really don't feel like writing stuff out, so I'll just list instructions 
and hope that's enough.

Thanks to TheEnigmaBlade for their 
[soulmate finder script](https://gist.github.com/TheEnigmaBlade/24205c62280b056fde3d)
which saved me a lot of potentially wasted time, trying to figure out how on earth to
authenticate with MAL, visit a user's page and get affinity.


## The thing you're here for: the results!
Results are at [`erkghlerngm44_results.txt`](erkghlerngm44_results.txt) 
(apologies for the shit taste).

Ran this script from 17:27 to 18:27 (approx) on the 10th April. As you can see,
malaffinity returns the same affinity as MAL 100% of the time.


## I don't believe you! How do I run this myself?
Sigh

### Setup
1. Download/fork/clone/whatever this repo.
2. [Create a Reddit client](https://www.reddit.com/prefs/apps) and put your
   `client_id`, `client_secret`, as well as a unique `user_agent`
   ([guidelines](https://github.com/reddit/reddit/wiki/API)) under the
   `reddit` config in `config.ini`.
3. Somehow acquire your `MALSESSIONID` cookie, and place that, as well as your
   MAL username under the `mal` config in `config.ini`.
4. Install dependencies (see ["Dependencies"](#dependencies) below).
5. Run script (see ["Usage"](#usage) below).

### Dependencies
* BeautifulSoup4
* Configparser
* MALAffinity
* PRAW 4
* Requests

For the lazy:

    $ pip install -r requirements.txt
    
You might run into issues when installing `MALAffinity`, specifically with
Scipy and Numpy. If this is the case, follow the instructions 
[here](https://github.com/erkghlerngm44/malaffinity#dependencies).

### Usage
* Run script. (`$ python3 affinity_tests.py`)
* Press `CTRL+C` (`^C`) when you want to stop. It'll run forever and ever if you don't.
* Check results.txt for results (in a nice table layout!)
* Problems? Got a `False` somewhere? 
  [Tell me](https://www.reddit.com/message/compose/?to=erkghlerngm44) and I'll have a look.
  

## That's it

Just realised that the effort required to connect to MAL and retrieve affinity that way
is a lot less than *making* a script to calculate it yourself.

![](https://i.imgur.com/7BwL6Fa.jpg)

Ah well. At least the effort required to *run* malaffinity is a lot less than scraping.
That's better for you, I guess.