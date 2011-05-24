NAME = bijinclock
VERSION = 0.9.3

rpm: $(NAME)-$(VERSION).tar.bz2
	rpmbuild -ta $(NAME)-$(VERSION).tar.bz2

$(NAME)-$(VERSION).tar.bz2: bijinclock bijinclock.spec bijinclock.desktop
	git archive --prefix $(NAME)-$(VERSION)/ --format=tar HEAD| bzip2 -c > $(NAME)-$(VERSION).tar.bz2

clean:
	rm -f $(NAME)-*.tar.bz2
