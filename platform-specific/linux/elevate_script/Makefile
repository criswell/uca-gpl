# Makefile for the Elevate Script tool

#include ../Globals.mk

SOURCES=elevate_script.cpp

OBJECTS=elevate_script.o

elevate_script: $(OBJECTS)
	$(CPP) $(OBJECTS) -o elevate_script

static: $(OBJECTS)
	@echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	@echo Static linking enabled - Be sure to check the README/INSTALL
	@echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	$(CPP) $(STATIC_BASE) $(STATIC_CC) $(OBJECTS) -o elevate_script

elevate_script.o: $(SOURCES) $(HEADERS)
	$(CPP) $(CP_FLAGS) $(SOURCES)

.PHONY: clean

clean:
	@echo Cleaning the build environment
	@rm -f *~ *.o *.so core core.*
	@rm -f elevate_script

