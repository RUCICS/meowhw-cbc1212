#!/usr/bin/env python3
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np

def test_dd_performance(block_size):
    """测试使用dd命令在指定块大小下的性能"""
    try:
        # 使用dd从/dev/zero读取并写入/dev/null，测试纯IO性能
        cmd = [
            'dd', 
            'if=/dev/zero', 
            'of=/dev/null', 
            f'bs={block_size}', 
            'count=100000',
            'status=progress'
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        
        # 从dd的输出中提取速度信息
        if result.stderr:
            lines = result.stderr.strip().split('\n')
            for line in lines:
                if 'MB/s' in line or 'GB/s' in line:
                    # 解析速度
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if 'MB/s' in part:
                            speed_str = parts[i-1]
                            return float(speed_str)
                        elif 'GB/s' in part:
                            speed_str = parts[i-1]
                            return float(speed_str) * 1024
        
        # 如果无法从输出中解析速度，则根据时间计算
        # 100000 块 * block_size 字节 / 时间
        total_bytes = 100000 * block_size
        speed_mb_per_sec = (total_bytes / (1024 * 1024)) / elapsed_time
        return speed_mb_per_sec
        
    except subprocess.TimeoutExpired:
        return 0
    except Exception as e:
        print(f"测试块大小 {block_size} 时出错: {e}")
        return 0

def main():
    # 测试不同的缓冲区大小（以字节为单位）
    # 从4KB到1MB，以2的幂递增
    block_sizes = [4096 * (2**i) for i in range(8)]  # 4KB, 8KB, 16KB, ..., 1MB
    block_size_labels = ['4KB', '8KB', '16KB', '32KB', '64KB', '128KB', '256KB', '512KB']
    
    speeds = []
    
    print("开始测试不同缓冲区大小的性能...")
    print("这可能需要几分钟时间...")
    
    for i, block_size in enumerate(block_sizes):
        print(f"测试缓冲区大小: {block_size_labels[i]}")
        speed = test_dd_performance(block_size)
        speeds.append(speed)
        print(f"速度: {speed:.2f} MB/s")
        time.sleep(1)  # 稍微暂停一下
    
    # 绘制结果
    plt.figure(figsize=(12, 8))
    plt.bar(block_size_labels, speeds, color='skyblue', alpha=0.7)
    plt.xlabel('缓冲区大小')
    plt.ylabel('读写速度 (MB/s)')
    plt.title('不同缓冲区大小下的IO性能')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    
    # 在柱状图上显示数值
    for i, speed in enumerate(speeds):
        plt.text(i, speed + max(speeds) * 0.01, f'{speed:.1f}', 
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('buffer_size_performance.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 找到最佳缓冲区大小
    max_speed_idx = speeds.index(max(speeds))
    optimal_size = block_sizes[max_speed_idx]
    
    print(f"\n实验结果:")
    print(f"最佳缓冲区大小: {block_size_labels[max_speed_idx]} ({optimal_size} 字节)")
    print(f"最高速度: {max(speeds):.2f} MB/s")
    
    # 分析性能平台期
    print(f"\n性能分析:")
    for i, (size_label, speed) in enumerate(zip(block_size_labels, speeds)):
        if speed >= max(speeds) * 0.95:  # 在最高性能的95%以内
            print(f"{size_label}: {speed:.2f} MB/s (接近最优)")
    
    return block_sizes, speeds

if __name__ == "__main__":
    main() 