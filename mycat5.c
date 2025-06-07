#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <sys/stat.h>

// 获取最大公约数
size_t gcd(size_t a, size_t b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}

// 获取最小公倍数
size_t lcm(size_t a, size_t b) {
    return (a / gcd(a, b)) * b;
}

// 检查是否为2的幂
int is_power_of_two(size_t n) {
    return n > 0 && (n & (n - 1)) == 0;
}

// 获取IO缓冲区大小，考虑系统调用开销
size_t io_blocksize(int fd) {
    long page_size = sysconf(_SC_PAGESIZE);
    if (page_size == -1) {
        page_size = 4096; // 默认值
    }
    
    struct stat file_stat;
    if (fstat(fd, &file_stat) == -1) {
        return (size_t)page_size * 16; // 出错时使用64KB
    }
    
    size_t fs_block_size = (size_t)file_stat.st_blksize;
    
    // 检查文件系统块大小是否合理（是2的幂且不超过1MB）
    if (!is_power_of_two(fs_block_size) || fs_block_size > 1024 * 1024) {
        fs_block_size = (size_t)page_size;
    }
    
    // 返回内存页大小和文件系统块大小的最小公倍数
    size_t base_size = lcm((size_t)page_size, fs_block_size);
    
    // 根据实验结果，使用16倍的基础大小来减少系统调用开销
    // 这通常会产生64KB-128KB的缓冲区
    size_t buffer_size = base_size * 16;
    
    // 限制缓冲区大小在合理范围内（64KB-256KB）
    if (buffer_size < 64 * 1024) {
        buffer_size = 64 * 1024;
    } else if (buffer_size > 256 * 1024) {
        buffer_size = 256 * 1024;
    }
    
    return buffer_size;
}

// 分配页对齐的内存
char* align_alloc(size_t size) {
    void *ptr;
    long page_size = sysconf(_SC_PAGESIZE);
    if (page_size == -1) {
        page_size = 4096;
    }
    
    // 使用posix_memalign进行页对齐分配
    if (posix_memalign(&ptr, (size_t)page_size, size) != 0) {
        return NULL;
    }
    return (char*)ptr;
}

// 释放页对齐的内存
void align_free(void* ptr) {
    if (ptr != NULL) {
        free(ptr);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "用法: %s <文件名>\n", argv[0]);
        return 1;
    }
    
    int fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        perror("打开文件失败");
        return 1;
    }
    
    size_t buffer_size = io_blocksize(fd);
    char *buffer = align_alloc(buffer_size);
    if (buffer == NULL) {
        perror("页对齐内存分配失败");
        close(fd);
        return 1;
    }
    
    ssize_t bytes_read;
    
    while ((bytes_read = read(fd, buffer, buffer_size)) > 0) {
        ssize_t bytes_written = 0;
        while (bytes_written < bytes_read) {
            ssize_t result = write(STDOUT_FILENO, buffer + bytes_written, 
                                 bytes_read - bytes_written);
            if (result == -1) {
                perror("写入失败");
                align_free(buffer);
                close(fd);
                return 1;
            }
            bytes_written += result;
        }
    }
    
    if (bytes_read == -1) {
        perror("读取失败");
        align_free(buffer);
        close(fd);
        return 1;
    }
    
    align_free(buffer);
    close(fd);
    return 0;
} 