#! /usr/bin/env python3
"""
A Python 3 script for my r34 Discord bot.
"""
import urllib.request
import xmltodict
import random
import discord

__version__ = '1.0'

client = discord.Client()


def get_data(url):
    """
    Returns data from a given url.
    """
    with urllib.request.urlopen(url) as file:
        xml = file.read()

    return xmltodict.parse(xml.decode("utf8"))


def get_post(tags):
    """
    Returns a random post from rule34.xxx using parameter tags.
    """
    url = "https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=" + tags
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
        data = get_data(url + "&pid=" + str((index // items) - 1))
        index %= 100

    return data[posts]['post'][index]['@file_url']


@client.event
async def on_message(message):
    content = message.content
    prefix = "+r34 "

    if not (content.startswith(prefix) and message.channel.is_nsfw()):
        return

    content = get_post(content[len(prefix):])

    if content is None:
        content = "No results."

    await message.channel.send(content=content)


def main():
    with open('token.txt') as file:
        token = file.read()

    client.run(token)


if __name__ == '__main__':
    main()
