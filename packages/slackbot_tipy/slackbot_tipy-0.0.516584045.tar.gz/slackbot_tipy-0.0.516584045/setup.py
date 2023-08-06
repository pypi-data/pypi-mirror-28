import time

from setuptools import find_packages

from distutils.core import setup

patch_level = int(time.time())

ver = "0.0." + str(patch_level)[1:]

setup(
  name = 'slackbot_tipy',
  packages = find_packages(),
  version = ver,
  description = 'Python Module for Text Intent Slackbot',
  author = 'Wray Mills',
  author_email = 'wray@wrayesian.com',
  url = 'https://github.com/wray/tipy',
  download_url = 'https://github.com/wray/tipy/tarball/'+ver,
  keywords = ['slackbot', 'RPi', 'AWS'],
  classifiers = [],
)
