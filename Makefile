CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=c99

# 目标文件
TARGETS = mycat1 mycat2 mycat3 mycat4 mycat5 mycat6

# 默认目标
all: $(TARGETS)

# 编译规则
mycat1: mycat1.c
	$(CC) $(CFLAGS) -o $@ $<

mycat2: mycat2.c
	$(CC) $(CFLAGS) -o $@ $<

mycat3: mycat3.c
	$(CC) $(CFLAGS) -o $@ $<

mycat4: mycat4.c
	$(CC) $(CFLAGS) -o $@ $<

mycat5: mycat5.c
	$(CC) $(CFLAGS) -o $@ $<

mycat6: mycat6.c
	$(CC) $(CFLAGS) -o $@ $<

# 清理目标
clean:
	rm -f $(TARGETS)

# 测试目标
test: all
	@echo "测试所有mycat版本..."
	@echo "确保test.txt文件存在"
	@if [ ! -f test.txt ]; then \
		echo "生成测试文件..."; \
		python3 -c "import random; random.seed(42); open('test.txt', 'wb').write(random.randbytes(2*1024*1024*1024))"; \
	fi
	@echo "运行性能测试..."
	@hyperfine --warmup 1 --runs 3 'cat test.txt > /dev/null'
	@hyperfine --warmup 1 --runs 3 './mycat1 test.txt > /dev/null'
	@hyperfine --warmup 1 --runs 3 './mycat2 test.txt > /dev/null'
	@hyperfine --warmup 1 --runs 3 './mycat3 test.txt > /dev/null'
	@hyperfine --warmup 1 --runs 3 './mycat4 test.txt > /dev/null'
	@hyperfine --warmup 1 --runs 3 './mycat5 test.txt > /dev/null'
	@hyperfine --warmup 1 --runs 3 './mycat6 test.txt > /dev/null'

.PHONY: all clean test 