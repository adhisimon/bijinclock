Name: bijinclock
Version: 0.9.6
Release: 1
BuildArch: noarch
Group: Applications/Internet
Summary: Clock with beautiful women photo
License: GPLv2
URL: https://github.com/adhisimon/bijinclock
Source0: https://github.com/downloads/adhisimon/bijinclock/bijinclock-%{version}.tar.bz2
BuildRequires: desktop-file-utils
Requires: python pygtk2 coreutils make

%description
Bijin Clock is a clock program. It display photos of beautiful women
every minute.

Currently it support photos from http://www.clockm.com/

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
#mkdir -p $RPM_BUILD_ROOT/%{_bindir}
#install -m 755 bijinclock $RPM_BUILD_ROOT/%{_bindir}/bijinclock
make DESTDIR=$RPM_BUILD_ROOT BINDIR=/usr/bin DATADIR=/usr/share install
desktop-file-install --vendor="adhisimon" --dir=%{buildroot}%{_datadir}/applications %{name}.desktop
rm -f %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/bijinclock
%{_datadir}/applications/adhisimon-%{name}.desktop
%doc AUTHOR COPYING INSTALL README

%changelog
* Tue May 24 2011 Adhidarma Hadiwinoto <gua@adhisimon.or.id>
- Initial version
