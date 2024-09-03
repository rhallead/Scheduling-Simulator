# Makefile for building schedSim executable

# Compiler settings
PYTHON = python

# Executable name
EXECUTABLE = schedSim

# Source files
SRC = schedSim.py

# Default target
all: $(EXECUTABLE)

# Build the executable
$(EXECUTABLE): $(SRC)
	chmod +x $(SRC)

# Clean up
clean:
    # No cleanup needed for Python script
