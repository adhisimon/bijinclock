NAME = bijinclock
VERSION = 0.9.9
DESTDIR = /
BINDIR = /usr/local/bin
DATADIR = /usr/local/share

install:
	mkdir -p $(DESTDIR)/$(BINDIR)
	install -m 755 bijinclock.py $(DESTDIR)/$(BINDIR)/bijinclock
	mkdir -p $(DESTDIR)/$(DATADIR)/applications/
	install -m 644 bijinclock.desktop $(DESTDIR)/$(DATADIR)/applications/
	mkdir -p $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 README $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 AUTHOR $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 COPYING $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 INSTALL $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	mkdir -p $(DESTDIR)/$(DATADIR)/icons
	install -m 644 bijinclock.png $(DESTDIR)/$(DATADIR)/icons/adhisimon-bijinclock.png

uninstall:
	rm -f $(DESTDIR)/$(BINDIR)/bijinclock
	rm -f $(DESTDIR)/$(DATADIR)/applications/bijinclock.desktop
	rm -rf $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	rm -f $(DESTDIR)/$(DATADIR)/icons/adhisimon-bijinclock.png

rpm: tar
	rpmbuild -ta $(NAME)-$(VERSION).tar.bz2

tar: $(NAME)-$(VERSION).tar.bz2

$(NAME)-$(VERSION).tar.bz2: bijinclock.py bijinclock.spec bijinclock.desktop README INSTALL AUTHOR COPYING bijinclock.png
	git archive --prefix $(NAME)-$(VERSION)/ --format=tar HEAD| bzip2 -c > $(NAME)-$(VERSION).tar.bz2

clean:
	rm -f $(NAME)-*.tar.bz2
