from setuptools import setup

version = '0.0.2'

setup(
    name='video_funnel',
    packages=['video_funnel'],
    version=version,
    description='Use multiple connections to request the video, then feed the combined data to the player.',
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    author='Chen Shuaimin',
    author_email='chen_shuaimin@outlook.com',
    url='https://github.com/cshuaimin/video-funnel',
    python_requires='>=3.6',
    install_requires=['aiohttp', 'argparse'],

    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],
    license="MIT",
    keywords='Online multi-threaded video play',
    entry_points={
        'console_scripts': [
            'vf = video_funnel.__main__:main'
        ]
    }
)
