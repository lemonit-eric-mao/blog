---
title: '计算训练深度学习模型时所需的 GPU 显存大小'
date: '2024-02-22T01:53:26+00:00'
status: private
permalink: /2024/02/22/%e8%ae%a1%e7%ae%97%e8%ae%ad%e7%bb%83%e6%b7%b1%e5%ba%a6%e5%ad%a6%e4%b9%a0%e6%a8%a1%e5%9e%8b%e6%97%b6%e6%89%80%e9%9c%80%e7%9a%84-gpu-%e6%98%be%e5%ad%98%e5%a4%a7%e5%b0%8f
author: 毛巳煜
excerpt: ''
type: post
id: 10669
category:
    - 人工智能
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
calculate\_gpu\_memory.sh
-------------------------

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
    echo "scale=2; <span class="katex math inline">1 / 1024 / 1024 / 1024" | bc
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
phi=</span>(to_gb_from_bytes <span class="katex math inline">phi_in_bytes)

# 计算显存需求
C_model=</span>(echo "2 * <span class="katex math inline">phi" | bc)
C_grad=</span>(echo "2 * <span class="katex math inline">phi" | bc)
C_opti=</span>(echo "4 * <span class="katex math inline">phi * 3" | bc)
C_activation=</span>(echo "<span class="katex math inline">n_layer *</span>batch * (14 * <span class="katex math inline">n_ctx *</span>d_model + 4 * <span class="katex math inline">n_ctx *</span>d_ff + 8 * <span class="katex math inline">n_ctx *</span>n_heads * <span class="katex math inline">d_attn + 5 *</span>n_heads * <span class="katex math inline">n_ctx *</span>n_ctx)" | bc)
C_activation_gb=<span class="katex math inline">(to_gb_from_bytes</span>C_activation)

# 计算总共需要的显存
total_memory=<span class="katex math inline">(echo "</span>C_model + <span class="katex math inline">C_grad +</span>C_opti + <span class="katex math inline">C_activation_gb" | bc)

# 输出显存需求
echo "---------------计算结果-----------------"
echo "模型参数占用显存 (C[model]):</span>C_model GB"
echo "模型梯度占用显存 (C[grad]): <span class="katex math inline">C_grad GB"
echo "优化器状态占用显存 (C[opti]):</span>C_opti GB"
echo "中间激活值占用显存 (C[activation]): <span class="katex math inline">C_activation_gb GB"
echo -e "\033[32m 总共需要显存:</span>total_memory GB \033[0m"

# 判断优化器状态是否变化
read -p "优化器状态是否变化？(y/N): " opti_change
if [ "<span class="katex math inline">opti_change" == "N" ]; then
    total_memory_no_opti=</span>(echo "<span class="katex math inline">C_model +</span>C_grad + <span class="katex math inline">C_activation_gb" | bc)
    echo -e "\033[36m 不计优化器状态变化的情况下，总共需要显存:</span>total_memory_no_opti GB \033[0m"
fi


```