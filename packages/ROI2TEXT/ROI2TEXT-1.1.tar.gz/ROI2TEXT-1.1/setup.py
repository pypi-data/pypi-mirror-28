import setuptools

setuptools.setup(
    name="ROI2TEXT",
    version="1.1",
    url="https://github.com/unique1o1/ROI2TEXT",

    author="Yunik Maharjan",
    author_email="yunik.maharjan@icloud.com",
    license='MIT',
    description="Quickly extract text from your screenshot into clipboard",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=['requests', 'pyscreenshot',
                      'pynput', 'pytesseract', 'scipy', 'numpy', 'pillow'],
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3'
    ],
    # download_url='https://github.com/unique1o1/Meet-SMS/archive/v1.3.1.tar.gz',
    entry_points="""
    [console_scripts]
    img2txt=roi2text.roi2text:main
    """,
)
