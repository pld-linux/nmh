Summary:	A capable mail handling system with a command line interface
Name:		nmh
Provides:	mh
Version:	0.27
Release:	9
Copyright:	freeware
Group:		Applications/Mail
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Source0:	ftp://ftp.math.gatech.edu/pub/nmh/%{name}-%{version}.tar.gz
Patch0:		nmh-0.24-config.patch
Patch1:		nmh-0.27-buildroot.patch
Patch2:		nmh-0.27-security.patch
Patch3:		nmh-0.27-compat21.patch
Requires:	smtpdaemon
Obsoletes:	mh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/lib/nmh
%define		_sysconfdir	/etc/nmh

%description
Nmh is an email system based on the MH email system and is intended to
be a (mostly) compatible drop-in replacement for MH. Nmh isn't a
single comprehensive program. Instead, it consists of a number of
fairly simple single-purpose programs for sending, receiving, saving,
retrieving and otherwise manipulating email messages. You can freely
intersperse nmh commands with other shell commands or write custom
scripts which utilize nmh commands. If you want to use nmh as a true
email user agent, you'll want to also install exmh to provide a user
interface for it--nmh only has a command line interface.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
LIBS="-lgdbm"
LDFLAGS="-s"
export LIBS LDFLAGS
%configure \
	--with-editor=/bin/vi

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.old

gzip -9nf COPYRIGHT DIFFERENCES FAQ MAIL.FILTERING README TODO VERSION \
	ZSH.COMPLETION $RPM_BUILD_ROOT%{_mandir}/*/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -d %{_bindir}/mh -a ! -L %{_bindir}/mh ] ; then
	ln -s . %{_bindir}/mh
fi
if [ ! -d %{_usrlibdir}/mh -a ! -L %{_usrlibdir}/mh ] ; then
	ln -s nmh %{_usrlibdir}/mh
fi
if [ -d /etc/smrsh -a ! -L /etc/smrsh/slocal ] ; then
	ln -sf %{_libdir}/slocal /etc/smrsh/slocal
fi

%triggerpostun -- mh, nmh <= 0.27-7
if [ ! -d %{_bindir}/mh -a ! -L %{_bindir}/mh ] ; then
	ln -s . %{_bindir}/mh
fi
if [ ! -d %{_usrlibdir}/mh -a ! -L %{_usrlibdir}/mh ] ; then
	ln -s nmh %{_usrlibdir}/mh
fi

%preun
if [ $1 = 0 ]; then
	[ ! -L %{_bindir}/mh ] || rm -f %{_bindir}/mh
	[ ! -L %{_usrlibdir}/mh ] || rm -f %{_usrlibdir}/mh
	[ ! -d /etc/smrsh -a -L /etc/smrsh/slocal ] || rm -f /etc/smrsh/slocal
fi


%files
%defattr(644,root,root,755)
%doc {COPYRIGHT,DIFFERENCES,FAQ,MAIL.FILTERING,README}.gz
%doc {TODO,VERSION,ZSH.COMPLETION}.gz
%dir %{_libdir}
%dir %{_sysconfdir}
%config %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%{_mandir}/*/*
