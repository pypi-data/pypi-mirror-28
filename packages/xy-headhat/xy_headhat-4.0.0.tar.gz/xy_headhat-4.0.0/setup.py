from distutils.core import setup
setup(
  name = 'xy_headhat',
  packages = ['xy_headhat'],
  package_data = {'xy_headhat':['data/*']},
  version = '4.0.0',
  description = 'Add Christmas Hat',
  long_description='Auto Add Christmas Hat On Your Head',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'python3','python','christmas','head','hat'],
  license='MIT',
  install_requires=[
    'opencv-python',
    'numpy',
    'dlib',
    'pillow'
  ]
)
