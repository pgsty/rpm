#!/bin/bash
set -euo pipefail

# script to create rpmbuild.tar.gz and upload to pigsty.cc / pigsty.io

BIN_DIR="$(cd "$(dirname "$0")" && pwd)"
HOME_DIR="$(cd "${BIN_DIR}/.." && pwd)"
TMP_DIR="$HOME_DIR/tmp"
TARBALL_NAME="rpmbuild.tar.gz"

# make tarball
echo "build tmp/${TARBALL_NAME}"
mkdir -p "${TMP_DIR}"
COPYFILE_DISABLE=1 gtar -zcf "${TMP_DIR}/${TARBALL_NAME}" \
    --exclude-vcs --exclude='.DS_Store' --exclude='._*' \
    --exclude='rpmbuild/BUILD' --exclude='rpmbuild/BUILDROOT' \
    --exclude='rpmbuild/RPMS' --exclude='rpmbuild/SRPMS' \
    --exclude='rpmbuild/SOURCES' --exclude='*.rpm' --exclude='*.log' \
    -C "${HOME_DIR}" rpmbuild
cd "${TMP_DIR}"

# print info
ls -alh "${TARBALL_NAME}"
md5sum  "${TARBALL_NAME}"

# upload to cloud
cp "${TARBALL_NAME}" "$HOME/pgsty/repo/ext/spec/${TARBALL_NAME}"
rclone copyto "${TARBALL_NAME}" "cos:/repo-1304744452/ext/spec/${TARBALL_NAME}"
rclone copyto "${TARBALL_NAME}" "cf:/repo/ext/spec/${TARBALL_NAME}"

# you can get it from:
# https://repo.pigsty.cc/ext/spec/rpmbuild.tar.gz
# https://repo.pigsty.io/ext/spec/rpmbuild.tar.gz
