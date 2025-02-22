# vchord building caveats

Ubuntu 24 直接安装 Clang 即可

```bash
apt install clang
```

To build this extension, you'll need [clang-17+](https://github.com/tensorchord/VectorChord/issues/188)

You can install `clang` on Ubuntu 24 directly, and install clang-18 on Ubuntu 22 / Debian 12 with:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://apt.llvm.org/llvm.sh | bash -s -- 18
sudo update-alternatives --install /usr/bin/clang clang $(which clang-18) 255
```