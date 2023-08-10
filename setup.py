from distutils.core import setup

with open('requirements.txt') as file:
  requirements = file.readlines()

setup(name='red_camera',
      version='0.1',
      description='Python package to communicate from raspberry pi zero w to red camera raptor vk 8',
      author='Andrea Franceschetti',
      author_email='andrea.franceschetti.af@gmail.com',
      install_requires=requirements
    #   scripts=['scripts/main']
     )