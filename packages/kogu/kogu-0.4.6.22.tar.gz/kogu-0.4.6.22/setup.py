from setuptools import setup, find_packages

setup(
    name='kogu',
    version='0.4.6.22',
    description='Kogu helper library',
    url='https://kogu.ai',
    download_url='https://drive.google.com/uc?authuser=0&' +
    'id=1z7AfFkVfHs7LoDOyFy8U54hfjie1fbJc&export=download',
    author='Proekspert AS',
    author_email='hello@kogu.ai',
    license='MIT',
    packages=find_packages(),
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
)
