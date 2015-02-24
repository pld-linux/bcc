Summary:	Bruce's C compiler
Summary(pl.UTF-8):	Kompilator C Bruce'a
Name:		bcc
Version:	0.16.19
Release:	2
License:	GPL
Group:		Development/Languages
Source0:	http://www.debath.co.uk/dev86/Dev86src-%{version}.tar.gz
# Source0-md5:	442e98e1afa23fe00d40c5a996385942
Patch0:		Dev86src-noroot.patch
Patch1:		Dev86src-opt.patch
Patch2:		dev86-0.16.17-fortify.patch
Patch3:		dev86-pic.patch
Patch4:		dev86-64bit.patch
Patch5:		dev86-noelks.patch
Patch6:		dev86-nostrip.patch
Patch7:		dev86-print-overflow.patch
Patch8:		dev86-make.patch
Patch9:		dev86-copt.patch
Patch10:	dev86-format.patch
URL:		http://www.debath.co.uk/
Requires:	bin86 >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't try to strip Linux-8086 objects
%define		_noautostrip	.*%{_libdir}/bcc/.*\\.[ao]


%description
Bcc is a simple C compiler that produces 8086 assembler, in addition
compiler compile time options allow 80386 or 6809 versions. The
compiler understands traditional K&R C with just the restriction that
bit fields are mapped to one of the other integer types.

%description -l pl.UTF-8
Bcc jest prostym kompilatorem C tworzącym pliki asemblerowe 8086,
a dodatkowo pozwala na wybranie wersji 80386 lub 6809. Kompilator
rozumie tradycyjne C K&R z takim ograniczeniem, że pola bitowe
są odwzorowywane do jednego z innych typów całkowitych.

%prep
%setup -q -n dev86-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%if "%{_lib}" == "lib64"
%patch4 -p1
%endif
%ifnarch %{ix86}
%patch5 -p1
%endif
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

mv -f bootblocks/README README.bootblocks
mv -f copt/README README.copt
mv -f dis88/README README.dis88
mv -f elksemu/README README.elksemu
mv -f unproto/README README.unproto

%build
CC="%{__cc}" \
%{__make} -j1 all other \
	OPT="%{rpmcppflags} %{rpmcflags}" <<!FooBar!
5
quit
!FooBar!

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install-all \
	DIST=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir}/bcc \
	INCLDIR=%{_libdir}/bcc \
	LOCALPREFIX=%{_prefix} \
	MANDIR=%{_mandir}

cp -R libc/kinclude $RPM_BUILD_ROOT%{_libdir}/bcc

ln -sf objdump86 $RPM_BUILD_ROOT%{_bindir}/nm86
ln -sf objdump86 $RPM_BUILD_ROOT%{_bindir}/size86

# these are separated in bin86 package
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{as86,ld86}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{as,ld}86.1*

%ifnarch %{ix86}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/elks*.1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes Contributors README*
%attr(755,root,root) %{_bindir}/ar86
%attr(755,root,root) %{_bindir}/bcc
%attr(755,root,root) %{_bindir}/dis86
%ifarch %{ix86}
%attr(755,root,root) %{_bindir}/elksemu
%endif
%attr(755,root,root) %{_bindir}/makeboot
%attr(755,root,root) %{_bindir}/nm86
%attr(755,root,root) %{_bindir}/objdump86
%attr(755,root,root) %{_bindir}/size86
%dir %{_libdir}/bcc
%attr(755,root,root) %{_libdir}/bcc/as86_encap
%attr(755,root,root) %{_libdir}/bcc/bcc-cc1
%attr(755,root,root) %{_libdir}/bcc/bcc-cpp
%attr(755,root,root) %{_libdir}/bcc/copt
%attr(755,root,root) %{_libdir}/bcc/unproto
%{_libdir}/bcc/i386
%{_libdir}/bcc/include
%{_libdir}/bcc/kinclude
%{_libdir}/bcc/crt*.o
%{_libdir}/bcc/lib*.a
%{_libdir}/bcc/rules.*
%{_mandir}/man1/bcc.1*
%{_mandir}/man1/dis86.1*
%ifarch %{ix86}
%{_mandir}/man1/elks.1*
%{_mandir}/man1/elksemu.1*
%endif
