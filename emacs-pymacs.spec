%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global pkg pymacs

Name:           emacs-%{pkg}
Version:        0.23
Release:        4%{?dist}
Summary:        Emacs and Python integration framework
Group:          Development/Libraries
License:        GPLv2+
URL:            http://pymacs.progiciels-bpi.ca/
# git clone https://github.com/pinard/Pymacs.git
# git archive --prefix="emacs-pymacs-0.23/" --format=tar v0.23 | xz > emacs-pymacs-0.23.tar.xz
Source0:        %{name}-%{version}.tar.xz
Source1:        %{pkg}-init.el

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
# to generate pdf
BuildRequires:  python-docutils
BuildRequires:  texlive-latex

# for tests
BuildRequires:  emacs

Requires:       python2
Requires:       emacs(bin) >= %{_emacs_version}


%package -n %{name}-el
Summary:	Elisp source files for %{pkg} under GNU Emacs
Group:          Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{name}-el
This package contains the elisp source files for %{pkg} under GNU Emacs. You
do not need to install this package to run %{name}. Install the %{name}
package to use %{pkg} with GNU Emacs.


%description
Pymacs is a powerful tool which, once started from Emacs, allows
both-way communication between Emacs Lisp and Python. Pymacs aims
Python as an extension language for Emacs rather than the other way
around, and this asymmetry is reflected in some design choices. Within
Emacs Lisp code, one may load and use Python modules. Python functions
may themselves use Emacs services, and handle Emacs Lisp objects kept
in Emacs Lisp space.


%prep
%setup -q
# make sure we are using right interpreter to build
sed -i 's:PYSETUP =.*:PYSETUP=%{__python} setup.py:g' Makefile
sed -i 's:rst2latex.py:rst2latex:' Makefile

# remove shebangs from library
sed -i '/#!.*/ {d}' Pymacs/pymacs.py __init__.py.in

# remove executable bits from docs
chmod -x contrib/rebox/rebox

%build
make %{?_smp_mflags} all pymacs.pdf
%{_emacs_bytecompile} %{pkg}.el

%check
make check

%install
%{__python} setup.py install --skip-build --root %{buildroot}

install -dm 755 %{buildroot}/%{_emacs_sitelispdir}/
install -pm 644 %{pkg}.elc %{buildroot}/%{_emacs_sitelispdir}/
install -pm 644 %{pkg}.el %{buildroot}/%{_emacs_sitelispdir}/

# install startup file
install -dm 755 %{buildroot}/%{_emacs_sitestartdir}/
install -pm 644 %{SOURCE1} %{buildroot}/%{_emacs_sitestartdir}/


%files
%doc COPYING README THANKS contrib TODO ChangeLog pymacs.pdf pymacs.rst
%{python_sitelib}/Pymacs/
%{python_sitelib}/*.egg-info
%{_emacs_sitelispdir}/%{pkg}.elc
%{_emacs_sitestartdir}/*.el

%files -n %{name}-el
%{_emacs_sitelispdir}/%{pkg}.el

%changelog
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

