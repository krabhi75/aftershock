.PHONY: test scan serve

test:
	python3 -m unittest discover -s tests -v

scan:
	python3 -m aftershock scan

serve:
	python3 -m aftershock serve
