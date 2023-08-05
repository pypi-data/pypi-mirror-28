from distutils.core import setup
setup(
  name = 'xy_facedetect',
  packages = ['xy_facedetect'],
  package_data = {'xy_facedetect':['data/*']},
  # package_dir = {'':'xy_facedetect'},
  # data_files = [('data/haarcascade_frontalface_default.xml')],
  # include_package_data = True,
  version = '8.0.2',
  description = 'Get The Face Detect',
  long_description='Get The Face Detect',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'python3','python','face detect','face','detect'],
  license = 'MIT',
  install_requires = ['opencv-python']
)
