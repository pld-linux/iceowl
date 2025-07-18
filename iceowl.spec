# TODO
# - kill -O overriding our optflags
# - Package: calendar-timezones
# - Package: calendar-google-provider
# - Package: iceowl-extension
#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnomeui		# disable gnomeui support
%bcond_without	gnomevfs	# disable GNOME comp. (gconf+libgnome+gnomevfs) and gnomevfs ext.
%bcond_without	gnome		# disable all GNOME components (gnome+gnomeui+gnomevfs)

%if %{without gnome}
%undefine	with_gnomeui
%undefine	with_gnomevfs
%endif

Summary:	Standalone Calendar Application
Summary(pl.UTF-8):	Samodzielny kalendarz
Name:		iceowl
Version:	0.9
Release:	0.1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/calendar/sunbird/releases/%{version}/source/lightning-sunbird-%{version}-source.tar.bz2
# Source0-md5:	7757ffefd4a30bcc1497b93b3dc6c0ce
Source1:	%{name}.sh
Source2:	%{name}.desktop
Patch0:		mozilla-install.patch
Patch1:		libpng14.patch
Patch2:		elif.patch
URL:		http://www.mozilla.org/projects/sunbird/
%{?with_gnomevfs:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	cairo-devel >= 1.2.0
BuildRequires:	freetype-devel
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
%{?with_gnomevfs:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnomeui:BuildRequires:	libgnomeui-devel >= 2.2.0}
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
Requires:	cairo >= 1.2.0
Requires:	nspr >= 1:4.6.3
Requires:	nss >= 1:3.11.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# firefox/thunderbird/seamonkey/sunbird provide their own versions
%define		_noautoreqdep		libgkgfx.so libgtkxtbin.so libxpcom_compat.so libxpcom_core.so libgfxpsshar.so libxpistub.so
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# we don't want these to satisfy xulrunner-devel
%define		_noautoprov		libgtkembedmoz.so libmozjs.so libxpcom.so
# and as we don't provide them, don't require either
%define		_noautoreq		%{_noautoprov}

%define		specflags	-fno-strict-aliasing

%description
Iceowl is a Mozilla Based Calendar application. The goal is to produce
a cross platform stand alone Calendar application using the XUL user
interface language. Iceowl leaves a somewhat smaller memory footprint
than the Mozilla suite.

%prep
%setup -q -c
cd mozilla
%patch -P0 -p1
%patch -P1 -p2
%patch -P2 -p1

%build
cd mozilla
cat << 'EOF' > .mozconfig
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}

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
ac_add_options --disable-optimize
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --enable-debugger-info-modules
ac_add_options --enable-crash-on-assert
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
ac_add_options --disable-logging
ac_add_options --enable-optimize="%{rpmcflags} -Os"
%endif
ac_add_options --disable-strip
ac_add_options --disable-strip-libs
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with gnomeui}
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomeui
%endif
%if %{with gnomevfs}
ac_add_options --enable-gnomevfs
%else
ac_add_options --disable-gnomevfs
%endif
ac_add_options --disable-crashreporter
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --disable-xprint
ac_add_options --enable-canvas
#ac_add_options --enable-libxul
ac_add_options --enable-pango
ac_add_options --enable-startup-notification
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-lcms
ac_add_options --enable-system-sqlite
#ac_add_options --enable-xft
ac_add_options --enable-xinerama
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
ac_add_options --disable-pedantic
ac_add_options --disable-xterm-updates
ac_add_options --enable-application=calendar
ac_add_options --with-x
ac_add_options --disable-freetype2
ac_add_options --enable-ipcd
ac_add_options --enable-ldap-experimental
ac_add_options --enable-storage

ac_cv_visibility_pragma=no
EOF

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}

%{__make} -C obj-%{_target_cpu}/xpinstall/packager stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/js $RPM_BUILD_ROOT%{_datadir}/%{name}/js
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/extensions $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/js $RPM_BUILD_ROOT%{_libdir}/%{name}/js
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res

sed 's,@LIBDIR@,%{_libdir},' %{SOURCE1} > $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/sunbird
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
cp -a calendar/sunbird/app/mozicon128.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

# it will complain on startup about bad chrome install otherwise
touch $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}/chrome.manifest

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
for d in chrome defaults extensions greprefs icons js res; do
	if [ -d %{_libdir}/%{name}/$d ] && [ ! -L %{_libdir}/%{name}/$d ]; then
		install -d %{_datadir}/%{name}
		mv %{_libdir}/%{name}/$d %{_datadir}/%{name}/$d
	fi
done
exit 0

#%post
#%{_sbindir}/firefox-chrome+xpcom-generate

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/sunbird

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%{_libdir}/%{name}/components/*.js
%{_libdir}/%{name}/components/*.xpt

%{_libdir}/%{name}/LICENSE
%{_libdir}/%{name}/README.txt

%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/m*
%attr(755,root,root) %{_libdir}/%{name}/s*
%attr(755,root,root) %{_libdir}/%{name}/reg*
%attr(755,root,root) %{_libdir}/%{name}/x*

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/js
%{_datadir}/%{name}/res
%dir %{_datadir}/%{name}/extensions

# the signature of the default theme
%{_datadir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%{_datadir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}
%{_datadir}/%{name}/extensions/calendar-timezones@mozilla.org

%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}.desktop

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/extensions
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/js
%{_libdir}/%{name}/res
