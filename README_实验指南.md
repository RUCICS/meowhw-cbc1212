# MeowLab 实验运行指南

这是一个探索cat命令性能优化的系统编程实验项目。通过实现多个版本的cat程序，我们将学习缓冲区设计、内存对齐、文件系统优化等高性能IO编程技术。

## 环境要求

- Linux操作系统（推荐Ubuntu 20.04+）
- GCC编译器
- Python 3.x
- matplotlib库（用于绘图）
- hyperfine工具（用于性能测试）

## 安装依赖

```bash
# 安装编译工具
sudo apt update
sudo apt install build-essential

# 安装Python依赖
pip3 install matplotlib numpy

# 安装hyperfine
# 方法1: 使用cargo安装
cargo install hyperfine

# 方法2: 使用包管理器安装
sudo apt install hyperfine
```

## 快速开始

### 1. 编译所有mycat版本

```bash
make all
```

### 2. 生成测试文件

```bash
python3 -c "
import random
random.seed(42)
with open('test.txt', 'wb') as f:
    for _ in range(2048):
        f.write(random.randbytes(1024*1024))
"
```

### 3. 运行性能测试

```bash
make test
```

## 各版本说明

- **mycat1**: 基础版本，每次读取1字节
- **mycat2**: 添加页大小缓冲区
- **mycat3**: 内存页对齐优化
- **mycat4**: 文件系统块大小对齐
- **mycat5**: 优化缓冲区大小
- **mycat6**: fadvise系统调用优化

## 实验任务

### 缓冲区大小实验
```bash
python3 buffer_size_test.py
```

### 性能分析
```bash
python3 performance_analysis.py
```

## 清理
```bash
make clean
``` 