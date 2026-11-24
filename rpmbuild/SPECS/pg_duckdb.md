# pg_duckdb 1.2.2 配方

1.2.1 的历史构建与补丁审查见 [构建记录](../../doc/pg_duckdb.md)。

- 上游 pg_duckdb：`4e921ffbe4a16b3caec6cf24ca0151fa9d88032d`（v1.2.2）。
- DuckDB gitlink：`8d78114e90a53823803660bf821f6073ac87da8c`（v2.0.1）。
- httpfs：`f71cfdb4bff85b9e15b1f3b842d9aa395aff0167`，仍由 CMake 固定取源。
- 主归档：`pg_duckdb-1.2.2.tar.gz`，根目录 `pg_duckdb-1.2.2`。
- SHA256：`87ca6f9e2b2775731319f2ba95c7f4748b9a08cc2fd2c123020b445985d13abb`。
- EL9 另需 `curl-8.23.0.tar.gz`，仅用于私有 PIC 静态构建。
- 当前目标 PG15–19 / EL9+；PG14、EL8 已退出。
- LLVM 默认开启，主包包含 bitcode/index；核心和桥接层均保留完整 DWARF。

构建时以目标 PostgreSQL 的 PGXS `Makefile.global` 中的 `LLVM_BINPATH` 为准。
例如，PGDG 的 `1PGDG.rhel10.3`（PG15–19）指定 `/usr/lib64/llvm21/bin`。
Rocky 10.3 的默认工具链已升至 LLVM 22。使用这批 PGDG 开发包时，可从
[Rocky 10.2 归档](https://dl.rockylinux.org/vault/rocky/10.2/) 安装匹配的
`clang`、`llvm` 21.1.8 及对应的开发包。

1.2.2 修复了普通数据库角色通过 httpfs 读取 HTTPS 文件时加载系统 CA 证书的问题。
在 Rocky Linux 9.9 aarch64 的 PG18 上，实测普通角色通过签名的 httpfs
读取了启用证书校验的 HTTPS CSV。另以 pg_mooncake 0.3.4 建立镜像，
将已有的 pg_duckdb 1.2.1 升至 1.2.2 后，重启、读取旧数据和复制新写入均通过。

源码只放权威目录 `~/pgsty/repo/ext/src`，先在 builder 运行
`pig build get pg_duckdb`；缺失时只复制具体归档。
本机 `rpmbuild/SOURCES` 不存放源码。

只保留两份最小打包补丁：`source-archive` 处理归档与安装顺序，
`private-curl` 处理系统 curl API 不足；旧 httpfs C++ move 修复已上游化。
当前 PG19 兼容代码来自上游。任何支持声明均以构建记录里的实际证据为准。
