SUBDIRS = resource license src

desktopdir = @home@/Desktop

shortcut:
	cp -f plexicon.desktop $(desktopdir)/plexicon.desktop
	chown @user@ $(desktopdir)/plexicon.desktop
	chmod u+x $(desktopdir)/plexicon.desktop

remove-shortcut:
	rm -f $(desktopdir)/plexicon.desktop