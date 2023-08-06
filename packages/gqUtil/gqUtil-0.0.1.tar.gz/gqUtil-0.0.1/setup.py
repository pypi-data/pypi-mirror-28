# coding:utf-8

from setuptools import setup, find_packages
import io
VERSION = '0.0.1'

with io.open("README.rst", encoding='utf-8') as f:
    long_description = f.read()
# 这里是读取那个文件里面的必须安装的  这样无论手动 pip install -r requirements.txt 安装
# 还是自动安装install_requires 都是这些信息
install_requires = open("requirements.txt").readlines()

setup(
    name="gqUtil",
    version=VERSION,
    description='myUtil',
    long_description=long_description,
    author='gaoqiang',
    author_email='gaoqiang1112@163.com',
    maintainer='gaoqiang',
    maintainer_email='gaoqiang1112@163.com',
    license='MIT License',
    packages=find_packages(),
    url='https://github.com/gaoqiang1112/gqUtil.git',
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    install_requires=install_requires,
)