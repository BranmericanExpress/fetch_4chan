from setuptools import setup, find_packages

setup(
  name='fetch_4chan',
  version='1.0.0',
  packages=find_packages(),
  install_requires=[
    'requests',
    'tqdm'
  ],
  entry_points={
    'console_scripts': [
      'fetch-4chan=scripts.fetch_threads:main'
    ],
  },
  author='Brandon Pettee',
  author_email='brandonwpettee@gmail.com',
  description='A script to fetch threads and images from 4chan.',
  url='https://github.com/BranmericanExpress/fetch_4chan',
)