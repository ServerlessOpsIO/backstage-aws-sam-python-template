build-CommonLayer:
	python${{ values.python_version  }} ./setup.py build
	pip${{ values.python_version   }} wheel -w tmp -e .
	mkdir $(ARTIFACTS_DIR)/python
	pip${{ values.python_version   }} install tmp/common-* --target $(ARTIFACTS_DIR)/python/

