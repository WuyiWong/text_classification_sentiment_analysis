# 这个脚本是用来书写 text classfication and sentiment analysis的主脚本

import pandas as pd
import os
import time
from datetime import datetime

from transformers import AutoTokenizer, AutoModelForCausalLM

# TODO 主脚本部分未完成
# 加载 LLaMA 3.2 模型和分词器
tokenizer = AutoTokenizer.from_pretrained("meta-llama/LLaMA3.2")
model = AutoModelForCausalLM.from_pretrained("meta-llama/LLaMA3.2")

# 遍历数据集中的每条评论，生成对应的 prompt 并进行推理
for index, row in df.iterrows():
    review = row['review_text']
    embedding = row['embedding']
    
    # 使用函数生成 prompt
    final_prompt = create_few_shot_prompt(review, embedding)
    
    # 将 prompt 转换为模型输入的格式
    inputs = tokenizer(final_prompt, return_tensors="pt")
    
    # 使用 LLaMA 3.2 生成输出
    outputs = model.generate(**inputs)
    
    # 解码输出结果
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print(f"Review {index + 1} Result: {decoded_output}\n")
