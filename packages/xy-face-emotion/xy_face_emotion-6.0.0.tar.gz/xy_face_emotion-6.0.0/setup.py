from distutils.core import setup
setup(
  name = 'xy_face_emotion',
  packages = ['xy_face_emotion'],
  package_data = {'xy_face_emotion':['data/*']},
  version = '6.0.0',
  description = 'Check The Face Emotion With Living Video',
  long_description='Check The Face Emotion With Living Video',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'python3','python','Emotion','video'],
  license='MIT',
  install_requires=[
    'opencv-python',
    'numpy',
    'tensorflow',
    'keras',
    'pandas',
    'statistics',
    'h5py',
    'matplotlib',
    'PyYAML'
  ]
)
