# If KF7 still provides these icons, then their installation should then
# be disabled in KF6 builds.
%global install_icons 1
# for compatibility, to be removed once Kexi (and others?) are ported
%global install_rcc 1

%global  kf_version 6.6.0

Name:    kf6-breeze-icons
Summary: Breeze icon theme library
Version: 6.18.0
Release: 0%{?dist}

# skladnik.svg is CC-BY-SA-4.0
# folder-edit-sign-encrypt.svg is LGPL-2.1-or-later
# src/lib/ is LGPL-2.0-or-later
# all other icons are LGPL-3.0-or-later
License: LGPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-3.0-or-later AND CC-BY-SA-4.0
URL:     https://api.kde.org/frameworks/breeze-icons/html/
Source0:    %{name}-%{version}.tar.bz2
Provides:      breeze-icon-theme

BuildRequires: extra-cmake-modules >= %{kf_version}
BuildRequires: kf6-rpm-macros
BuildRequires: qt6-qtbase-devel

# for generate-24px-versions.py
BuildRequires: python3-lxml

Requires:      qt6-qtsvg

%description
%{summary}.

%if %{with install_icons}
%package -n breeze-icon-theme
Summary:     Breeze icon theme
# analysis above
License:     LGPL-2.1-or-later AND LGPL-3.0-or-later AND CC-BY-SA-4.0
BuildArch:   noarch
# upstream name
Provides:    breeze-icons = %{version}-%{release}
# package changed arch
Obsoletes:   breeze-icon-theme < 6.3.0-2
%description -n breeze-icon-theme
%{summary}.
%endif

%if %{with install_rcc}
%package -n breeze-icon-theme-rcc
Summary:     Breeze Qt resource files
# analysis above
License:     LGPL-2.1-or-later AND LGPL-3.0-or-later AND CC-BY-SA-4.0
BuildArch:   noarch
# package changed arch
Obsoletes:   breeze-icon-theme-rcc < 6.3.0-2
%description -n breeze-icon-theme-rcc
%{summary}.
%endif

%package     devel
Summary:     Breeze icon theme development files
Requires:    %{name} = %{version}-%{release}
# renamed for https://pagure.io/fedora-kde/SIG/issue/530
Provides:    breeze-icon-theme-devel = %{version}-%{release}
Obsoletes:   breeze-icon-theme-devel < 6.3.0-2
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
%cmake_kf6 \
  -DBINARY_ICONS_RESOURCE:BOOL=%{?with_install_rcc:ON}%{!?with_install_rcc:OFF} \
  -DSKIP_INSTALL_ICONS:BOOL=%{?with_install_icons:OFF}%{!?with_install_icons:ON} \
  %{nil}

%cmake_build


%install
%cmake_install


%files
%license COPYING.LIB
%doc README.md
%{_kf6_libdir}/libKF6BreezeIcons.so.*

%files devel
%{_kf6_includedir}/BreezeIcons/
%{_kf6_libdir}/cmake/KF6BreezeIcons/
%{_kf6_libdir}/libKF6BreezeIcons.so

%if %{with install_icons}
%files -n breeze-icon-theme
%license COPYING-ICONS
%doc README.md
%ghost %{_datadir}/icons/breeze/icon-theme.cache
%{_datadir}/icons/breeze/index.theme
%{_datadir}/icons/breeze/*/
%ghost %{_datadir}/icons/breeze-dark/icon-theme.cache
%{_datadir}/icons/breeze-dark/index.theme
%{_datadir}/icons/breeze-dark/*/
%exclude %{_datadir}/icons/breeze/breeze-icons.rcc
%endif

%if %{with install_rcc}
%files -n breeze-icon-theme-rcc
%{_datadir}/icons/breeze/breeze-icons.rcc
%endif
