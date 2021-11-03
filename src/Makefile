# -*- MakeFile -*-

CC = g++

CFLAGS = -std=c++11 -fPIC -shared -w -Wall -Wextra
PYTHONLIB = `python3.8-config --includes --libs`
BOOSTLIBS = -lboost_python38 -lboost_numpy38

DEBUGFLAGS = -g -Wall

seircpp: seircpp.cpp core.cpp gillespieSEIR.cpp
	$(CC) -o seircpp.so seircpp.cpp core.cpp gillespieSEIR.cpp \
	$(CFLAGS) $(PYTHONLIB) $(BOOSTLIBS)
