Summary:	A capable mail handling system with a command line interface.
Name:		nmh
Provides:	mh
Version:	0.27
Release:	9
Copyright:	freeware
Group:		Applications/Mail
Source:		ftp://ftp.math.gatech.edu/pub/nmh/%{name}-%{version}.tar.gz
Patch0:		nmh-0.24-config.patch
Patch1:		nmh-0.27-buildroot.patch
Patch2:		nmh-0.27-security.patch
Patch3:		nmh-0.27-compat21.patch
Requires:	smtpdaemon
Obsoletes:	mh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
LIBS=-lgdbm CFLAGS="$RPM_OPT_FLAGS" ./configure \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir}/nmh \
	--sysconfdir=/etc/nmh \
	--with-editor=/bin/vi

make

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/etc/nmh/*.old

strip --strip-unneeded $RPM_BUILD_ROOT%{_bindir}/* || :

gzip -9nf COPYRIGHT DIFFERENCES FAQ MAIL.FILTERING README TODO VERSION \
	ZSH.COMPLETION $RPM_BUILD_ROOT%{_mandir}/*/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -d %{_bindir}/mh -a ! -L %{_bindir}/mh ] ; then
    ln -s . %{_bindir}/mh
fi
if [ ! -d %{_libdir}/mh -a ! -L %{_libdir}/mh ] ; then
    ln -s nmh %{_libdir}/mh
fi

%triggerpostun -- mh, nmh <= 0.27-7
if [ ! -d %{_bindir}/mh -a ! -L %{_bindir}/mh ] ; then
    ln -s . %{_bindir}/mh
fi
if [ ! -d %{_libdir}/mh -a ! -L %{_libdir}/mh ] ; then
    ln -s nmh %{_libdir}/mh
fi

%preun
if [ $1 = 0 ]; then
    [ ! -L %{_bindir}/mh ] || rm -f %{_bindir}/mh
    [ ! -L %{_libdir}/mh ] || rm -f %{_libdir}/mh
fi

%files
%defattr(644,root,root,755)
%doc {COPYRIGHT,DIFFERENCES,FAQ,MAIL.FILTERING,README}.gz
%doc {TODO,VERSION,ZSH.COMPLETION}.gz
%dir %{_libdir}/nmh
%dir /etc/nmh
%config /etc/nmh/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/nmh/*
%{_mandir}/*/*
