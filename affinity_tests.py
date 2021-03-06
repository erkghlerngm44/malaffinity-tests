#!/usr/bin/env python3

import re
import time

import bs4
import configparser
import malaffinity
import praw
import requests

import tableprint


wait_between_requests = 2
retry_after_failed_request = 5

regex = "myanimelist\.net/(?:profile|animelist)/([a-z0-9_-]+)"
regex = re.compile(regex, re.I)

mal_profile_url = "https://myanimelist.net/profile/{}"


# Grab stuff from the config file.
config = configparser.ConfigParser()
config.read("config.ini")

reddit = config.items("reddit")
reddit = dict(reddit)

mal = config.items("mal")
mal = dict(mal)


# Set up the request session to authenticate with MAL
session = requests.Session()

# Retrieve the CSRF token from MAL and store into `session`'s cookies.
# Auth won't work without this
c = session.get("https://myanimelist.net/login.php")
s = bs4.BeautifulSoup(c.content, "html.parser")
csrf = s.select_one('meta[name="csrf_token"]').attrs["content"]

# Now use that, as well as the username, password and other things, to authenticate
r = session.post("https://myanimelist.net/login.php", data={
    "user_name": mal["username"],
    "password": mal["password"],
    # Stay authenticated (not sure if this does anything)
    "cookie": "1",
    # Why, Xinil?
    "submit": "1",
    "csrf_token": csrf
})

# Check the request went well, raise an exception if not
if r.ok:
    print("Successfully authenticated with MAL")
else:
    raise Exception("Something happened")


# Set up the malaffinity thing now.
pearson = malaffinity.MALAffinity(mal["username"], round=1)


def get_comment_stream():
    # HACK: avoiding dodgy "local variable referenced before assignment"
    # bullshit I can't be bothered to deal with.
    reddit = praw.Reddit( **globals()["reddit"] )

    return reddit.subreddit("anime").stream.comments()

def get_affinity_from_mal(username):
    resp = session.request(
        "GET",
        mal_profile_url.format(username)
    )

    # TODO: Handle this better.
    if not resp.ok:
        return

    resp = bs4.BeautifulSoup(resp.content, "html.parser")

    # typo intentional. WHY, XINIL?
    affinity = resp.select_one(".user-compatability-graph .bar-outer.anime .bar-inner")
    affinity = affinity.string.strip()
    # Handle the stupid "--" things that happen with negative affinities
    affinity = affinity.replace("--", "-")
    # Remove the percent.
    affinity = affinity.replace("%", "")
    affinity = float(affinity)

    return affinity


def handle_comment(comment):
    if not comment.author:
        return

    author_name = comment.author.name

    if author_name in processed:
        return

    processed.add(author_name)

    print("Processing user: {}".format(author_name))

    flair_text = comment.author_flair_text

    if not flair_text:
        print("- No flair text. Skipping...")
        return

    match = regex.search(flair_text)

    if not match:
        print("- Can't find MAL username. Skipping...")
        return

    username = match.group(1)

    time.sleep(wait_between_requests)

    success = False

    for _ in range(2):
        try:
            our_affinity = pearson.calculate_affinity(username)

        except malaffinity.exceptions.MALRateLimitExceededError:
            print("- MAL rate limit exceeded. Halting for a few seconds...")
            time.sleep(retry_after_failed_request)
            continue

        except malaffinity.exceptions.MALAffinityException:
            print("- Affinity can't be calculated for some reason.")
            return

        except Exception as e:
            # Will this ever happen?
            print("- Some other error occured. Error: {}".format(e))

            a = input("Press [ENTER] to skip, `X`, [ENTER] to exit ")
            if a.upper() == "X": exit()
            else: return

        else:
            success = True

    if not success:
        return

    # No need to include shared as we're just checking affinity stuff.
    # Shared count on MAL's out of whack as well. (Includes PTW + unrated for some reason)
    our_affinity = our_affinity[0]

    print("- MALAffinity says affinity is {}%".format(our_affinity))

    # Halt again.
    time.sleep(wait_between_requests)

    # Now get the affinity from MAL.
    mal_affinity = get_affinity_from_mal(username)

    if not mal_affinity:
        print("- MAL refused to give us the affinity for some reason. Ah well.")
        return

    print("- MAL says affinity is {}%".format(mal_affinity))

    # Save to results.
    results.append({
        "username": username,
        "malaffinity": our_affinity,
        "mals_affinity": mal_affinity,
        "match": our_affinity == mal_affinity
    })

    return


def main():
    global processed
    global results

    processed = set()
    results = list()

    comments = get_comment_stream()

    start_time = time.time()

    while True:
        try:
            for comment in comments:
                handle_comment(comment)

        except KeyboardInterrupt:
            print("\n\n" + "KeyboardInterrupt. Breaking loop...")
            break

        except Exception as e:
            print("Error: {}".format(e))
            time.sleep(30)

    end_time = time.time()

    runtime = round(end_time - start_time)

    print("Script runtime: {} seconds".format(runtime))
    print("Writing results...")

    # Write to pretty table.
    table = tableprint.TablePrint("results.txt", space_out=20)

    table.write_row("MAL Username", "MALAffinity", "MAL's Affinity", "Match?", is_header=True)

    for result in results:
        row = [
            result["username"],
            result["malaffinity"],
            result["mals_affinity"],
            result["match"]
        ]

        table.write_row(row)

    table.close()

    return


if __name__ == "__main__":
    main()
