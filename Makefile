PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
LIBDIR = $(PREFIX)/lib
PKGLIBDIR = $(LIBDIR)/rabbitvcs-cosmic
DATADIR = $(PREFIX)/share
DOCSDIR = $(DATADIR)/doc/rabbitvcs-cosmic

.PHONY: all install uninstall

all:
	@echo "Run 'make install' to install rabbitvcs-cosmic"

install:
	install -Dm755 ra
	
	
	bbitvcs-cosmic-action $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-action
	install -Dm755 rabbitvcs-cosmic $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic
	install -Dm644 config.py $(DESTDIR)$(PKGLIBDIR)/config.py
	install -Dm755 settings.py $(DESTDIR)$(PKGLIBDIR)/settings.py
	install -Dm755 install.py $(DESTDIR)$(PKGLIBDIR)/install.py
	install -Dm755 uninstall.py $(DESTDIR)$(PKGLIBDIR)/uninstall.py
	install -Dm644 Makefile $(DESTDIR)$(PKGLIBDIR)/Makefile
	install -Dm644 README.md $(DESTDIR)$(DOCSDIR)/README.md
	printf '#!/bin/bash\nexec python3 $(PKGLIBDIR)/settings.py "$$@"\n' > $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-settings
	chmod 755 $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-settings
	printf '#!/bin/bash\nexec python3 $(PKGLIBDIR)/install.py "$$@"\n' > $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-install
	chmod 755 $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-install
	printf '#!/bin/bash\nexec python3 $(PKGLIBDIR)/uninstall.py "$$@"\n' > $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-uninstall
	chmod 755 $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-uninstall

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-action
	rm -f $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic
	rm -f $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-settings
	rm -f $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-install
	rm -f $(DESTDIR)$(BINDIR)/rabbitvcs-cosmic-uninstall
	rm -rf $(DESTDIR)$(PKGLIBDIR)
	rm -rf $(DESTDIR)$(DOCSDIR)
