
TEST ?= $(shell bash -c 'read -p "Test: " TEST; echo $$TEST')

run:
	@g++ -o main Codigo/main.cpp -llept -ltesseract -O3
	@./main
	@rm main

test:
	@g++ -o test Test/$(TEST).cpp -llept -ltesseract -O3
	@./test
	@rm test
