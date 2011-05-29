NAME = bijinclock
VERSION = 1.0.0
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
	install -m 644 bijinclock.png $(DESTDIR)/$(DATADIR)/icons/bijinclock.png

uninstall:
	rm -f $(DESTDIR)/$(BINDIR)/bijinclock
	rm -f $(DESTDIR)/$(DATADIR)/applications/bijinclock.desktop
	rm -rf $(DESTDIR)/$(DATADIR)/doc/$(NAME)-$(VERSION)
	rm -f $(DESTDIR)/$(DATADIR)/icons/bijinclock.png

rpm: tar
	rpmbuild -ta $(NAME)-$(VERSION).tar.bz2

tar: $(NAME)-$(VERSION).tar.bz2

$(NAME)-$(VERSION).tar.bz2: bijinclock.py bijinclock.spec bijinclock.desktop README INSTALL AUTHOR COPYING bijinclock.png
	git archive --prefix $(NAME)-$(VERSION)/ --format=tar HEAD| bzip2 -c > $(NAME)-$(VERSION).tar.bz2

signedrpm: tar
	rpmbuild --sign -ta $(NAME)-$(VERSION).tar.bz2

upload2repo: signedrpm
	scp ~/rpmbuild/RPMS/noarch/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/fedora/13/i386/
	scp ~/rpmbuild/RPMS/noarch/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/fedora/13/x86_64/
	scp ~/rpmbuild/SRPMS/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/fedora/13/SRPMS/
	scp ~/rpmbuild/RPMS/noarch/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/fedora/14/i386/
	scp ~/rpmbuild/RPMS/noarch/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/fedora/14/x86_64/
	scp ~/rpmbuild/SRPMS/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/fedora/14/SRPMS/
	scp ~/rpmbuild/RPMS/noarch/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/fedora/15/i386/
	scp ~/rpmbuild/RPMS/noarch/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/fedora/15/x86_64/
	scp ~/rpmbuild/SRPMS/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/fedora/15/SRPMS/
	scp ~/rpmbuild/RPMS/noarch/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/rhel/5/i386/
	scp ~/rpmbuild/RPMS/noarch/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/rhel/5/x86_64/
	scp ~/rpmbuild/SRPMS/$(NAME)-$(VERSION)*.rpm websimon@axis.email-pribadi.com:adhisimonrepo/rhel/5/SRPMS/


clean:
	rm -f $(NAME)-*.tar.bz2
