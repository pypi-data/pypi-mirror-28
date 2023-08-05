from distutils.core import setup
setup(
  name = 'xy_voice',
  packages = ['xy_voice'],
  version = '5.0.0',
  description = 'Speech Recognition',
  long_description='Speech Recognition，voice2text,text2voice',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'voice', 'python3','python','Voice Recognition'],
  license='MIT',
  install_requires=[
        'pyaudio',
        'wave',
        'pinyinxy1'
    ],
)
