import setuptools

setuptools.setup(
    name="pywatts",
    version="0.3.0",
    packages=setuptools.find_packages(),

    install_requires=['cloudpickle', 'holidays', 'xarray>=0.19', 'numpy', 'pandas', 'matplotlib', 'workalendar', 'tabulate'],
    extras_require={
        'dev': [
            "pytest",
            "sphinx>=4",
            "pylint",
            "pytest-cov"
        ],
        'sm': ['statsmodels'],
        'ml': ['scikit-learn >= 1.0'],
        'dl': ['tensorflow', 'torch'],
        'online': ['river']
    },
    author="pyWATTS-TEAM",
    author_email="pywatts-team@iai.kit.edu",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Natural Language :: English",
        "Operating System :: OS Independent",

    ],
    description="A python time series pipelining project",
    keywords="preprocessing time-series machine-learning",
)
