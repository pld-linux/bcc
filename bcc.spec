Summary:	Bruce's C compiler
Summary(pl):	Kompiler C Bruce'a
Name:		bcc
Version:	0.16.0
Release:	2
License:	GPL
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/Jêzyki
Source0:	http://www.cix.co.uk/~mayday/Dev86src-%{version}.tar.gz
Patch0:		Dev86src-noroot.patch
Patch1:		Dev86src-nobcc.patch
Patch2:		Dev86src-bccpaths.patch
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86}
Requires:	bin86

%description
Bcc is a simple C compiler that produces 8086 assembler, in addition
compiler compile time options allow 80386 or 6809 versions. The
compiler understands traditional K&R C with just the restriction that
bit fields are mapped to one of the other integer types.

%description -l pl
Bcc jest prostym kompilatorem C produkuj±cym pliki asemblerowe 8086,
a dodatkowo pozwala na wybranie wersji 80386 lub 6809. Kompilator
rozumie tradycyjne K&R C z takim ograniczeniem, ¿e pola bitowe
s± odwzorowywane do jednego z innych typów ca³kowitych.

%prep
%setup -q -n dev86-%{version}
%patch0 -b .oot -p1
%patch1 -b .djb -p1
%patch2 -b .bccpaths -p1

%build
CC="%{__cc}" %{__make} <<!FooBar!
5
quit
!FooBar!

%install
rm -rf $RPM_BUILD_ROOT

%{__make} DIST=${RPM_BUILD_ROOT} install

install -m 755 $RPM_BUILD_ROOT/lib/elksemu $RPM_BUILD_ROOT%{_bindir}
#rm -rf ${RPM_BUILD_ROOT}/lib/
cp -R libc/kinclude ${RPM_BUILD_ROOT}%{_libdir}/bcc

cd ${RPM_BUILD_ROOT}%{_bindir}
rm -f nm86 size86
ln -s objdump86 nm86
ln -s objdump86 size86

# move header files out of %{_includedir} and into %{_libdir}/bcc/include
mv ${RPM_BUILD_ROOT}%{_includedir} ${RPM_BUILD_ROOT}%{_libdir}/bcc

# move man pages where they belong
install -d ${RPM_BUILD_ROOT}%{_mandir}
mv ${RPM_BUILD_ROOT}/usr/man/* ${RPM_BUILD_ROOT}%{_mandir}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root,755)
%doc README MAGIC Contributors bootblocks/README copt/README dis88/README
%doc elksemu/README unproto/README bin86/README-0.4 bin86/README bin86/ChangeLog
%dir %{_libdir}/bcc
%dir %{_libdir}/bcc/i86
%dir %{_libdir}/bcc/i386
%dir %{_libdir}/bcc/include
%attr(755,root,root) %{_bindir}/bcc
#%attr(755,root,root) %{_bindir}/as86
%attr(755,root,root) %{_bindir}/as86_encap
#%attr(755,root,root) %{_bindir}/ld86
%attr(755,root,root) %{_bindir}/objdump86
%attr(755,root,root) %{_bindir}/nm86
%attr(755,root,root) %{_bindir}/size86
%attr(755,root,root) %{_libdir}/bcc/bcc-cc1
%attr(755,root,root) %{_libdir}/bcc/copt
%attr(755,root,root) %{_libdir}/bcc/unproto
%{_libdir}/bcc/i86/*
%{_libdir}/bcc/i386/*
%{_libdir}/liberror.txt
%{_libdir}/bcc/include/*
%{_libdir}/bcc/kinclude/*
%attr(755,root,root) %{_bindir}/elksemu
%{_mandir}/man1/*
