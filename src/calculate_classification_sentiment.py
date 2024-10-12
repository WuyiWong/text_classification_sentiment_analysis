# 这个脚本是用来书写 text classfication and sentiment analysis的主脚本
import pandas as pd
import os
import time
from datetime import datetime
from src.prompt_design import create_few_shot_prompt
from src.data_preparation import DataPrep

from transformers import AutoTokenizer, AutoModelForCausalLM

class LlamaTextClassificationSentiment(object): # TODO 生成类名

    def __init__(self, model, tokenizer, data_prep):
        self.model = model
        self.tokenizer = tokenizer
        self.data_prep = data_prep

    def generate_classification_and_sentiment(self, df_review_embedding, classification_label):
        # 遍历数据集中的每条评论，生成对应的 prompt 并进行推理
        for index, row in df_review_embedding.iterrows():
            review = row['review_text']
            embedding = row['embedding']
            
            # 使用函数生成 prompt
            final_prompt = create_few_shot_prompt(review, embedding, classification_label)
            
            # 将 prompt 转换为模型输入的格式
            inputs = tokenizer(final_prompt, return_tensors="pt")
            
            # 使用 LLaMA 3.2 生成输出
            outputs = model.generate(**inputs)
            
            # 解码输出结果
            decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            print(f"Review {index + 1} Result: {decoded_output}\n")
    
    
if __name__ == '__main__':
    # 加载 LLaMA 3.2 模型和分词器
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/LLaMA3.2")
    model = AutoModelForCausalLM.from_pretrained("meta-llama/LLaMA3.2")
    # 加载数据集
    data_prep = DataPrep()
    file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms支持/schema分类标签结果_MKT_AK数据.xlsx'
    df_review_text, classification_label = data_prep.load_data(file_path)
    df_review_text_embedding = data_prep.sentence_embedding(df_review_text)

    llama_text_classification_sentiment = LlamaTextClassificationSentiment(model, tokenizer, data_prep)
    llama_text_classification_sentiment.generate_classification_and_sentiment(df_review_text_embedding, classification_label)
