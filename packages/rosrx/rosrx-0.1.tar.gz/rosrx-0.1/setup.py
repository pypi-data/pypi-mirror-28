from setuptools import setup

setup(name='rosrx',
      version='0.1',
      description='Reactive extensions for rospy',
      url='http://github.com/nlinkas/rosrx',
      author='Joergen Borgesen',
      author_email='jorgen@nlink.no',
      keywords='rx rxpy reactive ROS rospy',
      license='MIT',
      packages=['rosrx'],
      install_requires=['rx'],
      zip_safe=True)
