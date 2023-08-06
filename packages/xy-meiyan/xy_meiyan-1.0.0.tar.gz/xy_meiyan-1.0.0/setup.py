from distutils.core import setup
setup(
  name = 'xy_meiyan',
  packages = ['xy_meiyan'],
  package_data = {'xy_meiyan':['data/*']},
  version = '1.0.0',
  description = 'Image beauty',
  long_description='Image beauty',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'python3','python','Image beauty','Image','Beauty'],
  license='MIT',
  install_requires=[
    'numpy',
    'scipy',
    'pillow'
  ]
)
