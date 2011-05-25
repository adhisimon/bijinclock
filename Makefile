NAME = bijinclock
VERSION = 0.9.8.1
DESTDIR = /
BINDIR = /usr/local/bin
DATADIR = /usr/local/share

install: bijinclock bijinclock.desktop README
	mkdir -p $(DESTDIR)/$(BINDIR)
	install -m 755 -t $(DESTDIR)/$(BINDIR) bijinclock
	mkdir -p $(DESTDIR)/$(DATADIR)/applications/
	install -m 644 bijinclock.desktop $(DESTDIR)/$(DATADIR)/applications/
	mkdir -p $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 README $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 AUTHOR $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 COPYING $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 INSTALL $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)

uninstall:
	rm -f $(DESTDIR)/$(BINDIR)/bijinclock
	rm -f $(DESTDIR)/$(DATADIR)/applications/bijinclock.desktop
	rm -rf $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)

rpm: tar
	rpmbuild -ta $(NAME)-$(VERSION).tar.bz2

tar: $(NAME)-$(VERSION).tar.bz2

$(NAME)-$(VERSION).tar.bz2: bijinclock bijinclock.spec bijinclock.desktop README
	git archive --prefix $(NAME)-$(VERSION)/ --format=tar HEAD| bzip2 -c > $(NAME)-$(VERSION).tar.bz2

clean:
	rm -f $(NAME)-*.tar.bz2
