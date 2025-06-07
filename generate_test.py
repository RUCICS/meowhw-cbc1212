import random

MB = 1024 * 1024

# A static seed for reproducibility
random.seed(42)

print("正在生成测试文件...")
with open("test.txt", "wb") as f:
    for i in range(128):  # 生成128MB而不是2GB，因为Windows环境测试
        if i % 10 == 0:
            print(f"已生成 {i}MB...")
        f.write(random.randbytes(1 * MB))  # 1MB of random data

print("测试文件生成完成！") 