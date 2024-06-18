---
title: "计算训练深度学习模型时所需的 GPU 显存大小"
date: "2024-02-22"
categories: 
  - "人工智能"
---

## calculate\_gpu\_memory.sh

```bash
#!/bin/bash

## 用法 以 ChatGLM3-6B 模型为例
# sh calculate_gpu_memory.sh
# 请依次输入模型的参数：
# 模型参数大小 (φ)（以字节为单位）: 6000000000
# 模型层数 (n[layer]): 28
# 隐藏层大小 (d[model]): 4096
# 中间隐藏层大小 (d[ff]): 16384
# 注意力头数 (n[heads]): 32
# 上下文大小 (n[ctx]): 2048
# 注意力输出维度大小 (d[attn]): 1
# 批大小 (Batch size): 1


# 函数：将字节单位转换为GB
to_gb_from_bytes() {
    echo "scale=2; $1 / 1024 / 1024 / 1024" | bc
}

# 获取模型参数
echo "请依次输入模型的参数："
read -p "模型参数大小 (φ)（以字节为单位）: " phi_in_bytes
read -p "模型层数 (n[layer]): " n_layer
read -p "隐藏层大小 (d[model]): " d_model
read -p "中间隐藏层大小 (d[ff]): " d_ff
read -p "注意力头数 (n[heads]): " n_heads
read -p "上下文大小 (n[ctx]): " n_ctx
read -p "注意力输出维度大小 (d[attn]): " d_attn
read -p "批大小 (Batch size): " batch

# 显存计算的常量
phi=$(to_gb_from_bytes $phi_in_bytes)

# 计算显存需求
C_model=$(echo "2 * $phi" | bc)
C_grad=$(echo "2 * $phi" | bc)
C_opti=$(echo "4 * $phi * 3" | bc)
C_activation=$(echo "$n_layer * $batch * (14 * $n_ctx * $d_model + 4 * $n_ctx * $d_ff + 8 * $n_ctx * $n_heads * $d_attn + 5 * $n_heads * $n_ctx * $n_ctx)" | bc)
C_activation_gb=$(to_gb_from_bytes $C_activation)

# 计算总共需要的显存
total_memory=$(echo "$C_model + $C_grad + $C_opti + $C_activation_gb" | bc)

# 输出显存需求
echo "---------------计算结果-----------------"
echo "模型参数占用显存 (C[model]): $C_model GB"
echo "模型梯度占用显存 (C[grad]): $C_grad GB"
echo "优化器状态占用显存 (C[opti]): $C_opti GB"
echo "中间激活值占用显存 (C[activation]): $C_activation_gb GB"
echo -e "\033[32m 总共需要显存: $total_memory GB \033[0m"

# 判断优化器状态是否变化
read -p "优化器状态是否变化？(y/N): " opti_change
if [ "$opti_change" == "N" ]; then
    total_memory_no_opti=$(echo "$C_model + $C_grad + $C_activation_gb" | bc)
    echo -e "\033[36m 不计优化器状态变化的情况下，总共需要显存: $total_memory_no_opti GB \033[0m"
fi

```
