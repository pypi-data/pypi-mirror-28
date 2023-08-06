.PHONY: test unittests coveragetest flaketest checkmanifest coverage

test: coveragetest flaketest setuptest checkmanifest

unittests:
	# Run unit tests with coverage
	coverage run --branch --source=opvoeden_api,tests setup.py test

coveragetest: unittests
	# Generate coverage report and require minimum coverage
	coverage report --show-missing --fail-under 95

flaketest:
	# Check syntax and style
	flake8

setuptest:
	python setup.py check -vmrs

checkmanifest:
	# Check if all files are included in the sdist
	check-manifest

coverage: unittests
	# Generate test coverage html report
	coverage html
