# duckdb_fdw 独立静态打包

当前设计：duckdb_fdw **2.0.2** 内嵌从源码构建的 DuckDB **2.0.0**，同一 PostgreSQL 主版本与 `pg_duckdb` 安装互斥。此文件记录本次开发验证；结果表将在验证完成后填入，不能视为发布记录。

## 来源与旧补丁审查

| 项目 | 正式 tag | commit | 源码归档 SHA-256 |
|---|---|---|---|
| [duckdb_fdw](https://github.com/alitrack/duckdb_fdw/releases/tag/v2.0.2) | v2.0.2 | `4c444d19f80eace50bc09fa3ec766e8ca2cf667d` | `1ed7935b009211915434fd65083b0562389e3faf1722865f81633d70a0c0fc8b` |
| [DuckDB](https://github.com/duckdb/duckdb/releases/tag/v2.0.0) | v2.0.0 | `d54cbbe3df17e8e5ce68312f483b4155836112aa` | `7e89053255046bfb26afbd7f524a2fb84df7dbef496aa911ea35e4a1182fdc00` |

两者均为非 draft、非 prerelease 正式 release。FDW tag 是 annotated tag，tag 对象为 `ee274ae7b17b0df6dad33de95feadf83ae837bb0`。校验值是下载官方 tag 归档后本地计算并固定的值，不是上游单独签署的校验声明。

最终源码位于 `/Users/vonng/pgsty/repo/ext/src/duckdb_fdw-2.0.2.tar.gz` 和 `duckdb-2.0.0.tar.gz`。不修改、冒用旧的 `2.0.1+git20260529.9354241` 归档。

原 `duckdb_fdw-2.0.1.patch` 已撤销，逐项处理如下：

- PG14–18 planner API、PG18 explain 头文件、slot 初始化：正式上游已有对应实现，撤销旧修改。
- 缺省 user mapping、连接初始化、事务清理、类型转换：正式上游已重写相关路径，采用上游实现。
- UPDATE/DELETE 回归预期、普通文本方括号处理：采用正式上游测试和修复。
- 旧 SQL 升级语法补丁：不继承；忠实安装上游所有 control/SQL/升级脚本。
- 从 pg_duckdb 取头文件、软链接 `libduckdb.so`、RPATH、旧 ABI 开关、共享 runtime 共存补丁：移除。
- 新补丁只处理独立静态构建、静态扩展注册、运行时来源检测及互斥策略。

## 链接与运行边界

构建使用发行版编译、加固、调试 flags 和 PIC。显式链接 DuckDB core、HTTP/动态加载能力以及 core_functions、Parquet、JSON、ICU 静态归档，不依赖 `-lduckdb` 搜索，不安装通用 `libduckdb.so`。系统 libc/libstdc++ 等仍动态链接。FDW 的 PGXS bitcode 和 index 进入主包，调试符号由 RPM/DEB 自动拆分。

EL9 GCC 11.5 的 LTO 链接产物在文件库 `INSERT` 上触发 `PhysicalBatchInsert::GetDataInternal` 的 NULL state 内部错误；内存库路径正常。官方 2.0.0 CLI 和同一批 PIC fat archives 以 `-fno-lto` 链接的独立 C API、PostgreSQL 原型均通过同一插入测试。因此最终 native 链接显式使用 `-fno-lto`，保留发行版的编译优化、加固和 DWARF。这与 PGXS 的 Clang bitcode/LLVM JIT 是不同路径，后者继续启用。未修改 DuckDB 执行器源码或绕过该 SQL 测试。

本方案保留 DuckDB 公共符号并使用 `-Bsymbolic` 约束自身定义的内部绑定。它不隔离 PostgreSQL 的全局 ELF 加载命名空间，尤其不能保证之后加载的另一 DuckDB 核心不会误绑定。`_PG_init` 和查询时检查都晚于 `dlopen` 的重定位与构造函数，不能当作完整共存保护。因此以同 PG 主版本 `Conflicts` 限制受支持的安装组合；不修改 pg_duckdb、不添加 Replaces、不覆盖其文件。

运行时 guard 以 `dladdr` 返回的 ELF 基址核对嵌入核心所属模块，并扫描已加载的 pg_duckdb 和外部 libduckdb。不根据 control 文件是否存在拒绝，也不伪造库文件名。保留清晰错误和重启提示；禁止原有 unsupported override 绕过此包的互斥策略。

从 pg_duckdb 模式切换到 FDW 模式时，修改 `shared_preload_libraries` 并重启 PostgreSQL。卸载/替换包不会卸载已有服务器进程内的库；新连接仍可能继承 postmaster 预加载的旧库。不同数据库或查询顺序不构成隔离。不能承诺同一 backend 内临时切换。

## 验证与复现

工作证据目录：`/Users/vonng/tmp/duckdb-fdw-20261024/`，包含官方 release/tag JSON、下载校验、原工作树状态、构建与测试日志以及最终产物。

本次只验收 `pgsty/el9a:build` / PG18 和随后 `pgsty/u24a:build` / PG18。不运行生产矩阵、不提交、不推送、不发布、不更新 pgext。

RPM 基本流程（仅隔离容器）：

```sh
cd /root/rpmbuild
pig build get duckdb_fdw
pig build get duckdb_fdw-2.0.2.tar.gz duckdb-2.0.0.tar.gz
# 镜像尚未提供新源码时，只复制上面的两个确定缺失归档。
./dep duckdb_fdw 18
cp SPECS/patches/duckdb_fdw-2.0.2-static.patch SOURCES/
rpmbuild -ba --define 'pgmajorversion 18' --define 'duckdb_core_jobs 10' \
  --define '_smp_mflags -j10' --define '_binary_payload w7.zstdio' \
  SPECS/duckdb_fdw.spec
```

本次迭代最后一次使用 `-ba --noprep` 复用已经校验、解包、打补丁并编译的源码归档，删除旧 `.so` 后重新链接，完整执行 build/install/debug 拆分和 RPM/SRPM 打包，没有使用 `--short-circuit`。上面的命令用于从干净环境复现。`w7.zstdio` 只降低验收制品的压缩等级，保留完整 payload 和调试信息；配方不改变仓库默认压缩设置。

`bin/duckdb-fdw-smoke.sql` 验证实际引擎、读写/回滚、NULL、decimal、timestamptz、数组和普通文本、Parquet。`bin/duckdb-fdw-httpfs.sql` 使用匹配 v2.0.0 的官方 `httpfs`，验证加载及回环 HTTP Parquet 读取。仅在一次性数据库执行。

官方测试插件来自 `https://extensions.duckdb.org/v2.0.0/linux_arm64/httpfs.duckdb_extension.gz`，压缩文件 SHA-256 为 `f524888fc7d74cc0c6c4a8f7ed5beedac5b12e71cb426503f882c72ce6afbd43`。它是测试输入，不打入 FDW 包。

## 外部待办

未修改 pgext 元数据库。后续在授权元数据更新时，需要将 upstream/RPM/DEB 版本设为实际验证值，source 改为两个新归档，移除 pg_duckdb 运行依赖，记录同 PG 主版本安装互斥。不要将只完成代表性构建的结果推广为所有平台可用。
