CC := g++
CFLAGS := -Wall -Wextra -pedantic -std=c++23 -O2

EXE := convert.exe

SRCDIR := src
SOURCES := $(wildcard $(SRCDIR)/*.cpp)
OBJDIR := obj
OBJS := $(patsubst $(SRCDIR)/%.cpp,$(OBJDIR)/%.o,$(SOURCES))

build: $(OBJS)
	@$(CC) $(CFLAGS) -o $(EXE) $(OBJS)

$(OBJDIR)/%.o: %.cpp | $(OBJDIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJDIR):
	@mkdir -p $(OBJDIR)

.PHONY: clean
clean:
	@rm -f $(EXE) $(OBJS)