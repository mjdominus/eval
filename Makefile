
SOURCE= grammar.py semantics.py
TESTS=  test_exprs.py

test: .test

.test: $(SOURCE) $(TESTS)
	./test_exprs.py && touch .test
