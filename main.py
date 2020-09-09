#! /usr/bin/env python3
"""
A Python 3 script for my r34 Discord bot.
"""
import urllib.request
import xmltodict
import random
import discord
import xml.parsers.expat

__version__ = '1.0'

domain = "https://rule34.xxx/index.php?"
client = discord.Client()


def get_data(url):
    """
    Returns data from a given url.
    """
    with urllib.request.urlopen(url) as file:
        xml = file.read()

    return xmltodict.parse(xml.decode('utf-8', 'replace'))


def get_post(tags):
    """
    Returns a random post from rule34.xxx using parameter tags.
    """
    url = domain + "page=dapi&s=post&q=index&tags=" + tags
    data = get_data(url)
    posts = 'posts'
    count = int(data[posts]['@count'])

    if count == 0:
        return None

    items = 100

    if count <= items:
        index = random.randint(0, count)

    else:
        limit = 200000

        if count > limit:
            count = limit

        index = random.randint(0, count)
        data = get_data(url + "&pid=" + str((index // items)))
        index %= 100

    post = data[posts]['post'][index]
    return "%s\n<%s%s%s>" % (
        post['@file_url'], domain, "page=post&s=view&id=", post['@id']
    )

def get_comment():
    """
    Returns a random comment from rule34.xxx.
    """
    data = get_data(domain + "page=dapi&s=comment&q=index")
    comment = random.choice(data['comments']['comment'])
    return "> %s\n%s (<https://rule34.xxx/index.php?page=post&s=view&id=%s>)" % (comment['@body'], comment['@creator'], comment['@post_id'])
    

@client.event
async def on_message(message):
    content = message.content
    prefix = "+r34"

    try:
        if content.startswith(prefix):
            content = get_post(content[len(prefix):].replace(" ", "+"))

        elif content.startswith("+pog"):
            content = get_comment()

        else:
            return

    except urllib.error.URLError:
        content = "Fetch failed."

    except xml.parsers.expat.ExpatError:
        content = "Parsing failed."

    if content is None:
        content = "No results."

    elif not message.channel.is_nsfw():
                content = "This is NOT a NSFW channel."

    await message.channel.send(content=content)


def main():
    with open('token.txt') as file:
        token = file.read()

    client.run(token)


if __name__ == '__main__':
    main()
