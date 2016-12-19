try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

VERSION = '1.0.dev22'
DESCRIPTION = "BioC data structures and encoder/decoder for Python"
with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
        name='bioc',
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author='Yifan Peng',
        author_email='yifan.peng@nih.gov',
        keywords=['bioc'],
        license='BSD 3-clause license',
        packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
        url='https://github.com/yfpeng/pengyifan-pybioc',
        platforms=['any'],
        install_requires=[
            'docutils>=0.3',
            'lxml'],
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Console',
            'Environment :: MacOS X',
            'Environment :: X11 Applications :: Qt',
            'Environment :: Win32 (MS Windows)',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Text Processing :: Markup :: XML',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
        ],
)
