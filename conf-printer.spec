#
#  This file is part of Conf File Printer.
#
#  Conf File Printer is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Conf File Printer is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Conf File Printer. If not, see <http://www.gnu.org/licenses/>.
#
##


Name:           conf-printer
Version:        0.0
Release:        %( echo "0" )
Summary:        This tool intended to assist in configuration file usage in Shell scripts - get an option value from YAML file.

License:        GPL 3
URL:            http://github.com
Source0:        http://github.com/.../%{name}-%{version}.tar.gz

requires:       python python-argparse python-libs PyYAML

BuildArch:      noarch

%global __os_install_post %{nil}

%description
This is a tool to wrap around 'rsync' between remote and local nodes. Arguments are passed via configuration files.

%prep
%setup -q

%build
%configure

%install
%make_install

%post
true

%preun
rm -rf /opt/%{name}

%files
/opt/%{name}

## There is 'changelog' section below. It's format is strict.
## New change log insertions can be done using command:
##    rpmdev-bumpspec --comment="Descriptive text." --userstring="A Name <a-name@github.com>" this.spec
%changelog
* Sun Mar 20 2016 Prairies Ariea <prairies.ariea@localhost> 0.0-0
- Package created.
