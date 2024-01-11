%global uid 133
%global username bacula

%if 0%{?rhel} && ! 0%{?epel}
%bcond_with nagios
%else
%bcond_without nagios
%endif

Name:               bacula
Version:            11.0.1
Release:            5%{?dist}
Summary:            Cross platform network backup for Linux, Unix, Mac and Windows
# See LICENSE for details
License:            AGPLv3 with exceptions
URL:                http://www.bacula.org

Source0:            http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Source2:            quickstart_postgresql.txt
Source3:            quickstart_mysql.txt
Source4:            quickstart_sqlite3.txt
Source5:            README.Redhat
Source6:            %{name}.logrotate
Source10:           %{name}-fd.service
Source11:           %{name}-dir.service
Source12:           %{name}-sd.service
Source15:           %{name}-fd.sysconfig
Source16:           %{name}-dir.sysconfig
Source17:           %{name}-sd.sysconfig
Source19:           https://salsa.debian.org/bacula-team/bacula/-/raw/master/debian/additions/bacula-tray-monitor.png#/bacula-tray-monitor.png

Patch1:             %{name}-openssl.patch
Patch2:             %{name}-queryfile.patch
Patch3:             %{name}-sqlite-priv.patch
Patch4:             %{name}-bat-build.patch
Patch5:             %{name}-seg-fault.patch
Patch6:             %{name}-logwatch.patch
Patch7:             %{name}-non-free-code.patch
Patch8:             %{name}-desktop.patch
Patch9:             %{name}-g++-options.patch
Patch10:            %{name}-install.patch
Patch11:            %{name}-docker-plugin.patch
# Original patch removed by mistake, upstream is not willing to add it again:
# http://www.bacula.org/git/cgit.cgi/bacula/commit/?h=Branch-7.0&id=51b3b98fb77ab3c0decee455cc6c4d2eb3c5303a
# Without this, there is no library providing the correct shared object name
# required by the daemons.
# http://bugs.bacula.org/view.php?id=2084
Patch12:            %{name}-autoconf.patch
Patch13:            %{name}-build-cdp-plugin.patch
Patch14:            %{name}-nagios.patch
Patch15:            %{name}-use-crypto-from-openssl.patch

BuildRequires:      desktop-file-utils
BuildRequires:      perl-generators
BuildRequires:      sed

BuildRequires:      autoconf
BuildRequires:      automake
BuildRequires:      gcc
BuildRequires:      gcc-c++
BuildRequires:      glibc-devel
BuildRequires:      libacl-devel
BuildRequires:      libstdc++-devel
BuildRequires:      libxml2-devel
BuildRequires:      libcap-devel
BuildRequires:      lzo-devel
BuildRequires:      make
BuildRequires:      ncurses-devel
BuildRequires:      openssl-devel
BuildRequires:      qt5-qtbase-devel
BuildRequires:      readline-devel
BuildRequires:      sqlite-devel
BuildRequires:      systemd
BuildRequires:      zlib-devel

%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:      mariadb-connector-c-devel
# https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules
BuildRequires:      perl-interpreter
%else
BuildRequires:      mysql-devel
BuildRequires:      perl
BuildRequires:      tcp_wrappers-devel
%endif

%if 0%{?fedora}
BuildRequires:      libpq-devel
%else
BuildRequires:      postgresql-devel
%endif

%description
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture and is efficient and relatively easy to
use, while offering many advanced storage management features that make it easy
to find and recover lost or damaged files.

%package libs
Summary:            Bacula libraries

%description libs
Bacula is a set of programs that allow you to manage the backup,
recovery, and verification of computer data across a network of
different computers. It is based on a client/server architecture.

This package contains basic Bacula libraries, which are used by all
Bacula programs.

%package libs-sql
Summary:            Bacula SQL libraries
Obsoletes:          bacula-libs-mysql <= 5.0.3
Obsoletes:          bacula-libs-sqlite <= 5.0.3
Obsoletes:          bacula-libs-postgresql <= 5.0.3
Provides:           bacula-libs-mysql = %{version}-%{release}
Provides:           bacula-libs-sqlite = %{version}-%{release}
Provides:           bacula-libs-postgresql = %{version}-%{release}

%description libs-sql
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the SQL Bacula libraries, which are used by Director and
Storage daemons. You have to select your preferred catalog library through the
alternatives system.

%package common
Summary:            Common Bacula files
Provides:           group(%username) = %uid
Provides:           user(%username) = %uid
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires(pre):      shadow-utils
Requires(postun):   shadow-utils

%description common
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains files common to all Bacula daemons.

%package director
Summary:            Bacula Director files
Requires:           bacula-common%{?_isa} = %{version}-%{release}
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           bacula-libs-sql%{?_isa} = %{version}-%{release}
# Director backends merged into core.
Provides:           bacula-director-common = %{version}-%{release}
Obsoletes:          bacula-director-common < 5.2.3-5
Provides:           bacula-director-mysql = %{version}-%{release}
Obsoletes:          bacula-director-mysql < 5.2.3-5
Provides:           bacula-director-sqlite = %{version}-%{release}
Obsoletes:          bacula-director-sqlite < 5.2.3-5
Provides:           bacula-director-postgresql = %{version}-%{release}
Obsoletes:          bacula-director-postgresql < 5.2.3-5

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description director
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the director files.

%package logwatch
Summary:            Bacula Director logwatch scripts
BuildArch:          noarch
Requires:           bacula-director = %{version}-%{release}
Requires:           logwatch

%description logwatch
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains logwatch scripts for Bacula Director.

%package storage
Summary:            Bacula storage daemon files
Requires:           bacula-common%{?_isa} = %{version}-%{release}
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           bacula-libs-sql%{?_isa} = %{version}-%{release}
Requires:           mt-st
Requires:           mtx
# Storage backends merged into core.
Provides:           bacula-storage-common = %{version}-%{release}
Obsoletes:          bacula-storage-common < 5.2.2-2
Provides:           bacula-storage-mysql = %{version}-%{release}
Obsoletes:          bacula-storage-mysql < 5.2.0
Provides:           bacula-storage-sqlite = %{version}-%{release}
Obsoletes:          bacula-storage-sqlite < 5.2.0
Provides:           bacula-storage-postgresql = %{version}-%{release}
Obsoletes:          bacula-storage-postgresql < 5.2.0

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description storage
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the storage daemon, the daemon responsible for writing
the data received from the clients onto tape drives or other mass storage
devices.

%package client
Summary:            Bacula backup client
Requires:           bacula-common%{?_isa} = %{version}-%{release}
Requires:           bacula-libs%{?_isa} = %{version}-%{release}

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description client
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the bacula client, the daemon running on the system to be
backed up.

%package console
Summary:            Bacula management console
Obsoletes:          bacula-console-wxwidgets <= 5.0.3
Requires:           bacula-libs%{?_isa} = %{version}-%{release}

%description console
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the command-line management console for the bacula backup
system.

%package console-bat
Summary:            Bacula bat console
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           dejavu-lgc-sans-fonts

%description console-bat
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the bat version of the bacula management console.

%package traymonitor
Summary:            Bacula system tray monitor
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           dejavu-lgc-sans-fonts

%description traymonitor
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This package contains the Gnome and KDE compatible tray monitor to monitor your
bacula server.

%package devel
Summary:            Bacula development files
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           bacula-libs-sql%{?_isa} = %{version}-%{release}

%description devel
Bacula is a set of programs that allow you to manage the backup, recovery, and
verification of computer data across a network of different computers. It is
based on a client/server architecture.

This development package contains static libraries and header files.

%if %{with nagios}
%package -n nagios-plugins-bacula
Summary:            Nagios Plugin - check_bacula
Requires:           bacula-libs%{?_isa} = %{version}-%{release}
Requires:           nagios-common%{?_isa}

%description -n nagios-plugins-bacula
Provides check_bacula support for Nagios.
%endif

%prep
%autosetup -p1

cp %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} .

# Regenerate configure
pushd autoconf
sed -i -r 's/(hardcode_into_libs)=.*$/\1=no/' libtool/libtool.m4
aclocal -I bacula-macros/ -I gettext-macros/ -I libtool/
popd
autoconf -I autoconf/ -o configure autoconf/configure.in

# Remove execution permissions from files we're packaging as docs later on
find updatedb -type f | xargs chmod -x

%build
export CFLAGS="%{optflags} -I%{_includedir}/ncurses"
export CPPFLAGS="%{optflags} -I%{_includedir}/ncurses"
export PATH="$PATH:%{_qt5_bindir}"

%configure \
    --disable-conio \
    --disable-rpath \
    --disable-s3 \
    --docdir=%{_datadir}/bacula \
    --enable-bat \
    --enable-batch-insert \
    --enable-build-dird \
    --enable-build-stored \
    --enable-includes \
    --enable-largefile \
    --enable-readline \
    --enable-smartalloc \
    --sysconfdir=%{_sysconfdir}/bacula \
    --with-basename=bacula \
    --with-bsrdir=%{_localstatedir}/spool/bacula \
    --with-dir-password=@@DIR_PASSWORD@@ \
    --with-fd-password=@@FD_PASSWORD@@ \
    --with-hostname=localhost \
    --with-logdir=%{_localstatedir}/log/bacula \
    --with-mon-dir-password=@@MON_DIR_PASSWORD@@ \
    --with-mon-fd-password=@@MON_FD_PASSWORD@@ \
    --with-mon-sd-password=@@MON_SD_PASSWORD@@ \
    --with-mysql \
    --with-openssl \
    --with-pid-dir=%{_localstatedir}/run \
    --with-plugindir=%{_libdir}/%{name} \
    --with-postgresql \
    --with-scriptdir=%{_libexecdir}/bacula \
    --with-sd-password=@@SD_PASSWORD@@ \
    --with-smtp-host=localhost \
    --with-sqlite3 \
    --with-subsys-dir=%{_localstatedir}/lock/subsys \
%if 0%{!?fedora} || 0%{!?rhel} > 7
    --with-tcp-wrappers \
%endif
    --with-working-dir=%{_localstatedir}/spool/bacula \
    --with-x

# Remove RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

pushd src/qt-console/
    %{?qmake_qt5}%{!?qmake_qt5:qmake-qt5} bat.pro
    pushd tray-monitor
        %{?qmake_qt5}%{!?qmake_qt5:qmake-qt5} tray-monitor.pro
    popd
popd

%make_build
%make_build -C src/tools/cdp-client
%if %{with nagios}
%make_build -C examples/nagios/check_bacula
%endif

pushd src/qt-console/
    %{?qmake_qt5}%{!?qmake_qt5:qmake-qt5} bat.pro
    pushd tray-monitor
        %{?qmake_qt5}%{!?qmake_qt5:qmake-qt5} tray-monitor.pro
    popd
popd

# Convert image to png for tray monitor icon
%install
%make_install
%make_install -C src/tools/cdp-client
%if %{with nagios}
%make_install -C examples/nagios/check_bacula
%endif

# This will be managed through alternatives, as it requires the name to NOT
# change between upgrades, so the versioned library name can not be used.
rm -f %{buildroot}%{_libdir}/libbaccats.so

# Bat
install -p -m 644 -D src/qt-console/images/bat_icon.png %{buildroot}%{_datadir}/pixmaps/bat_icon.png
install -p -m 644 -D scripts/bat.desktop %{buildroot}%{_datadir}/applications/bat.desktop
install -p -m 755 -D src/qt-console/.libs/bat %{buildroot}%{_sbindir}/bat

install -p -m 644 -D manpages/bacula-tray-monitor.1 %{buildroot}%{_mandir}/man1/bacula-tray-monitor.1
install -p -m 644 -D %{SOURCE19} %{buildroot}%{_datadir}/pixmaps/bacula-tray-monitor.png
install -p -m 644 -D scripts/bacula-tray-monitor.desktop %{buildroot}%{_datadir}/applications/bacula-tray-monitor.desktop

# Logrotate
mkdir -p %{buildroot}%{_localstatedir}/log/bacula
install -p -m 644 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/bacula

# Logwatch
install -p -m 755 -D scripts/logwatch/bacula %{buildroot}%{_sysconfdir}/logwatch/scripts/services/bacula
install -p -m 755 -D scripts/logwatch/applybaculadate %{buildroot}%{_sysconfdir}/logwatch/scripts/shared/applybaculadate
install -p -m 644 -D scripts/logwatch/logfile.bacula.conf %{buildroot}%{_sysconfdir}/logwatch/conf/logfiles/bacula.conf
install -p -m 644 -D scripts/logwatch/services.bacula.conf %{buildroot}%{_sysconfdir}/logwatch/conf/services/bacula.conf

# Systemd unit files
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 -D %{SOURCE10} %{buildroot}%{_unitdir}/bacula-fd.service
install -p -m 644 -D %{SOURCE11} %{buildroot}%{_unitdir}/bacula-dir.service
install -p -m 644 -D %{SOURCE12} %{buildroot}%{_unitdir}/bacula-sd.service

# Sysconfig
install -p -m 644 -D %{SOURCE15} %{buildroot}%{_sysconfdir}/sysconfig/bacula-fd
install -p -m 644 -D %{SOURCE16} %{buildroot}%{_sysconfdir}/sysconfig/bacula-dir
install -p -m 644 -D %{SOURCE17} %{buildroot}%{_sysconfdir}/sysconfig/bacula-sd

# Spool directory
mkdir -p %{buildroot}%{_localstatedir}/spool/bacula

# Remove stuff we do not need
rm -f %{buildroot}%{_libexecdir}/bacula/{bacula,bacula-ctl-*,startmysql,stopmysql,bconsole,make_catalog_backup}
rm -f %{buildroot}%{_sbindir}/bacula
rm -f %{buildroot}%{_mandir}/man8/bacula.8.gz
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_datadir}/bacula/{ChangeLog,INSTALL,LICENSE*,README,ReleaseNotes,VERIFYING,technotes}

# Fix up some perms so rpmlint does not complain too much
chmod 755 %{buildroot}%{_sbindir}/*
chmod 755 %{buildroot}%{_libdir}/%{name}/*
chmod 755 %{buildroot}%{_libexecdir}/bacula/*
chmod 644 %{buildroot}%{_libexecdir}/bacula/btraceback.*

%ldconfig_scriptlets libs

%post libs-sql
/usr/sbin/alternatives --install %{_libdir}/libbaccats.so libbaccats.so %{_libdir}/libbaccats-mysql.so 50
/usr/sbin/alternatives --install %{_libdir}/libbaccats.so libbaccats.so %{_libdir}/libbaccats-sqlite3.so 40
/usr/sbin/alternatives --install %{_libdir}/libbaccats.so libbaccats.so %{_libdir}/libbaccats-postgresql.so 60

# Fix for automatic selection of backends during upgrades
if readlink /etc/alternatives/libbaccats.so | grep --silent mysql || \
    readlink /etc/alternatives/bacula-dir | grep --silent mysql || \
    readlink /etc/alternatives/bacula-sd | grep --silent mysql; then
    /usr/sbin/alternatives --set libbaccats.so %{_libdir}/libbaccats-mysql.so
elif readlink /etc/alternatives/libbaccats.so | grep --silent sqlite || \
    readlink /etc/alternatives/bacula-dir | grep --silent sqlite || \
    readlink /etc/alternatives/bacula-sd | grep --silent sqlite; then
    /usr/sbin/alternatives --set libbaccats.so %{_libdir}/libbaccats-sqlite3.so
else
    /usr/sbin/alternatives --set libbaccats.so %{_libdir}/libbaccats-postgresql.so
fi
%{?ldconfig}

%preun libs-sql
if [ "$1" = 0 ]; then
    /usr/sbin/alternatives --remove libbaccats.so %{_libdir}/libbaccats-mysql.so
    /usr/sbin/alternatives --remove libbaccats.so %{_libdir}/libbaccats-sqlite3.so
    /usr/sbin/alternatives --remove libbaccats.so %{_libdir}/libbaccats-postgresql.so
fi

%ldconfig_postun libs-sql

%pre common
getent group %username >/dev/null || groupadd -g %uid -r %username &>/dev/null || :
getent passwd %username >/dev/null || useradd -u %uid -r -s /sbin/nologin \
    -d /var/spool/bacula -M -c 'Bacula Backup System' -g %username %username &>/dev/null || :
exit 0

%post client
%systemd_post %{name}-fd.service

%preun client
%systemd_preun %{name}-fd.service

%postun client
%systemd_postun_with_restart %{name}-fd.service

%post director
%systemd_post %{name}-dir.service

%preun director
%systemd_preun %{name}-dir.service

%postun director
%systemd_postun_with_restart %{name}-dir.service

%post storage
%systemd_post %{name}-sd.service

%preun storage
%systemd_preun %{name}-sd.service

%postun storage
%systemd_postun_with_restart %{name}-sd.service

%files libs
%license LICENSE
%doc AUTHORS ChangeLog SUPPORT ReleaseNotes LICENSE-FAQ LICENSE-FOSS
%{_libdir}/libbac-%{version}.so
%{_libdir}/libbaccfg-%{version}.so
%{_libdir}/libbacfind-%{version}.so
%{_libdir}/libbacsd-%{version}.so

%files libs-sql
# On Fedora 28 this gets recreated automatically even if the library is
# deleted in the install section.
# On EPEL 6 this is required until RPM assembly time or an error is given due
# to the missing library.
# So: leave the library in place until the very end and just exclude it.
%exclude %{_libdir}/libbaccats-%{version}.so
%{_libdir}/libbaccats-mysql-%{version}.so
%{_libdir}/libbaccats-mysql.so
%{_libdir}/libbaccats-postgresql-%{version}.so
%{_libdir}/libbaccats-postgresql.so
%{_libdir}/libbaccats-sqlite3-%{version}.so
%{_libdir}/libbaccats-sqlite3.so
%{_libdir}/libbacsql-%{version}.so

%files common
%doc README.Redhat quickstart_*
%config(noreplace) %{_sysconfdir}/logrotate.d/bacula
%dir %{_localstatedir}/log/bacula %attr(750, bacula, bacula)
%dir %{_localstatedir}/spool/bacula %attr(750, bacula, bacula)
%dir %{_libexecdir}/%{name}
%dir %{_sysconfdir}/%{name} %attr(755,root,root)
%{_libexecdir}/%{name}/btraceback.dbx
%{_libexecdir}/%{name}/btraceback.gdb
%{_libexecdir}/%{name}/bacula_config
%{_libexecdir}/%{name}/btraceback.mdb
%{_mandir}/man8/btraceback.8*
%{_sbindir}/btraceback

%files director
%doc updatedb examples/sample-query.sql
%config(noreplace) %{_sysconfdir}/bacula/bacula-dir.conf %attr(640,root,bacula)
%config(noreplace) %{_sysconfdir}/bacula/query.sql %attr(640,root,bacula)
%config(noreplace) %{_sysconfdir}/sysconfig/bacula-dir
%{_libexecdir}/%{name}/baculabackupreport
%{_libexecdir}/%{name}/create_bacula_database
%{_libexecdir}/%{name}/delete_catalog_backup
%{_libexecdir}/%{name}/drop_bacula_database
%{_libexecdir}/%{name}/drop_bacula_tables
%{_libexecdir}/%{name}/grant_bacula_privileges
%{_libexecdir}/%{name}/make_bacula_tables
%{_libexecdir}/%{name}/make_catalog_backup.pl
%{_libexecdir}/%{name}/update_bacula_tables
%{_libexecdir}/%{name}/create_mysql_database
%{_libexecdir}/%{name}/drop_mysql_database
%{_libexecdir}/%{name}/drop_mysql_tables
%{_libexecdir}/%{name}/grant_mysql_privileges
%{_libexecdir}/%{name}/make_mysql_tables
%{_libexecdir}/%{name}/update_mysql_tables
%{_libexecdir}/%{name}/create_sqlite3_database
%{_libexecdir}/%{name}/drop_sqlite3_database
%{_libexecdir}/%{name}/drop_sqlite3_tables
%{_libexecdir}/%{name}/grant_sqlite3_privileges
%{_libexecdir}/%{name}/make_sqlite3_tables
%{_libexecdir}/%{name}/update_sqlite3_tables
%{_libexecdir}/%{name}/create_postgresql_database
%{_libexecdir}/%{name}/drop_postgresql_database
%{_libexecdir}/%{name}/drop_postgresql_tables
%{_libexecdir}/%{name}/grant_postgresql_privileges
%{_libexecdir}/%{name}/make_postgresql_tables
%{_libexecdir}/%{name}/update_postgresql_tables
%{_mandir}/man1/bsmtp.1*
%{_mandir}/man8/bacula-dir.8*
%{_mandir}/man8/bregex.8*
%{_mandir}/man8/bwild.8*
%{_mandir}/man8/dbcheck.8*
%{_sbindir}/bacula-dir
%{_sbindir}/bdirjson
%{_sbindir}/bregex
%{_sbindir}/bsmtp
%{_sbindir}/bwild
%{_sbindir}/dbcheck
%{_unitdir}/bacula-dir.service

%files logwatch
%config(noreplace) %{_sysconfdir}/logwatch/conf/logfiles/bacula.conf
%config(noreplace) %{_sysconfdir}/logwatch/conf/services/bacula.conf
%{_sysconfdir}/logwatch/scripts/services/bacula
%{_sysconfdir}/logwatch/scripts/shared/applybaculadate

%files storage
%config(noreplace) %{_sysconfdir}/bacula/bacula-sd.conf %attr(640,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/bacula-sd
%{_libexecdir}/%{name}/disk-changer
%{_libexecdir}/%{name}/isworm
%{_libexecdir}/%{name}/mtx-changer
%{_libexecdir}/%{name}/mtx-changer.conf
%{_libexecdir}/%{name}/tapealert
%{_mandir}/man8/bacula-sd.8*
%{_mandir}/man8/bcopy.8*
%{_mandir}/man8/bextract.8*
%{_mandir}/man8/bls.8*
%{_mandir}/man8/bscan.8*
%{_mandir}/man8/btape.8*
%{_sbindir}/bacula-sd
%{_sbindir}/bcopy
%{_sbindir}/bextract
%{_sbindir}/bls
%{_sbindir}/bscan
%{_sbindir}/bsdjson
%{_sbindir}/btape
%{_unitdir}/bacula-sd.service

%files client
%config(noreplace) %{_sysconfdir}/bacula/bacula-fd.conf %attr(640,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/bacula-fd
%{_mandir}/man8/bacula-fd.8*
%{_libdir}/%{name}/bpipe-fd.so
%{_libdir}/%{name}/cdp-fd.so
%{_libdir}/%{name}/docker-fd.so
%{_sbindir}/bacula-fd
%{_sbindir}/bfdjson
%{_sbindir}/cdp-client
%{_unitdir}/bacula-fd.service

%files console
%config(noreplace) %{_sysconfdir}/bacula/bconsole.conf %attr(640,root,root)
%{_mandir}/man8/bconsole.8*
%{_sbindir}/bconsole
%{_sbindir}/bbconsjson

%files console-bat
%config(noreplace) %{_sysconfdir}/bacula/bat.conf %attr(640,root,root)
%{_datadir}/applications/bat.desktop
%{_datadir}/bacula/*.html
%{_datadir}/bacula/*.png
%{_datadir}/pixmaps/bat_icon.png
%{_mandir}/man1/bat.1*
%{_sbindir}/bat

%files traymonitor
%config(noreplace) %{_sysconfdir}/bacula/bacula-tray-monitor.conf %attr(640,root,root)
%{_datadir}/applications/bacula-tray-monitor.desktop
%{_datadir}/pixmaps/bacula-tray-monitor.png
%{_mandir}/man1/bacula-tray-monitor.1*
%{_sbindir}/bacula-tray-monitor

%files devel
%{_includedir}/bacula
%{_libdir}/libbac.so
%{_libdir}/libbaccfg.so
%{_libdir}/libbacfind.so
%{_libdir}/libbacsd.so
%{_libdir}/libbacsql.so

%if %{with nagios}
%files -n nagios-plugins-bacula
%{_libdir}/nagios/plugins/check_bacula
%endif

%changelog
* Tue Feb 15 2022 Pavel Cahyna <pcahyna@redhat.com> - 11.0.1-5
- Make nagios-plugin build conditional and disabled on RHEL to avoid
  generating this subpackage that has missing dependencies
- Fix flags for annobin in Qt tools (bat & tray-monitor) build
- Add a forgotten RHEL 8 patch to use openssl crypto (random numbers, hmac,
  hashing functions)
  Resolves: rhbz#1935458

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 11.0.1-4
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 16 2021 Mohan Boddu <mboddu@redhat.com> - 11.0.1-3
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 11.0.1-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Thu Feb 11 2021 Simone Caronni <negativo17@gmail.com> - 11.0.1-1
- Update to 11.0.1.

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 11.0.0-5
- rebuild for libpq ABI fix rhbz#1908268

* Thu Jan 28 2021 Simone Caronni <negativo17@gmail.com> - 11.0.0-4
- Remove leftover ImageMagick build requirement.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Simone Caronni <negativo17@gmail.com> - 11.0.0-2
- Build CDP plugin components.

* Tue Jan 12 2021 Simone Caronni <negativo17@gmail.com> - 11.0.0-1
- Update to 11.0.0.
- Enable Docker plugin.

* Tue Jan 12 2021 Simone Caronni <negativo17@gmail.com> - 9.6.7-1
- Update to 9.6.7.
- Drop support for building on CentOS/RHEL 6 and upgrades from version 2.4.
- Trim changelog.

* Wed Oct 07 2020 Simone Caronni <negativo17@gmail.com> - 9.6.6-1
- Update to 9.6.6.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Simone Caronni <negativo17@gmail.com> - 9.6.5-1
- Update to 9.6.5.

* Tue Mar 17 2020 Simone Caronni <negativo17@gmail.com> - 9.6.3-1
- Update to 9.6.3.

* Thu Mar 05 2020 Simone Caronni <negativo17@gmail.com> - 9.6.2-2
- Fix RHEL/CentOS 6 builds.

* Sat Feb 29 2020 Simone Caronni <negativo17@gmail.com> - 9.6.2-1
- Update to 9.6.2.

* Mon Feb 10 2020 Václav Doležal <vdolezal@redhat.com> - 9.4.4-4
- Fix FTBFS (#1799185)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 29 2019 Simone Caronni <negativo17@gmail.com> - 9.4.4-1
- Update to 9.4.4.

* Sat May 18 2019 Simone Caronni <negativo17@gmail.com> - 9.4.3-2
- SPEC file cleanups.

* Wed May 15 2019 Simone Caronni <negativo17@gmail.com> - 9.4.3-1
- Update to 9.4.3.

* Thu Apr 18 2019 Simone Caronni <negativo17@gmail.com> - 9.4.2-1
- Update to 9.4.2.

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 9.4.1-6
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 9.4.1-4
- Rebuilt for libcrypt.so.2 (#1666033)

* Sun Jan 13 2019 Simone Caronni <negativo17@gmail.com> - 9.4.1-3
- Build QT programs with QT 5 on RHEL/CentOS 7. Also, reduce the number of
  required QT packages for building.

* Sun Jan 13 2019 Simone Caronni <negativo17@gmail.com> - 9.4.1-2
- Add Debian patch to enable/disable S3 support at configure time.
- Disable S3 as it does not currently build:
  http://bugs.bacula.org/view.php?id=2446
- Update RPM macros.

* Sat Jan 12 2019 Simone Caronni <negativo17@gmail.com> - 9.4.1-1
- Update to 9.4.1.

* Sat Jan 12 2019 Simone Caronni <negativo17@gmail.com> - 9.4.0-1
- Update to 9.4.0.

* Sat Jan 12 2019 Simone Caronni <negativo17@gmail.com> - 9.2.1-2
- Make the build succeed also on supported RHEL and Fedora releases.
- Remove Fedora 27 references.
