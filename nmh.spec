Summary: A capable mail handling system with a command line interface.
Name: nmh
Obsoletes: mh
Provides: mh
Version: 0.27
Release: 8
Requires: smtpdaemon
Copyright: freeware
Group: Applications/Internet
Source0: ftp://ftp.math.gatech.edu/pub/nmh/nmh-0.27.tar.gz
Patch0: nmh-0.24-config.patch
Patch1: nmh-0.27-buildroot.patch
Patch2: nmh-0.27-security.patch
Patch3: nmh-0.27-compat21.patch
Buildroot: /var/tmp/%{name}-root

%description
Nmh is an email system based on the MH email system and is intended
to be a (mostly) compatible drop-in replacement for MH.  Nmh isn't
a single comprehensive program.  Instead, it consists of a number
of fairly simple single-purpose programs for sending, receiving,
saving, retrieving and otherwise manipulating email messages.  You
can freely intersperse nmh commands with other shell commands or
write custom scripts which utilize nmh commands.  If you want to use
nmh as a true email user agent, you'll want to also install exmh to
provide a user interface for it--nmh only has a command line interface.

If you'd like to use nmh commands in shell scripts, or if you'd like to
use nmh and exmh together as your email user agent, you should install
nmh.

%prep
%setup -q
%patch0 -p1 -b .config
%patch1 -p1 -b .buildroot
%patch2 -p1 -b .security
%patch3 -p1 -b .compat21

%build
LIBS=-lgdbm ./configure --prefix=/usr \
			--exec-prefix=/usr \
			--bindir=/usr/bin \
			--libdir=/usr/lib/nmh \
			--sysconfdir=/etc/nmh \
			--with-editor=/bin/vi

make

%install
DESTDIR=$RPM_BUILD_ROOT make install
strip `file $RPM_BUILD_ROOT/usr/bin/* | grep ELF | cut -d':' -f 1`

# XXX unnecessary because DOT_LOCKING is disabled
# chown root.mail $RPM_BUILD_ROOT/usr/bin/inc
# chmod 2755 $RPM_BUILD_ROOT/usr/bin/inc

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -d /usr/bin/mh -a ! -L /usr/bin/mh ] ; then
    ln -s . /usr/bin/mh
fi
if [ ! -d /usr/lib/mh -a ! -L /usr/lib/mh ] ; then
    ln -s nmh /usr/lib/mh
fi

%triggerpostun -- mh, nmh <= 0.27-7
if [ ! -d /usr/bin/mh -a ! -L /usr/bin/mh ] ; then
    ln -s . /usr/bin/mh
fi
if [ ! -d /usr/lib/mh -a ! -L /usr/lib/mh ] ; then
    ln -s nmh /usr/lib/mh
fi

%preun
if [ $1 = 0 ]; then
    [ ! -L /usr/bin/mh ] || rm -f /usr/bin/mh
    [ ! -L /usr/lib/mh ] || rm -f /usr/lib/mh
fi

%files
%defattr(-,root,root)
%doc COPYRIGHT DIFFERENCES FAQ MAIL.FILTERING README TODO VERSION ZSH.COMPLETION
%dir /usr/lib/nmh
%dir /etc/nmh
%config /etc/nmh/*
/usr/bin/*
/usr/lib/nmh/*
/usr/man/*/*
