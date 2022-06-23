clean:
	rm -rf *.pyc dist anvn.egg-info __pycache__ build ./*/__pycache__

upload:
	python setup.py upload

pyrcc:
	pyrcc5 -o anvn/resources.py resources.qrc

sdocs:
	docsify serve ./docs