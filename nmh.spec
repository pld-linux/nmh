Summary:	A capable mail handling system with a command line interface
Summary(pl):	System obs³ugi poczty z interfejsem z linii poleceñ
Name:		nmh
Version:	1.2
Release:	3
License:	Freeware
Group:		Applications/Mail
Source0:	http://savannah.nongnu.org/download/nmh/%{name}-%{version}.tar.gz
# Source0-md5:	aeebb9bef9ede7232f52c3a3b693eccc
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-build.patch
URL:		http://savannah.nongnu.org/projects/nmh/
BuildRequires:	gdbm-devel
BuildRequires:	ncurses-devel
Provides:	mh
Obsoletes:	mh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
%configure \
	--with-locking=fcntl \
	--with-mts=sendmail \
	--enable-pop
%{__make} \
	bindir=%{_bindir}/mh \
	libdir=%{_libdir}/mh \
	etcdir=%{_sysconfdir}/nmh

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SETGID_MAIL= \
	bindir=%{_bindir}/mh \
	libdir=%{_libdir}/mh \
	etcdir=%{_sysconfdir}/nmh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog README docs/{COMP*,FAQ,MAIL*,README.*,TODO}
%dir %{_bindir}/mh
%dir %{_libdir}/mh
%attr(755,root,root) %{_bindir}/mh/*
%attr(755,root,root) %{_libdir}/mh/*
%dir %{_sysconfdir}/nmh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nmh/*
%{_mandir}/*/*
