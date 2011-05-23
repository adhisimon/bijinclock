Name: bijinclock
Version: 0.9.2
Release: 1
BuildArch: noarch
Group: Applications/Internet
Summary: Clock with beautiful women photo
License: GPLv2
URL: http://adhisimon.or.id/bijinclock/
Source0: http://adhisimon.or.id/bijinclock/bijinclock-0.9.2.tar.bz2
%description
Bijin Clock is a clock program. It display photos of beautiful women
every minute.

Currently it support photos from http://www.clockm.com/

Require: python

%prep
%setup -q

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m 777 bijinclock $RPM_BUILD_ROOT/%{_bindir}/bijinclock
desktop-file-install --vendor="adhisimon" --dir=%{buildroot}%{_datadir}/applications %{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/bijinclock
%{_datadir}/applications/adhisimon-%{name}.desktop

%changelog
* Tue May 24 2011 Adhidarma Hadiwinot <gua@adhisimon.or.id>
- Initial version
