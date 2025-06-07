#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

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
    
    char buffer;
    ssize_t bytes_read;
    
    // 每次读取一个字节
    while ((bytes_read = read(fd, &buffer, 1)) > 0) {
        if (write(STDOUT_FILENO, &buffer, 1) != 1) {
            perror("写入失败");
            close(fd);
            return 1;
        }
    }
    
    if (bytes_read == -1) {
        perror("读取失败");
        close(fd);
        return 1;
    }
    
    close(fd);
    return 0;
} 