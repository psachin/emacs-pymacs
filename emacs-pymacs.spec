%global pkg pymacs
%global sum Emacs and Python integration framework
%global lang C.UTF-8

Name:           emacs-%{pkg}
Version:        0.25
Release:        8%{?dist}
Summary:        %{sum}
Group:          Development/Libraries
License:        GPLv2+
URL:            https://github.com/pinard/Pymacs
Source0:        https://github.com/pinard/Pymacs/archive/v0.25.tar.gz
Source1:        %{pkg}-init.el

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python2-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# for tests
BuildRequires:  emacs
# to generate pdf
BuildRequires:  python-docutils
BuildRequires:  python3-docutils
BuildRequires:  texlive-latex-bin-bin
BuildRequires:  texlive-texconfig
BuildRequires:  texlive-metafont-bin
BuildRequires:  texlive-cm
BuildRequires:  texlive-cmap
BuildRequires:  texlive-ec
BuildRequires:  texlive-times
BuildRequires:  texlive-pdftex-def
BuildRequires:  texlive-pslatex
BuildRequires:  texlive-courier
BuildRequires:  texlive-dvips
BuildRequires:  texlive-amsfonts

Requires:       python2
Requires:       python3
Requires:       emacs(bin) >= %{_emacs_version}

%description
Pymacs is a powerful tool which can be started from Emacs and allows
both-way communication between Emacs Lisp and Python. Pymacs aims
Python as an extension language for Emacs rather than the other way
around. For more info, visit %{url}.


%package -n %{name}-el
Summary:  Elisp source files for %{pkg} under GNU Emacs
Group:  Development/Libraries
Requires:  %{name} = %{version}-%{release}

%description -n %{name}-el
This package contains the elisp source files for %{pkg} under GNU
Emacs. You do not need to install this package to run %{name}.


%prep
%setup -q -n Pymacs-%{version}

# make sure we are using right interpreter to build
sed -i 's:^PYTHON =.*:PYTHON=%{__python}:g' Makefile
sed -i 's:^PYTHON =.*:PYTHON=%{__python3}:g' Makefile
sed -i 's:except ProtocolError, exception:except ProtocolError as exception:g' Pymacs.py.in
sed -i 's:rst2latex.py:rst2latex:' Makefile

# remove shebangs from library
sed -i '/^#!.*/ {d}' Pymacs.py.in
sed -i '/^#!.*/ {d}' pppp

# remove executable bits from docs
chmod -x contrib/rebox/rebox


%build
# https://github.com/pinard/Pymacs/issues/57
export LANG=%{lang}
make %{?_smp_mflags} all pymacs.pdf
%{_emacs_bytecompile} %{pkg}.el


%install
%{__python} setup.py install --skip-build --root %{buildroot}
export LANG=%{lang}
%py3_install

install -dm 755 %{buildroot}/%{_emacs_sitelispdir}/
install -pm 644 %{pkg}.elc %{buildroot}/%{_emacs_sitelispdir}/
install -pm 644 %{pkg}.el %{buildroot}/%{_emacs_sitelispdir}/

# install startup file
install -dm 755 %{buildroot}/%{_emacs_sitestartdir}/
install -pm 644 %{SOURCE1} %{buildroot}/%{_emacs_sitestartdir}/


%check
export LANG=%{lang}
make check


%files
%doc README THANKS contrib TODO pymacs.pdf pymacs.rst
%license COPYING
%{python_sitelib}/Pymacs.py*
%{python_sitelib}/*.egg-info
%{python3_sitelib}/Pymacs.py*
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/__pycache__/Pymacs*
%{_emacs_sitelispdir}/%{pkg}.elc
%{_emacs_sitestartdir}/*.el

%files -n %{name}-el
%{_emacs_sitelispdir}/%{pkg}.el

%changelog
* Thu June 09 2016 Sachin Patil <psachin@redhat.com> - 0.25-8
- Python3 support

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.25-3
- Fix BuildRequires to pull in proper LaTeX packages

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.25-1
- Update to latest upstream version (0.25)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.23-3
- Fix license tag to GPLv2+
- Use name macro where appropriate
- Use correct emacs requires

* Tue May 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.23-2
- Rename to emacs-pymacs
- Use emacs macros
- Byte-compile elisp source and put sources into subpackage

* Wed May  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.23-1
- Initial version of the package
