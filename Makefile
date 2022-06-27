clean:
	rm -rf *.pyc dist anvn.egg-info __pycache__ build ./*/__pycache__

upload:
	python setup.py upload

pyrcc:
	pyrcc5 -o anvn/anvn_resources.py anvn_resources.qrc

sdocs:
	docsify serve ./docs