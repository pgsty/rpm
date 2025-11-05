#!/bin/bash

# script to create rpmbuild.tar.gz and upload to pigsty.cc / pigsty.io

PROG_NAME="$(basename $0)"
BIN_DIR="$(cd $(dirname $0) && pwd)"
HOME_DIR="$(cd ${BIN_DIR}/.. && pwd)"
TMP_DIR="$HOME_DIR/tmp"
RPMBUILD_DIR="$HOME_DIR/rpmbuild"
TARBALL_NAME="rpmbuild.tar.gz"

# make tarball
echo "build tmp/rpmbuild"
rm -rf "${TMP_DIR}/rpmbuild"
cp -r ${RPMBUILD_DIR} ${TMP_DIR}
cd "${TMP_DIR}"
gtar -zcf rpmbuild.tar.gz rpmbuild
RPM_TARBALL="${TMP_DIR}/${TARBALL_NAME}"

# print info
ls -alh "${TARBALL_NAME}"
md5sum  "${TARBALL_NAME}"

# upload to cloud
cp "${TARBALL_NAME}" ~/pgsty/repo/ext/spec/${TARBALL_NAME}
rclone copyto "${TARBALL_NAME}" "cos:/repo-1304744452/ext/spec/${TARBALL_NAME}"
rclone copyto "${TARBALL_NAME}" "cf:/repo/ext/spec/${TARBALL_NAME}"

# you can get it from:
# https://repo.pigsty.cc/ext/spec/rpmbuild.tar.gz
# https://repo.pigsty.io/ext/spec/rpmbuild.tar.gz
