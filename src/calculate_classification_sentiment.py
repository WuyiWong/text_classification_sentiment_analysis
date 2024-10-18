# 这个脚本是用来书写 text classfication and sentiment analysis的主脚本
import pandas as pd
import os
import time
from datetime import datetime
from data_preparation import DataPrep

from common.script_base import ScriptBase
from prompt_design import PromptTuning
from transformers import AutoTokenizer, AutoModelForCausalLM

class LlamaTextClassificationSentiment(ScriptBase): 

    def __init__(self, model, tokenizer, data_prep):
        self.model = model
        self.tokenizer = tokenizer
        self.data_prep = data_prep

    def generate_classification_and_sentiment_v1(self, df_review, classification_label):
        
        
        # 使用函数生成 prompt
        prompt_tuning = PromptTuning()

        examples = prompt_tuning.examples_prompt()
        fixed_prompt_part = prompt_tuning.create_zero_shot_prompt(
            review='',  # 不传入评论
            categories=classification_label,
            examples=examples
        )
        # 如果不给examples会是什么结果？


        # 遍历数据集中的每条评论，生成对应的 prompt 并进行推理
        for index, row in df_review.iterrows():
            review = row['review_text']
            
            # 在固定的提示部分后添加当前的评论
            final_prompt = f"{fixed_prompt_part}\nReview: '{review}'\nOutputs:"
            # final_prompt = prompt_tuning.create_zero_shot_prompt(\
            #     review=review, categories=classification_label, examples=prompt_tuning.examples_prompt())
            
            # 将 prompt 转换为模型输入的格式
            inputs = self.tokenizer(final_prompt, return_tensors="pt")  # "pt"：返回 PyTorch 张量。
            
            # 获取输入tokens的长度            
            input_ids = inputs['input_ids']
            input_length = input_ids.shape[-1]
            
            # 使用 LLaMA 3.2 生成输出
            outputs = self.model.generate(**inputs, max_new_tokens=50, eos_token_id=self.tokenizer.eos_token_id, pad_token_id=self.tokenizer.eos_token_id)  # **inputs 是 Python 中的解包操作，意味着你将字典 inputs 中的所有键值对作为关键字参数传递给 generate 方法。
            
            # 获取仅由模型生成的 tokens
            generated_tokens = outputs[0][input_length: ]

            # 解码输出结果
            decoded_output = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            # 解析输出结果，提取出对应类别和每个类别的情感倾向
            sentiments_dict = parse_output(decoded_output, classification_label)
            


            self.info(f"Review {index + 1} Result: \n{decoded_output}\n")
    
    def generate_classification_and_sentiment_v2(self, df_review, classification_label):
        
        prompt_tuning = PromptTuning()
        
        # 在循环外生成分类和情感分析的示例
        classification_examples = prompt_tuning.classification_examples_long()
        sentiment_examples = prompt_tuning.sentiment_examples()

        # 遍历数据集中的每条评论，生成对应的 prompt 并进行推理
        for index, row in df_review.iterrows():
            review = row['review_text']
            
            # Step 1: 分类 (调用 create_classification_prompt 函数)
            classification_prompt = prompt_tuning.create_classification_prompt(
                review=review,
                categories=classification_label,
                examples=classification_examples
            )    
            
            # 将分类 prompt 转换为模型输入的格式
            inputs_classification = self.tokenizer(classification_prompt, return_tensors="pt")

            # 使用模型进行分类推理
            classification_outputs = self.model.generate(**inputs_classification, max_new_tokens=40, eos_token_id=self.tokenizer.eos_token_id, pad_token_id=self.tokenizer.eos_token_id)
            
            # 解码分类输出结果
            decoded_classification_output = self.tokenizer.decode(classification_outputs[0], skip_special_tokens=True)

            # 提取分类结果
            predicted_categories = prompt_tuning.extract_categories(decoded_classification_output)

            # 如果未识别出任何类别，跳过情感分析
            if not predicted_categories:
                self.info(f"Review {index + 1} Classification Result:\n {decoded_classification_output}\n")
                self.info(f"Review {index + 1} Sentiment Result:\n No categories identified.\n")
                continue

            # Step 2: 情感分析 (调用 create_sentiment_prompt 函数)
            sentiment_prompt = prompt_tuning.create_sentiment_prompt(
                review=review,
                predicted_categories=predicted_categories,
                examples=sentiment_examples
            )

             # 将情感分析 prompt 转换为模型输入的格式
            inputs_sentiment = self.tokenizer(sentiment_prompt, return_tensors="pt")
            
            # 使用模型进行情感分析推理
            sentiment_outputs = self.model.generate(
                **inputs_sentiment, 
                max_new_tokens=100, 
                eos_token_id=self.tokenizer.eos_token_id, 
                pad_token_id=self.tokenizer.eos_token_id
            )
        
            # 解码情感分析输出结果
            decoded_sentiment_output = self.tokenizer.decode(sentiment_outputs[0], skip_special_tokens=True)

            self.info(f"Review {index + 1} Classification Result:\n {decoded_classification_output}\n")
            self.info(f"Review {index + 1} Sentiment Result:\n {decoded_sentiment_output}\n")


if __name__ == '__main__':
    # 加载 LLaMA 3.2 模型和分词器
    # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
    tokenizer = AutoTokenizer.from_pretrained("/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/Llama-3.2-3B-Instruct")
    # model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
    model = AutoModelForCausalLM.from_pretrained("/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/Llama-3.2-3B-Instruct")
    # 加载数据集
    data_prep = DataPrep()
    file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/schema分类标签结果_MKT_AK数据.xlsx'
    df_review_text, classification_label = data_prep.load_data(file_path)
    # df_review_text = data_prep.sentence_embedding(df_review_text) # 暂时不将sentence embedding的结果直接作为llama的输入来使用

    llama_text_classification_sentiment = LlamaTextClassificationSentiment(model, tokenizer, data_prep)
    llama_text_classification_sentiment.generate_classification_and_sentiment_v1(df_review_text, classification_label)
    # llama_text_classification_sentiment.generate_classification_and_sentiment_v2(df_review_text, classification_label)
