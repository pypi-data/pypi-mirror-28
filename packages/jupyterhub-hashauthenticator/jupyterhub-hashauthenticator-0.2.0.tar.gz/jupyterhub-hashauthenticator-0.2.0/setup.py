from setuptools import setup

setup(
    name='jupyterhub-hashauthenticator',
    version='0.2.0',
    description='Hashed Password Authenticator for JupyterHub',
    url='https://github.com/thedataincubator/jupyterhub-hashauthenticator',
    author='Petko Minkov',
    author_email='pminkov@gmail.com',
    maintainer='Robert Schroll',
    maintainer_email='robert@thedataincubator.com',
    scripts=['scripts/hashauthpw', 'scripts/hashauthservice'],
    install_requires=['jupyterhub'],
    test_suite="hashauthenticator.tests",
    license='BSD3',
    packages=['hashauthenticator'],
)
