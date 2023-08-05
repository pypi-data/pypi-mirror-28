package=procgraph
include pypackage.mk



bump-upload:
	bumpversion   patch
	git push --tags
	git push --all
	rm -f dist/*
	find src -name '*pgc' -delete
	python setup.py sdist
	twine upload dist/*
