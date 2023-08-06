import setuptools

setuptools.setup(
    name="nbrsessionproxy",
    version='0.6.1',
    url="https://github.com/jupyterhub/nbrsessionproxy",
    author="Ryan Lovett",
    description="Jupyter extension to proxy RStudio's rsession",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'notebook',
        'nbserverproxy >= 0.5.1'
    ],
    package_data={'nbrsessionproxy': ['static/*']},
)
