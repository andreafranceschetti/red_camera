from distutils.core import setup


setup(name='red_camera',
      version='0.1',
      description='Python package to communicate from raspberry pi zero w to red camera raptor vk 8',
      author='Andrea Franceschetti',
      author_email='andrea.franceschetti.af@gmail.com',
      install_requires=['websockets', 'gpiozero'],
    #   scripts=['scripts/main']
     )