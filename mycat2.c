#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

// 获取IO缓冲区大小
size_t io_blocksize() {
    long page_size = sysconf(_SC_PAGESIZE);
    if (page_size == -1) {
        // 如果获取失败，使用默认值4KB
        return 4096;
    }
    return (size_t)page_size;
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
    
    size_t buffer_size = io_blocksize();
    char *buffer = malloc(buffer_size);
    if (buffer == NULL) {
        perror("内存分配失败");
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
                free(buffer);
                close(fd);
                return 1;
            }
            bytes_written += result;
        }
    }
    
    if (bytes_read == -1) {
        perror("读取失败");
        free(buffer);
        close(fd);
        return 1;
    }
    
    free(buffer);
    close(fd);
    return 0;
} 