SUBDIRS = resource license src

desktopdir = @home@/Desktop

shortcut:
	cp plexicon.desktop $(desktopdir)/plexicon.desktop
	chown @user@ $(desktopdir)/plexicon.desktop
	chmod u+rwx $(desktopdir)/plexicon.desktop
	chmod a+x $(datadir)/plexicon/src/plexicon.py

remove-shortcut:
	rm $(desktopdir)/plexicon.desktop
