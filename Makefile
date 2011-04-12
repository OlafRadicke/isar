
SHELL        = /bin/sh

DOCS         = ./docs
DOXYFILE     = ./docs/Doxyfile
DOXYDIR      = ./docs/doxygen

OUTPUT_DIST  = ./dist
OUTPUT_BUILD = ./build
PREFIX       = /usr/local/share
BINDIR       = /usr/local/bin

############  Rules  ############

# make build
all: dist

# check dependency
check:
	echo "sorry, does not implement!"

# clean build file
clean:
	$(RM)  $(wildcard $(OUTPUT_DIST))
	$(RM) -r $(wildcard $(OUTPUT_BUILD))
	$(RM) -r $(wildcard $(DOXYDIR))
	$(RM) -r $(OUTPUT_BUILD)/isar


# create distrebut-build
dist: doxygen
	mkdir $(OUTPUT_BUILD)
	cp ./GPL3.txt  $(OUTPUT_BUILD)
	cp ./README.txt  $(OUTPUT_BUILD)
	mkdir $(OUTPUT_BUILD)/src
	cp ./src/*.py  $(OUTPUT_BUILD)/src/
	mkdir $(OUTPUT_BUILD)/src/gui
	cp ./src/gui/*.py  $(OUTPUT_BUILD)/src/gui/
	mkdir ./$(OUTPUT_BUILD)/icons
	cp ./icons/*  $(OUTPUT_BUILD)/icons/
	mkdir $(OUTPUT_BUILD)/docs
	cp -R ./docs/*  $(OUTPUT_BUILD)/docs/
	ln -s $(OUTPUT_BUILD)/src/isar.py 

# create tar-file
tar: dist
	tar -cvzf ./isar_`date +%F`.tar.gz $(OUTPUT_BUILD)

# install program
install:
	mkdir $(PREFIX)/isar
	cp -r $(OUTPUT_BUILD)/* $(PREFIX)/isar/
	cp -R ./icons $(PREFIX)/isar/
	ln -s $(PREFIX)/isar/usr/isar.py /usr/local/bin/isar
	mkdir /var/isar

# remove program
uninstall:
	$(RM) -r $(PREFIX)/isar
	$(RM) $(BINDIR)/isar
	$(RM) /usr/local/bin/isar

# build doxygen-docs
doxygen:
	doxygen $(DOXYFILE)

.PHONY: all check clean dist install uninstall doxygen
