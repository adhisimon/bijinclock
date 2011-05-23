Name: bijinclock
Version: 0.9
Release: 2
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

%prep
%setup -q

%install
install -m 777 bijinclock $RPM_BUILD_ROOT/%{_bindir}

%changelog
* Tue May 24 2011 Adhidarma Hadiwinot <gua@adhisimon.or.id>
- Initial version
