NAME = bijinclock
VERSION = 0.9.3
DESTDIR = /usr/local

install: bijinclock bijinclock.desktop README
	mkdir -p $(DESTDIR)/bin
	install -m 755 bijinclock $(DESTDIR)/bin/
	mkdir -p $(DESTDIR)/share/applications/
	install -m 644 bijinclock.desktop $(DESTDIR)/share/applications/
	mkdir -p $(DESTDIR)/share/doc/$(NAME)-$(VERSION)
	install -m 644 README $(DESTDIR)/share/doc/$(NAME)-$(VERSION)

uninstall:
	rm -f $(DESTDIR)/bin/bijinclock
	rm -f $(DESTDIR)/share/applications/bijinclock.desktop
	rm -rf $(DESTDIR)/share/doc/$(NAME)-$(VERSION)

rpm: tar
	rpmbuild -ta $(NAME)-$(VERSION).tar.bz2
	echo $(TEST)

tar: $(NAME)-$(VERSION).tar.bz2

$(NAME)-$(VERSION).tar.bz2: bijinclock bijinclock.spec bijinclock.desktop README
	git archive --prefix $(NAME)-$(VERSION)/ --format=tar HEAD| bzip2 -c > $(NAME)-$(VERSION).tar.bz2

clean:
	rm -f $(NAME)-*.tar.bz2
