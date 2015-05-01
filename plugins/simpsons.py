"""!simpsons returns a random simpsons screenshot"""
import re
import requests
from random import randint


def simpsons():
    r = requests.get('http://homerize.com/_framegrabs/')
    directories = re.findall(r'<a href="([^"]+?/)">', r.text)
    rand_dir = directories[randint(0, len(directories))]
    pic_dir = 'http://homerize.com/_framegrabs/{}'.format(rand_dir)
    r2 = requests.get(pic_dir)
    images = re.findall(r'<a href="([^"]+?\.jpg)">', r2.text)
    rand_img = images[randint(0, len(images))]
    img_url = "{}{}".format(pic_dir, rand_img)
    return img_url


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!simpsons", text)
    if not match:
        return
    return simpsons()