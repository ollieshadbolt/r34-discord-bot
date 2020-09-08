import urllib.request
import xmltodict
import random
import discord


client = discord.Client()


def get_data(url):
    with urllib.request.urlopen(url) as fp:
        mybytes = fp.read()

    return xmltodict.parse(mybytes.decode("utf8"))


def get_post(tags):
    url = "https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=" + tags
    data = get_data(url)
    posts = 'posts'
    count = int(data[posts]['@count'])

    if count == 0:
        return None
    
    items = 100

    if count <= items:
        randint = random.randint(0, count)

    else:
        limit = 200000
        
        if count > limit:
            count = limit

        randint = random.randint(0, count)
        data = get_data(url + "&pid=" + str((randint // items) - 1))
        randint %= 100

    return data[posts]['post'][randint]['@file_url']


@client.event
async def on_message(message):
    content = message.content
    prefix = "r34"
    
    if not content.startswith(prefix):
        return

    await message.channel.send(content=get_post(content[len(prefix):]))


def main():
    with open('token.txt') as fp:
        token = fp.read()
    
    client.run(token)


if __name__ == '__main__':
    main()
