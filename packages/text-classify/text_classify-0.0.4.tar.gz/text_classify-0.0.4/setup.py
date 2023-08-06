try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='text_classify',
    version='0.0.4',
    description='Simple tool to predict text classes with various models.',
    long_description=readme(),
    license='MIT',
    packages=['text_classify'],
    install_requires=['jieba', 'pyltp', 'numpy', 'scipy', 'pybind11'],
    zip_safe=False,
)
