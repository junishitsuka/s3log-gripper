from setuptools import setup, find_packages

setup(
    name='gripper',
    version='1.0',
    packages=find_packages(),
    install_requires=['awscli'],
    entry_points={
        'console_scripts': 'gripper = src.main:gripper'
    },
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
