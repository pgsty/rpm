Name:           libarrow-s3
Version:        17.0.0
Release:        1PIGSTY%{?dist}
Summary:        Dependency libs for parquet s3 fdw
License:        Apache 2.0
URL:            https://github.com/apache/arrow

%description
Apache Arrow is a development platform for in-memory analytics.
It contains a set of technologies that enable big data systems to process and move data fast.

This package contains dependency libs for parquet_s3_fdw.

%prep

%build

%install
mkdir -p %{buildroot}/usr/lib64
cp -a %{_sourcedir}/libarrow-s3/* %{buildroot}/usr/lib64/

%files
/usr/lib64/libaws-cpp-sdk-core.so
/usr/lib64/libaws-cpp-sdk-s3.so
/usr/lib64/libarrow.so.1700.0.0
/usr/lib64/libparquet.so.1700.0.0
/usr/lib64/libarrow.so
/usr/lib64/libarrow.so.1700
/usr/lib64/libparquet.so
/usr/lib64/libparquet.so.1700

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Sun May 5 2024 Vonng <rh@vonng.com> - 17.0.0
- Initial RPM release, used by Pigsty <https://pigsty.io>