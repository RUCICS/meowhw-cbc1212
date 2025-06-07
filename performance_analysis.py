#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def plot_performance_comparison():
    """绘制所有mycat版本的性能对比图"""
    
    # 这里是模拟数据，实际使用时需要替换为真实的测试结果
    # 时间单位：秒，数值越小越好
    programs = ['cat', 'mycat1', 'mycat2', 'mycat3', 'mycat4', 'mycat5', 'mycat6']
    times = [2.1, 45.2, 3.8, 3.5, 3.2, 2.8, 2.5]  # 示例数据
    
    # 计算相对于cat的性能比
    cat_time = times[0]
    relative_performance = [cat_time / time for time in times]
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # 第一个图：执行时间对比
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']
    bars1 = ax1.bar(programs, times, color=colors, alpha=0.8)
    ax1.set_ylabel('执行时间 (秒)')
    ax1.set_title('不同cat实现的执行时间对比 (2GB文件)')
    ax1.set_yscale('log')  # 使用对数坐标，因为mycat1时间很长
    ax1.grid(axis='y', alpha=0.3)
    
    # 在柱状图上添加数值标签
    for bar, time in zip(bars1, times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{time:.1f}s', ha='center', va='bottom')
    
    # 第二个图：相对性能对比
    bars2 = ax2.bar(programs, relative_performance, color=colors, alpha=0.8)
    ax2.set_ylabel('相对性能 (相对于系统cat)')
    ax2.set_title('相对性能对比 (数值越高越好)')
    ax2.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='系统cat性能基准')
    ax2.grid(axis='y', alpha=0.3)
    ax2.legend()
    
    # 在柱状图上添加数值标签
    for bar, perf in zip(bars2, relative_performance):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{perf:.2f}x', ha='center', va='bottom')
    
    # 旋转x轴标签以避免重叠
    for ax in [ax1, ax2]:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return programs, times, relative_performance

def main():
    """主函数"""
    print("开始性能分析和可视化...")
    plot_performance_comparison()
    print("图表已保存: performance_comparison.png")

if __name__ == "__main__":
    main() 