__author__ = 'yusaira-khan'
import requests
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
proj_dir = os.path.dirname(current_dir)
speex_path = os.path.join(proj_dir, 'speex/')
try:
    os.mkdir(speex_path)
except OSError:
    pass
    # file already exists


with open('speex.min.js', 'w+') as handle:
    response = requests.get('https://raw.githubusercontent.com/yusaira-khan/speex.js/master/dist/speex.min.js',
                            stream=True)

    if not response.ok:
        # Something went wrong
        exit()

    for block in response.iter_content(1024):
        handle.write(block)
