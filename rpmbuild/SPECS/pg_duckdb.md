# pg_duckdb 1.2.1 配方

完整升级、补丁审查和 PG15–19 逐平台证据见 [构建记录](../../doc/pg_duckdb.md)。

- 上游 pg_duckdb：`451d389a3fe9d179b06172c6a3595d291de7ca76`（v1.2.1）。
- DuckDB gitlink：`8d78114e90a53823803660bf821f6073ac87da8c`（v2.0.1）。
- httpfs：`f71cfdb4bff85b9e15b1f3b842d9aa395aff0167`，仍由 CMake 固定取源。
- 主归档：`pg_duckdb-1.2.1.tar.gz`，根目录 `pg_duckdb-1.2.1`。
- SHA256：`9d4d6b6eb8100ced1ff82a9e2f641dc3440d2547dd6de2aedeccfdee1af7e3aa`。
- EL9 另需 `curl-8.23.0.tar.gz`，仅用于私有 PIC 静态构建。
- 当前目标 PG15–19 / EL9+；PG14、EL8 已退出。
- LLVM 默认开启，主包包含 bitcode/index；核心和桥接层均保留完整 DWARF。

源码只放权威目录 `~/pgsty/repo/ext/src`，先在 builder 运行
`pig build get pg_duckdb`；缺失时只复制具体归档。
本机 `rpmbuild/SOURCES` 不存放源码。

只保留两份最小打包补丁：`source-archive` 处理归档与安装顺序，
`private-curl` 处理系统 curl API 不足；旧 httpfs C++ move 修复已上游化。
当前 PG19 兼容代码来自上游。任何支持声明均以构建记录里的实际证据为准。
