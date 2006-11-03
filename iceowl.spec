# TODO: kill -O overriding our optflags
#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Mozilla Sunbird - standalone calendar application
Summary(pl):	Mozilla Sunbird - samodzielny kalendarz
Name:		mozilla-sunbird
Version:	0.3
Release:	0.1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/calendar/sunbird/releases/%{version}/source/sunbird-%{version}.source.tar.bz2
# Source0-md5:	5579069a44e382bb963e3bbf6897a366
URL:		http://www.mozilla.org/projects/sunbird/
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.2.0
BuildRequires:	freetype-devel
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libgnome-devel >= 2.0
BuildRequires:	libgnomeui-devel >= 2.2.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.7
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6.3
BuildRequires:	nss-devel >= 1:3.11.3-3
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires:	%{name}-lang-resources = %{version}
Requires:	cairo >= 1.2.0
Requires:	nspr >= 1:4.6.3
Requires:	nss >= 1:3.11.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sunbirddir	%{_libdir}/mozilla-sunbird

%description
The Sunbird Project is a cross platform standalone calendar
application based on Mozilla's XUL user interface language.

%description -l pl
Projekt Sunbird to wieloplatformowa aplikacja bed�ca samodzielnym
kalendarzem, oparta na j�zyku interfejsu u�ytkownika XUL.

%package devel
Summary:	Headers for developing programs that will use Mozilla Sunbird
Summary(pl):	Mozilla Sunbird - pliki nag��wkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	nspr-devel >= 1:4.6.3
Obsoletes:	mozilla-devel

%description devel
Mozilla Sunbird development package.

%description devel -l pl
Pliki nag��wkowe kalendarza Mozilla Sunbird.

%prep
%setup -q -c

%build
cd mozilla

cat << 'EOF' > .mozconfig
# Options for 'configure' (same as command-line options).
ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --disable-optimize
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
ac_add_options --enable-optimize="%{rpmcflags}"
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-@CONFIG_GUESS@
ac_add_options --disable-freetype2
ac_add_options --disable-logging
ac_add_options --disable-old-abi-compat-wrappers
ac_add_options --enable-application=calendar
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-elf-dynstr-gc
ac_add_options --enable-image-decoders=all
ac_add_options --enable-image-encoders=all
ac_add_options --enable-ipcd
ac_add_options --enable-ldap-experimental
ac_add_options --enable-native-uconv
ac_add_options --enable-safe-browsing
ac_add_options --enable-storage
ac_add_options --enable-system-cairo
ac_add_options --enable-url-classifier
ac_add_options --enable-xft
ac_add_options --with-default-mozilla-five-home=%{_sunbirddir}
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-java-bin-path=/usr/bin
ac_add_options --with-java-include-path=/usr/include
ac_add_options --with-qtdir=/usr
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
EOF

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
#install -d \
#	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
#	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
#	$RPM_BUILD_ROOT{%{_pkgconfigdir}}

%{__make} -C mozilla install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#%{_sbindir}/firefox-chrome+xpcom-generate
#
#%postun
#if [ "$1" = "0" ]; then
#	rm -rf %{_sunbirddir}/chrome/overlayinfo
#	rm -f  %{_sunbirddir}/chrome/*.rdf
#	rm -rf %{_sunbirddir}/components
#	rm -rf %{_sunbirddir}/extensions
#fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sunbird
%dir %{_sunbirddir}
%{_sunbirddir}/res
%dir %{_sunbirddir}/components
%attr(755,root,root) %{_sunbirddir}/components/*.so
%{_sunbirddir}/components/*.js
%{_sunbirddir}/components/*.xpt
%dir %{_sunbirddir}/plugins
%attr(755,root,root) %{_sunbirddir}/plugins/*.so
%{_sunbirddir}/searchplugins
%{_sunbirddir}/icons
%{_sunbirddir}/defaults
%{_sunbirddir}/greprefs
%dir %{_sunbirddir}/extensions
%attr(755,root,root) %{_sunbirddir}/*.so
%attr(755,root,root) %{_sunbirddir}/*.sh
%attr(755,root,root) %{_sunbirddir}/m*
%attr(755,root,root) %{_sunbirddir}/f*
%attr(755,root,root) %{_sunbirddir}/reg*
%attr(755,root,root) %{_sunbirddir}/x*
%{_datadir}/idl/sunbird-%{version}
#%{_pixmapsdir}/*
#%{_desktopdir}/*

%dir %{_sunbirddir}/chrome
%{_sunbirddir}/chrome/*.jar
%{_sunbirddir}/chrome/*.manifest
%dir %{_sunbirddir}/chrome/icons
%{_sunbirddir}/chrome/icons/default

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sunbird-config
%{_includedir}/sunbird-%{version}
%{_pkgconfigdir}/sunbird-*.pc
