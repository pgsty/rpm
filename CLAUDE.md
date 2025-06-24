# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a PostgreSQL extension RPM packaging repository for the Pigsty project. It builds RPM packages for PostgreSQL extensions that are not included in the official PGDG repository, primarily targeting Enterprise Linux (EL) distributions (EL7, EL8, EL9) on both x86_64 and aarch64 architectures.

## Repository Structure

- `src/` - Source tarballs for all PostgreSQL extensions
- `rpmbuild/` - RPM build environment following FHS structure
  - `SPECS/` - RPM spec files for each extension
  - `SOURCES/` - Source files and patches (mirrors `src/`)
  - `RPMS/` - Built RPM packages organized by OS/arch (el8.x86_64, el9.aarch64, etc.)
- `build` - Shell script for creating YUM repositories with signing support
- `tmp/` - Contains actual built RPM files organized by platform

## Common Commands

### Environment Setup
```bash
# Set up RPM build environment
rpmdev-setuptree

# Install development tools
sudo yum groupinstall --nobest -y 'Development Tools'
```

### Building Dependencies
```bash
# Build core dependencies first
make deps          # Build scws, libduckdb, pg_filedump
make scws scws-install
make libduckdb libduckdb-install
```

### Building Extensions
```bash
# Build specific extension
./build <extension_name> [pg_version] [options]
# Example: ./build zhparser 16 nodebug

# Build extension batches
make batch1        # Core extensions (zhparser, duckdb_fdw, hunspell, etc.)
make batch2        # Additional extensions 
make batch3        # More extensions
make batch4        # Platform-specific missing packages

# Build Rust/PGRX extensions
make rust1         # Main Rust extensions (pg_graphql, wrappers, etc.)
make rust2         # Additional Rust extensions (pgml, plprql)
```

### Working with Remote Build VMs
```bash
# Push specs and sources to build VMs
make push-el       # Push to all EL VMs (el8, el9)
make push8         # Push to EL8 VM specifically  
make push9         # Push to EL9 VM specifically

# Pull built RPMs from VMs
make pull-el       # Pull from all EL VMs
make pull8         # Pull from EL8 VM
make pull9         # Pull from EL9 VM
```

### Repository Management
```bash
# Create YUM repositories
./build <repo_path>           # Create repo in directory
./build <repo_path> sign      # Create repo with RPM signing

# Organize repos by OS version
make repo8         # Create EL8 repository
make repo9         # Create EL9 repository
```

## High-Level Architecture

### Extension Categories

1. **C/C++ Extensions (41 total)** - Traditional PostgreSQL extensions built from C/C++ source
2. **Rust/PGRX Extensions** - Modern extensions built using the pgrx framework
3. **Dependencies** - Core libraries like libduckdb, scws required by other extensions
4. **Kernels** - Alternative PostgreSQL kernels (OrioleDB, OpenHalo)

### Build Process Flow

1. **Source Management** - Source tarballs stored in `src/`, mirrored to `rpmbuild/SOURCES/`
2. **Spec Files** - RPM spec files in `rpmbuild/SPECS/` define build instructions per extension
3. **Batch Building** - Extensions organized into logical build batches with dependencies
4. **Multi-Architecture** - Supports x86_64 and aarch64 across EL8/EL9
5. **Remote Building** - Uses remote VMs for actual compilation, rsync for file transfer
6. **Repository Creation** - Final step creates signed YUM repositories

### Extension Dependencies

- `zhparser` requires `scws` library
- `duckdb_fdw` requires `libduckdb` 
- Many extensions support multiple PostgreSQL versions (13-17)
- Rust extensions require specific pgrx framework versions
- Some extensions have inter-dependencies (e.g., pg_vectorize needs pgmq, pg_cron)

### Makefile Organization

- Root `Makefile` - High-level coordination, VM management, repository creation
- `rpmbuild/Makefile` - Detailed extension building with batches and dependencies
- Build targets organized by complexity and dependency chains
- Separate workflows for x86_64 vs aarch64 builds

## Special Notes

- Always build dependencies (`make deps`) before extension batches
- Rust extensions require specific pgrx versions and may need proxy configuration
- The `build` script handles both repository creation and RPM signing
- Remote VM builds use SSH key authentication and rsync for file transfer
- Some extensions are marked as obsolete due to inclusion in PGDG or maintenance issues