# Smart Image

fast Smart Image Processing Tools included:

	1. non-maximum-suppression

deploy:
1. write requirements.txt

	e.g. numpy==1.13.3
2. write setup.py, please refer to https://pypi.python.org/pypi?:action=list_classifiers to get the format of 'classifires' option in setup.py
3. write .pypirc and copy .pypirc into path ~/
	i.e. the .pypirc record your login information to pypi.org 
4. run setup.py check

	command: python setup.py check
5. build up python package e.g. smartImage

	command: python setup.py sdist
6. upload the python package to pypi.org

	command: python setup.py sdist upload -r pypi, 
please note that pre-registeration has been removed in present pypi upload process
7. install the costumerized python package
	
	command: pip install bbk.smartImage
