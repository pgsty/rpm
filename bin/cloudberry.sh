#!/usr/bin/env bash
#==============================================================#
# File      :   cloudberry.sh
# Desc      :   build Cloudberry binary DEB/RPM from local tarball
# Path      :   bin/cloudberry.sh
#==============================================================#
set -euo pipefail

PROG_NAME="$(basename "$0")"
PROG_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${PROG_DIR}/.." && pwd)"
TEMPLATE_DIR="${ROOT_DIR}/meta/cloudberry"

MODE="all"
TAG="2.0.0-incubating"
VERSION=""
RELEASE="1"
TARBALL=""
WORK_ROOT="${ROOT_DIR}/tmp/cloudberry"
OUT_DIR="${ROOT_DIR}/tmp/cloudberry/dist"
PLATFORM="linux/amd64"
PULL_IMAGES=true
KEEP_WORKDIR=true
DRY_RUN=false

if command -v nproc >/dev/null 2>&1; then
  JOBS="$(nproc)"
else
  JOBS="$(sysctl -n hw.logicalcpu 2>/dev/null || echo 8)"
fi

usage() {
  cat <<EOF
Usage: ${PROG_NAME} [options]

Build Cloudberry DEB/RPM packages using a local source tarball.
Workflow is fixed: local tarball -> extract into build dir -> build -> package.

Options:
  -m, --mode <all|deb|rpm>   Build target (default: all)
  -t, --tarball <path>       Local Cloudberry source tarball
  -g, --tag <tag>            Upstream tag to download when tarball is missing (default: ${TAG})
  -v, --version <version>    Package version (default: inferred from tag)
  -r, --release <release>    Package release/build number (default: ${RELEASE})
  -j, --jobs <n>             Parallel make jobs inside container (default: ${JOBS})
  -w, --work-root <path>     Working root directory (default: ${WORK_ROOT})
  -o, --out-dir <path>       Artifact output directory (default: ${OUT_DIR})
  -p, --platform <platform>  Docker platform (default: ${PLATFORM})
      --no-pull              Skip docker image pull
      --clean-workdir        Remove work directory after success
  -n, --dry-run              Print commands only
  -h, --help                 Show this help

Examples:
  ${PROG_NAME} --mode all --tarball /path/to/cloudberry-2.0.0-incubating.tar.gz
  ${PROG_NAME} --mode deb --tag 2.0.0-incubating
EOF
}

log_info()  { printf "[INFO] %s\n" "$*"; }
log_warn()  { printf "[WARN] %s\n" "$*" >&2; }
log_fail()  { printf "[FAIL] %s\n" "$*" >&2; }
die()       { log_fail "$*"; exit 1; }

abs_path() {
  local p="$1"
  if [[ "$p" = /* ]]; then
    printf "%s\n" "$p"
  else
    printf "%s/%s\n" "$(pwd)" "$p"
  fi
}

infer_version_from_tag() {
  local v="$1"
  v="${v#v}"
  v="${v%-incubating}"
  printf "%s\n" "$v"
}

download_tarball() {
  local tag="$1"
  local dst="$2"
  local apache_url="https://downloads.apache.org/incubator/cloudberry/${tag}/apache-cloudberry-${tag}-src.tar.gz"
  local github_url="https://codeload.github.com/apache/cloudberry/tar.gz/refs/tags/${tag}"
  mkdir -p "$(dirname "$dst")"
  log_info "downloading Cloudberry source tarball: ${apache_url}"
  if ! curl -fL --retry 5 --retry-all-errors --retry-delay 2 -o "$dst" "$apache_url"; then
    log_warn "apache source tarball download failed, fallback to GitHub tag archive"
    curl -fL --retry 5 --retry-all-errors --retry-delay 2 -o "$dst" "$github_url"
  fi
  log_info "saved local tarball: ${dst}"
}

run_cmd() {
  if [[ "${DRY_RUN}" == true ]]; then
    printf "[DRY] "
    printf "%q " "$@"
    printf "\n"
    return 0
  fi
  "$@"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -m|--mode)
      MODE="$2"
      shift 2
      ;;
    -t|--tarball)
      TARBALL="$2"
      shift 2
      ;;
    -g|--tag)
      TAG="$2"
      shift 2
      ;;
    -v|--version)
      VERSION="$2"
      shift 2
      ;;
    -r|--release)
      RELEASE="$2"
      shift 2
      ;;
    -j|--jobs)
      JOBS="$2"
      shift 2
      ;;
    -w|--work-root)
      WORK_ROOT="$2"
      shift 2
      ;;
    -o|--out-dir)
      OUT_DIR="$2"
      shift 2
      ;;
    -p|--platform)
      PLATFORM="$2"
      shift 2
      ;;
    --no-pull)
      PULL_IMAGES=false
      shift
      ;;
    --clean-workdir)
      KEEP_WORKDIR=false
      shift
      ;;
    -n|--dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown option: $1"
      ;;
  esac
done

case "${MODE}" in
  all|deb|rpm) ;;
  *)
    die "invalid mode: ${MODE} (expected all|deb|rpm)"
    ;;
esac

[[ -d "${TEMPLATE_DIR}/deb" ]] || die "missing template dir: ${TEMPLATE_DIR}/deb"
[[ -f "${TEMPLATE_DIR}/rpm/cloudberry.spec" ]] || die "missing template file: ${TEMPLATE_DIR}/rpm/cloudberry.spec"

if [[ -z "${TARBALL}" ]]; then
  TARBALL="${WORK_ROOT}/sources/cloudberry-${TAG}.tar.gz"
fi

if [[ -z "${VERSION}" ]]; then
  VERSION="$(infer_version_from_tag "${TAG}")"
fi
[[ -n "${VERSION}" ]] || die "unable to infer package version"

TARBALL="$(abs_path "${TARBALL}")"
WORK_ROOT="$(abs_path "${WORK_ROOT}")"
OUT_DIR="$(abs_path "${OUT_DIR}")"

if [[ ! -f "${TARBALL}" ]]; then
  if [[ "${DRY_RUN}" == true ]]; then
    log_warn "tarball not found in dry-run mode: ${TARBALL}"
    run_cmd download_tarball "${TAG}" "${TARBALL}"
  else
    download_tarball "${TAG}" "${TARBALL}"
  fi
fi

if [[ "${DRY_RUN}" == false ]]; then
  [[ -f "${TARBALL}" ]] || die "local tarball not found: ${TARBALL}"
fi

run_cmd mkdir -p "${WORK_ROOT}" "${OUT_DIR}/deb" "${OUT_DIR}/rpm"

BUILD_ID="$(date +%Y%m%d-%H%M%S)"
WORK_DIR="${WORK_ROOT}/build-${BUILD_ID}"
run_cmd mkdir -p "${WORK_DIR}/artifacts/deb" "${WORK_DIR}/artifacts/rpm" "${WORK_DIR}/logs"
WORK_DIR="$(abs_path "${WORK_DIR}")"

log_info "mode: ${MODE}"
log_info "tarball(local): ${TARBALL}"
log_info "version/release: ${VERSION}-${RELEASE}"
log_info "workdir: ${WORK_DIR}"
log_info "outdir: ${OUT_DIR}"

run_container_build() {
  local target="$1"
  local image="$2"
  local log_file="${WORK_DIR}/logs/${target}.log"

  if [[ "${PULL_IMAGES}" == true ]]; then
    run_cmd docker pull --platform "${PLATFORM}" "${image}"
  fi

  local -a docker_cmd=(
    docker run --rm -i
    --platform "${PLATFORM}"
    --user root
    -v "${WORK_DIR}:/work"
    -v "${TARBALL}:/local/cloudberry.tar.gz:ro"
    -v "${TEMPLATE_DIR}:/templates:ro"
    "${image}"
    bash -s -- "${target}" "${VERSION}" "${RELEASE}" "${JOBS}"
  )

  if [[ "${DRY_RUN}" == true ]]; then
    printf "[DRY] "
    printf "%q " "${docker_cmd[@]}"
    printf "\n"
    return 0
  fi

  "${docker_cmd[@]}" <<'EOS' | tee "${log_file}"
set -euo pipefail

TARGET="$1"
PKG_VERSION="$2"
PKG_RELEASE="$3"
JOBS="$4"

log() {
  printf "[%s] %s\n" "${TARGET}" "$*"
}

ensure_ag() {
  if command -v ag >/dev/null 2>&1; then
    return
  fi
  if command -v apt-get >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y silversearcher-ag
  elif command -v dnf >/dev/null 2>&1; then
    dnf install -y the_silver_searcher
  fi
}

extract_local_tarball() {
  local dst_root="/work/build/${TARGET}"
  rm -rf "${dst_root}"
  mkdir -p "${dst_root}/src"
  tar -xf /local/cloudberry.tar.gz -C "${dst_root}/src"
  find "${dst_root}/src" -mindepth 1 -maxdepth 1 -type d | head -n1
}

run_configure_build() {
  local src_dir="$1"
  local build_destination="$2"
  local configure_script="${src_dir}/devops/build/automation/cloudberry/scripts/configure-cloudberry.sh"
  local build_script="${src_dir}/devops/build/automation/cloudberry/scripts/build-cloudberry.sh"

  # Ensure gpadmin exists in build environment.
  if ! id gpadmin >/dev/null 2>&1; then
    useradd -m -d /home/gpadmin -s /bin/bash gpadmin
  fi

  if [ -f "${configure_script}" ] && [ -f "${build_script}" ]; then
    chmod +x "${configure_script}" "${build_script}"
    su - gpadmin -c "cd ${src_dir} && SRC_DIR=${src_dir} ENABLE_DEBUG=false BUILD_DESTINATION=${build_destination} ${configure_script}"
    su - gpadmin -c "cd ${src_dir} && SRC_DIR=${src_dir} BUILD_DESTINATION=${build_destination} ${build_script}"
    return
  fi

  # Fallback for release tarballs that do not include devops/build scripts.
  rm -rf "${build_destination}"
  mkdir -p "${build_destination}/lib"
  if [ -d /usr/local/xerces-c/lib ]; then
    cp -v /usr/local/xerces-c/lib/libxerces-c.so /usr/local/xerces-c/lib/libxerces-c-3.*.so "${build_destination}/lib" || true
  fi

  export LD_LIBRARY_PATH="${build_destination}/lib:${LD_LIBRARY_PATH:-}"

  declare -a cfg
  cfg=(
    --prefix="${build_destination}"
    --disable-external-fts
    --enable-gpcloud
    --enable-ic-proxy
    --enable-mapreduce
    --enable-orafce
    --enable-orca
    --enable-pax
    --disable-pxf
    --enable-tap-tests
    --with-gssapi
    --with-ldap
    --with-libxml
    --with-lz4
    --with-openssl
    --with-pam
    --with-perl
    --with-pgport=5432
    --with-python
    --with-pythonsrc-ext
    --with-ssl=openssl
    --with-uuid=e2fs
  )
  if [ -d /usr/local/xerces-c/include ]; then
    cfg+=(--with-includes=/usr/local/xerces-c/include)
    cfg+=(--with-libraries="${build_destination}/lib")
  elif [ -d /usr/include/xercesc ]; then
    cfg+=(--with-includes=/usr/include/xercesc)
  fi

  (cd "${src_dir}" && ./configure "${cfg[@]}")
  (cd "${src_dir}" && make -j"${JOBS}" --directory "${src_dir}")
  (cd "${src_dir}" && make -j"${JOBS}" --directory "${src_dir}/contrib")
  (cd "${src_dir}" && make install --directory "${src_dir}")
  (cd "${src_dir}" && make install --directory "${src_dir}/contrib")
}

build_deb() {
  local src_dir="$1"
  local build_destination="${src_dir}/debian/build"

  ensure_ag
  rm -rf "${src_dir}/debian"
  mkdir -p "${src_dir}/debian/source"
  cp -a /templates/deb/. "${src_dir}/debian/"
  chmod +x "${src_dir}/debian/rules" "${src_dir}/debian/postinst"
  chmod -x "${src_dir}/debian/install" || true

  log "building from extracted local tarball in ${src_dir}"
  run_configure_build "${src_dir}" "${build_destination}"

  local os_distro="unknown"
  if [ -f /etc/os-release ]; then
    # shellcheck source=/dev/null
    . /etc/os-release
    os_distro="$(printf "%s%s" "${ID}" "${VERSION_ID}" | tr '[:upper:]' '[:lower:]')"
  fi
  export CBDB_PKG_VERSION="${PKG_VERSION}-${PKG_RELEASE}-${os_distro}"

  cat > "${src_dir}/debian/changelog" <<EOF
cloudberry (${CBDB_PKG_VERSION}) stable; urgency=low

  * cloudberry autobuild from local tarball

 -- cloudberry-builder <cloudberry-builder@$(hostname)>  $(date +'%a, %d %b %Y %H:%M:%S %z')
EOF

  (cd "${src_dir}" && dpkg-buildpackage -us -uc)

  mkdir -p /work/artifacts/deb
  cp "${src_dir}"/../cloudberry_"${CBDB_PKG_VERSION}"_*.deb /work/artifacts/deb/ 2>/dev/null || true
  cp "${src_dir}"/../cloudberry-dbgsym_"${CBDB_PKG_VERSION}"_*.ddeb /work/artifacts/deb/ 2>/dev/null || true
  cp "${src_dir}"/../cloudberry_"${CBDB_PKG_VERSION}"_*.changes /work/artifacts/deb/ 2>/dev/null || true
  cp "${src_dir}"/../cloudberry_"${CBDB_PKG_VERSION}"_*.buildinfo /work/artifacts/deb/ 2>/dev/null || true
  cp "${src_dir}"/../cloudberry_"${CBDB_PKG_VERSION}".dsc /work/artifacts/deb/ 2>/dev/null || true
  cp "${src_dir}"/../cloudberry_"${CBDB_PKG_VERSION}".tar.xz /work/artifacts/deb/ 2>/dev/null || true

  if ! ls /work/artifacts/deb/cloudberry_"${CBDB_PKG_VERSION}"_*.deb >/dev/null 2>&1; then
    log "failed to locate generated .deb file"
    exit 1
  fi
}

build_rpm() {
  local src_dir="$1"
  local build_destination="/usr/local/cloudberry"

  ensure_ag
  log "building from extracted local tarball in ${src_dir}"
  run_configure_build "${src_dir}" "${build_destination}"

  cp -f "${src_dir}/LICENSE" "${build_destination}/LICENSE"

  rpmdev-setuptree
  cp /templates/rpm/cloudberry.spec "${HOME}/rpmbuild/SPECS/cloudberry.spec"
  rpmbuild -bb "${HOME}/rpmbuild/SPECS/cloudberry.spec" \
    --define "version ${PKG_VERSION}" \
    --define "release ${PKG_RELEASE}"

  mkdir -p /work/artifacts/rpm
  find "${HOME}/rpmbuild/RPMS" -type f -name "cloudberry-${PKG_VERSION}-${PKG_RELEASE}*.rpm" -exec cp -f {} /work/artifacts/rpm/ \;
  find "${HOME}/rpmbuild/RPMS" -type f -name "cloudberry-debuginfo-${PKG_VERSION}-${PKG_RELEASE}*.rpm" -exec cp -f {} /work/artifacts/rpm/ \; || true
  find "${HOME}/rpmbuild/RPMS" -type f -name "cloudberry-debugsource-${PKG_VERSION}-${PKG_RELEASE}*.rpm" -exec cp -f {} /work/artifacts/rpm/ \; || true

  if ! ls /work/artifacts/rpm/cloudberry-"${PKG_VERSION}"-"${PKG_RELEASE}"*.rpm >/dev/null 2>&1; then
    log "failed to locate generated .rpm file"
    exit 1
  fi
}

src_dir="$(extract_local_tarball)"
[ -n "${src_dir}" ] || { log "cannot find extracted source directory"; exit 1; }

case "${TARGET}" in
  deb) build_deb "${src_dir}" ;;
  rpm) build_rpm "${src_dir}" ;;
  *) log "unknown target ${TARGET}"; exit 1 ;;
esac
EOS
}

if [[ "${MODE}" == "all" || "${MODE}" == "deb" ]]; then
  run_container_build "deb" "apache/incubator-cloudberry:cbdb-build-ubuntu22.04-latest"
fi

if [[ "${MODE}" == "all" || "${MODE}" == "rpm" ]]; then
  run_container_build "rpm" "apache/incubator-cloudberry:cbdb-build-rocky9-latest"
fi

run_cmd cp -f "${WORK_DIR}/artifacts/deb/"* "${OUT_DIR}/deb/" 2>/dev/null || true
run_cmd cp -f "${WORK_DIR}/artifacts/rpm/"* "${OUT_DIR}/rpm/" 2>/dev/null || true

if [[ "${DRY_RUN}" == false ]]; then
  log_info "deb artifacts:"
  ls -lh "${OUT_DIR}/deb" || true
  log_info "rpm artifacts:"
  ls -lh "${OUT_DIR}/rpm" || true
fi

if [[ "${KEEP_WORKDIR}" == false ]]; then
  run_cmd rm -rf "${WORK_DIR}"
fi

log_info "done"
