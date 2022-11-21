
TEST ?= $(shell bash -c 'read -p "Test: " TEST; echo $$TEST')

run:
	@g++ -o main Codigo/main.cpp
	@./main
	@rm main

test:
	@g++ -o test Test/$(TEST).cpp
	@./test
	@rm test