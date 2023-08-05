from distutils.core import setup
setup(
  name = 'xy_face_glass',
  packages = ['xy_face_glass'],
  version = '1.0.0',
  description = 'Auto Add Glass On Your Face',
  long_description='Auto Add Glass On Your Face',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'python3','python','face detect','face','glass'],
  license='MIT',
  install_requires=[
    'opencv-python',
    'imutils',
    'moviepy',
    'dlib',
    'numpy',
    'imageio',
    'pillow'
  ]
)
