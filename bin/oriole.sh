#!/bin/bash

# Script to replace PostgreSQL with OrioleDB in specific lines only
# Usage: ./replace_postgresql.sh [postgres_src_directory]

PROG_NAME="$(basename $0)"
BIN_DIR="$(cd $(dirname $0) && pwd)"
SRC_DIR="$(cd ${BIN_DIR}/../src && pwd)"
POSTGRES_DIR="${SRC_DIR}/postgres"
PACKAGE_NAME="oriolepg-17.11"

echo "locate $SRC_DIR"


echo "extract $SRC_DIR/postgres.tar.gz"
cd ${SRC_DIR}
rm -rf postgres
tar -xf postgres.tar.gz
cd postgres
git checkout patches17_11


echo "Replacing PostgreSQL with OrioleDB in specific lines in $POSTGRES_DIR"

# Replace in configure - only in PG_VERSION_STR line
if [ -f "$POSTGRES_DIR/configure" ]; then
    sed -i '' '/PG_VERSION_STR/s/PostgreSQL/OrioleDB/g' "$POSTGRES_DIR/configure"
    echo "Updated configure (PG_VERSION_STR line)"
else
    echo "Warning: configure not found"
fi

# Replace in configure.ac - only in line containing "PostgreSQL $PG_VERSION on"
if [ -f "$POSTGRES_DIR/configure.ac" ]; then
    sed -i '' '/PostgreSQL \$PG_VERSION on/s/PostgreSQL/OrioleDB/g' "$POSTGRES_DIR/configure.ac"
    echo "Updated configure.ac (PostgreSQL \$PG_VERSION on line)"
else
    echo "Warning: configure.ac not found"
fi

# Replace in meson.build - only in lines containing "PostgreSQL @0@"
if [ -f "$POSTGRES_DIR/meson.build" ]; then
    sed -i '' '/PostgreSQL @0@ on/s/PostgreSQL/OrioleDB/g' "$POSTGRES_DIR/meson.build"
    echo "Updated meson.build (PostgreSQL @0@ lines)"
else
    echo "Warning: meson.build not found"
fi

echo "Replacement complete!"


echo "Check OrioleDB String!"
grep OrioleDB  ${POSTGRES_DIR}/configure
grep OrioleDB  ${POSTGRES_DIR}/configure.ac
grep OrioleDB  ${POSTGRES_DIR}/meson.build


echo package ${PACKAGE_NAME}
rm -rf ${POSTGRES_DIR}/.git
mv ${POSTGRES_DIR} ${SRC_DIR}/${PACKAGE_NAME}

cd ${SRC_DIR}
gtar -czf ${PACKAGE_NAME}.tar.gz ${PACKAGE_NAME}
rm -rf ${PACKAGE_NAME}
