# TODO:
# - update to 1.1RC1 - project moved to savannah.nongnu.org
#
Summary:	A capable mail handling system with a command line interface
Summary(pl):	System obs³ugi poczty z interfejsem z linii poleceñ
Name:		nmh
Provides:	mh
Version:	1.0.4
Release:	6
License:	Freeware
Group:		Applications/Mail
Source0:	ftp://ftp.math.gatech.edu/pub/nmh/%{name}-%{version}.tar.gz
# Source0-md5:	caff7fbd5588d08701413fe4eaa87e87
Patch0:		%{name}-config.patch
Patch1:		%{name}-buildroot.patch
Patch2:		%{name}-compat21.patch
Patch3:		%{name}-bug7246.patch
BuildRequires:	gdbm-devel
BuildRequires:	ncurses-devel
Requires:	smtpdaemon
Requires:	/bin/vi
Obsoletes:	mh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_nmhlibdir	%{_libdir}/nmh
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

%description -l pl
Nmh jest systemem pocztowym bazuj±cym na systemie MH, w wiêkszo¶ci
kompatybilnym i mog±cym zast±piæ MH. Nmh nie jest pojedynczym
programem - sk³ada siê z wielu prostych programów s³u¿±cych do jednej
czynno¶ci (wysy³ania, odbierania, zapisywania, odczytywania...). Mo¿na
swobodnie umieszczaæ polecenia nmh miêdzy innymi poleceniami pow³oki
lub pisaæ skrypty korzystaj±ce z poleceñ nmh. Je¶li chcesz u¿ywaæ nmh
jako prawdziwego programu pocztowego, pomy¶l o zainstalowaniu exmh,
daj±cego interfejs u¿ytkownika - samo nmh mo¿na obs³ugiwaæ tylko z
linii poleceñ.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure2_13 \
	--with-editor=/bin/vi

%{__make} LIBS="-lgdbm -lgdbm_compat"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT SETGID_MAIL=

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.old

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -d %{_bindir}/mh -a ! -L %{_bindir}/mh ] ; then
	ln -sf . %{_bindir}/mh
fi
if [ ! -d %{_libdir}/mh -a ! -L %{_libdir}/mh ] ; then
	ln -sf nmh %{_libdir}/mh
fi
if [ -d /etc/smrsh -a ! -L /etc/smrsh/slocal ] ; then
	ln -sf %{_nmhlibdir}/slocal /etc/smrsh/slocal
fi

%triggerpostun -- mh, nmh <= 0.27-7
if [ ! -d %{_bindir}/mh -a ! -L %{_bindir}/mh ] ; then
	ln -sf . %{_bindir}/mh
fi
if [ ! -d %{_libdir}/mh -a ! -L %{_libdir}/mh ] ; then
	ln -sf nmh %{_libdir}/mh
fi

%preun
if [ "$1" = "0" ]; then
	[ ! -L %{_bindir}/mh ] || rm -f %{_bindir}/mh
	[ ! -L %{_libdir}/mh ] || rm -f %{_libdir}/mh
	[ ! -d /etc/smrsh -a -L /etc/smrsh/slocal ] || rm -f /etc/smrsh/slocal
fi

%files
%defattr(644,root,root,755)
%doc COPYRIGHT DIFFERENCES FAQ MAIL.FILTERING README TODO VERSION
%dir %{_nmhlibdir}
%dir %{_sysconfdir}
%config %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_nmhlibdir}/*
%{_mandir}/*/*
