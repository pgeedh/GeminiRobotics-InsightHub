from setuptools import setup
import os
from glob import glob

package_name = 'ros2_gemini_bridge'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Pruthvi Geedh',
    maintainer_email='pgeedh@users.noreply.github.com',
    description='ROS 2 bridge nodes for Google DeepMind Gemini Robotics 2.0 (ER 2 and VLA 2)',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gemini_perception_node = ros2_gemini_bridge.gemini_perception_node:main',
            'gemini_planner_node = ros2_gemini_bridge.gemini_planner_node:main',
        ],
    },
)
