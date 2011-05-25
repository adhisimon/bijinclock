NAME = bijinclock
VERSION = 0.9.6
DESTDIR = /usr/local
BINDIR = /bin
DATADIR = /usr/local/share

install: bijinclock bijinclock.desktop README
	mkdir -p $(DESTDIR)/$(BINDIR)
	install -m 755 -t $(DESTDIR)/$(BINDIR) bijinclock
	mkdir -p $(DATADIR)/applications/
	install -m 644 bijinclock.desktop $(DATADIR)/applications/
	mkdir -p $(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 README $(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 AUTHOR $(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 COPYING $(DATADIR)/doc/$(NAME)-$(VERSION)
	install -m 644 INSTALL $(DATADIR)/doc/$(NAME)-$(VERSION)

uninstall:
	rm -f $(DESTDIR)/$(BINDIR)/bijinclock
	rm -f $(DATADIR)/applications/bijinclock.desktop
	rm -rf $(DATADIR)/doc/$(NAME)-$(VERSION)

rpm: tar
	rpmbuild -ta $(NAME)-$(VERSION).tar.bz2
	echo $(TEST)

tar: $(NAME)-$(VERSION).tar.bz2

$(NAME)-$(VERSION).tar.bz2: bijinclock bijinclock.spec bijinclock.desktop README
	git archive --prefix $(NAME)-$(VERSION)/ --format=tar HEAD| bzip2 -c > $(NAME)-$(VERSION).tar.bz2

clean:
	rm -f $(NAME)-*.tar.bz2
