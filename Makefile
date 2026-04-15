PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share
DOCSDIR = $(DATADIR)/doc/rabbitvcs-cosmic

.PHONY: all install uninstall

all:
	@echo "Run 'make install' to install rabbitvcs-cosmic"

install:
	install -Dm755 rabbitvcs-cosmic-action $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-action
	install -Dm755 rabbitvcs-cosmic $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic
	install -Dm644 README.md $(DESTDIR)$(DOCSDIR)/README.md

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-action
	rm -f $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic
	rm -rf $(DESTDIR)$(DOCSDIR)
