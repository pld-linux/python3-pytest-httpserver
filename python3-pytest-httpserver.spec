#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	HTTP server for pytest
Summary(pl.UTF-8):	Serwer HTTP dla pytesta
Name:		python3-pytest-httpserver
Version:	1.0.8
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-httpserver/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-httpserver/pytest_httpserver-%{version}.tar.gz
# Source0-md5:	c9f72a5206cdecd571b20fcd0057f2f4
URL:		https://pypi.org/project/pytest-httpserver/
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 7.1.3
BuildRequires:	python3-requests >= 2.28.1
BuildRequires:	python3-werkzeug >= 2.0.0
BuildRequires:	python3-toml >= 0.10.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme >= 1.0.0
BuildRequires:	sphinx-pdg-3 >= 4
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library is designed to help to test HTTP clients without
contacting the real HTTP server. In other words, it is a fake HTTP
server which is accessible via localhost can be started with the
pre-defined expected HTTP requests and their responses.

%description -l pl.UTF-8
Ta biblioteka ma za zadanie wspomóc testowanie klientów HTTP bez
łączenia się z prawdziwym serwerem HTTP. Innymi słowy, jest to
fałszywy serwer HTTP, dostępny z poziomu localhosta, który można
uruchomić z predefiniowanymi, oczekiwanymi żądaniami HTTP i
odpowiedziami na nie.

%package apidocs
Summary:	API documentation for Python pytest-httpserver module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest-httpserver
Group:		Documentation

%description apidocs
API documentation for Python pytest-httpserver module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest-httpserver.

%prep
%setup -q -n pytest_httpserver-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_httpserver.pytest_plugin \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.md
%{py3_sitescriptdir}/pytest_httpserver
%{py3_sitescriptdir}/pytest_httpserver-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
