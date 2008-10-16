%define enable_manpage 0

Summary: Moblin System Settings
Name: moblin-settings
Version: 2.21
Release: %mkrel 2.18
URL: http://moblin.org
Source0: http://moblin.org/repos/releases/%{name}-%{version}.tar.gz
Patch0: add-gen-manpage-option.patch
License: GPLv2
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(pre): /usr/bin/polkit-auth
Requires(postun): coreutils

BuildRequires: glib2-devel >= 2.6.0
BuildRequires: dbus-devel  >= 0.90
BuildRequires: dbus-glib-devel >= 0.70
BuildRequires: dbus-glib >= 0.70
BuildRequires: polkit-devel >= 0.7
BuildRequires: alsa-lib-devel >= 0.9.0
BuildRequires: hal-devel >= 0.5.8
#BuildRequires: libX11-devel -- UNCOMMENT FOR TOUCHSCREEN
%if %{enable_manpage}
BuildRequires: docbook-utils
%endif

Requires: dbus >= 0.90
Requires: dbus-glib >= 0.70
Requires: glib2 >= 2.6.0
Requires: ConsoleKit >= 0.2.0
Requires: PolicyKit >= 0.7
Requires: hal >= 0.5.8

BuildRequires: autoconf, automake, libtool

%description
Moblin System Daemon is a daemon used to manage hardware settings
in a GUI agnostic manner

%package devel
Summary: Libraries and headers for Moblin System Daemon
Group: Development/C
Requires: %{name} = %{version}-%{release}
Requires: dbus-devel >= 0.90
Requires: pkgconfig

%description devel
Headers and libraries for Moblin System Daemon.

%prep
%setup -q -n %{name}-%{version}
%if !%{enable_manpage}
%patch0 -p1 -b .manpage
%endif

%build
./autogen.sh
%configure                                  \
    --disable-touchscreen                   \
%if !%{enable_manpage}
    --disable-man                           \
%endif
    --sysconfdir=/etc                       \
    prefix=/usr

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add moblin-kernel-modules
/sbin/chkconfig --add moblin-system-daemon

%preun
if [ $1 = 0 ]; then
    service moblin-system-daemon stop > /dev/null 2>&1
    /sbin/chkconfig --del moblin-system-daemon
    /sbin/chkconfig --del moblin-kernel-modules
fi

%files
%defattr(-,root,root,-)

%dir %{_sysconfdir}/dbus-1/system.d
%config %{_sysconfdir}/dbus-1/system.d/moblin-system-daemon.conf
%config %{_sysconfdir}/init.d/moblin-system-daemon
%config %{_sysconfdir}/init.d/moblin-kernel-modules

%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/system-services
%{_datadir}/dbus-1/system-services/org.moblin.SystemDaemon.service
%{_sbindir}/moblin-system-daemon
# %{_bindir}/moblin-touchdump -- UNCOMMENT FOR TOUCHSCREEN
%{_bindir}/moblin-system-tool
%if %{enable_manpage}
%doc %{_mandir}/man1/*
%endif

%files devel
%defattr(-,root,root,-)

%{_libdir}/pkgconfig/moblin-system-daemon.pc

%dir %{_includedir}/moblin-2.0/moblin-settings
%{_includedir}/moblin-2.0/moblin-settings/moblin-system-client.h

