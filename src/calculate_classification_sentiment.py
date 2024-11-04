# 这个脚本是用来书写 text classfication and sentiment analysis的主脚本
import pandas as pd
import os
import time
from datetime import datetime
from data_preparation import DataPrep
import torch
from common.script_base import ScriptBase
from prompt_design import PromptTuning
from transformers import AutoTokenizer, AutoModelForCausalLM
from parse_outputs import ParseOutput
import sys

class LlamaTextClassificationSentiment(ScriptBase): 

    def __init__(self, model, tokenizer, data_prep):
        # 判断是否支持MPS，如果支持则将模型移动到MPS，否则保持在CPU上
        
        if torch.cuda.is_available():
            self.model = model.to('cuda')  # 将模型移动到MPS设备上
            self.device = torch.device('cuda')
            print("CUDA device is available, using CUDA for computation.")
            
        else:
            self.model = model.to('cpu')
            self.device = torch.device('cpu')
            print("CUDA device is not available, using CPU for computation.")
        self.tokenizer = tokenizer
        self.data_prep = data_prep

    def generate_classification_and_sentiment_v1(self, df_review, classification_label):
        
        
        # 使用函数生成 prompt
        prompt_tuning = PromptTuning()

        examples = prompt_tuning.examples_prompt_combined_medium()
        fixed_prompt_part = prompt_tuning.create_prompt_combined(
            review='',  # 不传入评论
            categories=classification_label,
            examples=examples
        )
        
        parse_output_obj = ParseOutput()

        sentiment_classification_list = []
        # 遍历数据集中的每条评论，生成对应的 prompt 并进行推理
        for index, row in df_review.iterrows():
            review = row['review_text']
            
            # 在固定的提示部分后添加当前的评论
            final_prompt = f"{fixed_prompt_part}\nReview: '{review}'\nOutputs:"
            # final_prompt = prompt_tuning.create_zero_shot_prompt(\
            #     review=review, categories=classification_label, examples=prompt_tuning.examples_prompt())
            
            # 将 prompt 转换为模型输入的格式
            inputs = self.tokenizer(final_prompt, return_tensors="pt").to(self.device)  # "pt"：返回 PyTorch 张量。并且根据设备移动输入到MPS或CPU
            
            # 获取输入tokens的长度            
            input_ids = inputs['input_ids']
            input_length = input_ids.shape[-1]
            
            # 使用 LLaMA 3.2 生成输出
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=128, 
                temperature=0.2, 
                top_p=0.7, 
                eos_token_id=self.tokenizer.eos_token_id, 
                pad_token_id=self.tokenizer.eos_token_id
            )  # **inputs 是 Python 中的解包操作，意味着你将字典 inputs 中的所有键值对作为关键字参数传递给 generate 方法。
            
            # 获取仅由模型生成的 tokens
            generated_tokens = outputs[0][input_length: ].to('cpu')

            # 解码输出结果
            decoded_output = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            # 将输出结果，提取出对应类别和每个类别的情感倾向
            sentiments_dict = parse_output_obj.parse_output_sentiment_classification(decoded_output, classification_label, review)
            
            # 判断模型输出类别是否正确
            sentiment_dict_keys = list(sentiments_dict.keys())
            for category in sentiment_dict_keys:
                if category == 'review_text':
                    continue
                if category not in classification_label:
                    del sentiments_dict[category] # 删除对应的键值对

            sentiment_classification_list.append(sentiments_dict)
            self.info(f"Review {index + 1} has processed successfully\n")
            
            if index + 1 >= 100:
                break

            # self.info(f"Review {index + 1} Result: \n{decoded_output}\n")
        df_result = pd.DataFrame(sentiment_classification_list)

        return df_result

    def save_result(self, df_result, save_path):
        
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
            self.info(f"Save path: {save_path} has been created completely!\n")
        
        if save_path.endswith('xlsx'):
            df_result.to_excel(save_path, index=False)
        elif save_path.endswith('csv'):
            df_result.to_csv(save_path, index=False)
        

    
    def generate_classification_and_sentiment_v2(self, df_review, classification_label):
        
        prompt_tuning = PromptTuning()
        parse_output = ParseOutput()
        
        # 在循环外生成分类和情感分析的示例
        classification_examples = prompt_tuning.classification_examples_v2_medium(classification_label)
        sentiment_examples = prompt_tuning.sentiment_examples_v2()

        sentiment_classification_list = []
        # 遍历数据集中的每条评论，生成对应的 prompt 并进行推理
        for index, row in df_review.iterrows():
            review = row['review_text']
            
            # Step 1: 分类 (调用 create_classification_prompt 函数)
            classification_prompt = prompt_tuning.create_classification_prompt_v2(
                review=review,
                categories=classification_label,
                classification_examples=classification_examples
            )    
            
            # 将分类 prompt 转换为模型输入的格式
            inputs_classification = self.tokenizer(classification_prompt, return_tensors="pt").to(self.device)

            # 获取输入tokens的长度            
            input_ids_classification = inputs_classification['input_ids']
            input_length_classification = input_ids_classification.shape[-1]

            # 使用 LLaMA 3.2 生成输出
            classification_outputs = self.model.generate(
                **inputs_classification, 
                max_new_tokens=64, 
                temperature=0.2, # 0.1
                top_p=0.6,
                eos_token_id=self.tokenizer.eos_token_id, pad_token_id=self.tokenizer.eos_token_id
            )
            
            # 获取仅由模型生成的 tokens
            classification_generated_tokens = classification_outputs[0][input_length_classification: ].to('cpu')  # # 解码需要移回CPU

            # 解码分类输出结果
            decoded_classification_output = self.tokenizer.decode(classification_generated_tokens, skip_special_tokens=True)

            # 提取分类结果
            predicted_categories = parse_output.extract_categories(decoded_classification_output, classification_label)

            # 如果未识别出任何类别，跳过情感分析
            if not predicted_categories:
                # self.info(f"Review {index + 1} Classification Result:\n {decoded_classification_output}\n")
                self.info(f"Review {index + 1} Sentiment Result:\n No categories identified.\n")
                continue

            # Step 2: 情感分析 (调用 create_sentiment_prompt 函数)
            sentiment_prompt = prompt_tuning.create_sentiment_prompt_v2(
                review=review,
                predicted_categories=predicted_categories,
                examples=sentiment_examples
            )

             # 将情感分析 prompt 转换为模型输入的格式并移动到正确设备
            inputs_sentiment = self.tokenizer(sentiment_prompt, return_tensors="pt").to(self.device)
            
            # 获取输入tokens的长度            
            input_length_sentiments = inputs_sentiment['input_ids'].shape[-1]

            # 使用模型进行情感分析推理
            sentiment_outputs = self.model.generate(
                **inputs_sentiment, 
                max_new_tokens=256, 
                temperature=0.2, # 0.3
                top_p=0.8, # 0.7
                eos_token_id=self.tokenizer.eos_token_id, 
                pad_token_id=self.tokenizer.eos_token_id
            )
        
            # 获取仅由模型生成的 tokens
            sentiment_generated_tokens = sentiment_outputs[0][input_length_sentiments: ].to('cpu')  # 解码需要移回CPU

            # 解码情感分析输出结果
            decoded_sentiment_output = self.tokenizer.decode(sentiment_generated_tokens, skip_special_tokens=True)

            # 将输出结果，提取出对应类别和每个类别的情感倾向
            sentiments_dict = parse_output.parse_output_sentiment_classification(decoded_sentiment_output, classification_label, review)

            # 判断模型输出类别是否正确
            sentiments_keys = list(sentiments_dict.keys())
            for category in sentiments_keys:
                if category == 'review_text':
                    continue
                if category not in classification_label:
                    del sentiments_dict[category] # 删除对应的键值对
            
            sentiment_classification_list.append(sentiments_dict)

            self.info(f"Review {index + 1} has processed successfully\n")
            if index + 1 >= 100:
                break
            # self.info(f"Review {index + 1} Classification Result:\n {decoded_classification_output}\n")
            # self.info(f"Review {index + 1} Sentiment Result:\n {decoded_sentiment_output}\n")
        df_result = pd.DataFrame(sentiment_classification_list)
        return df_result

if __name__ == '__main__':
    # 加载 LLaMA 3.2 模型和分词器
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", trust_remote_code=True)
    # tokenizer = AutoTokenizer.from_pretrained("/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/Llama-3.2-3B-Instruct")
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True).eval()
    # model = AutoModelForCausalLM.from_pretrained("/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/Llama-3.2-3B-Instruct")
    # 加载数据集
    data_prep = DataPrep()
    file_path = '/home/featurize/work/projects/text_classification_sentiment_analysis/input/schema分类标签结果_MKT_AK数据.xlsx'
    


    df_review_text, classification_label = data_prep.load_data(file_path)
    # df_review_text = data_prep.sentence_embedding(df_review_text) # 暂时不将sentence embedding的结果直接作为llama的输入来使用

    llama_text_classification_sentiment = LlamaTextClassificationSentiment(model, tokenizer, data_prep)
    
    if len(sys.argv) == 2:
        prompt_type = sys.argv[1]

        if prompt_type == "one":
            save_path = '/home/featurize/work/projects/text_classification_sentiment_analysis/results/llama_outputs_one_long.xlsx'
            df_llama_sentiments_classfication = llama_text_classification_sentiment.generate_classification_and_sentiment_v1(df_review_text, classification_label)
            llama_text_classification_sentiment.save_result(df_llama_sentiments_classfication, save_path)
        elif prompt_type == "two":
            save_path = '/home/featurize/work/projects/text_classification_sentiment_analysis/results/llama_outputs_two.xlsx'
            df_llama_sentiments_classfication_cat = llama_text_classification_sentiment.generate_classification_and_sentiment_v2(df_review_text, classification_label)
            llama_text_classification_sentiment.save_result(df_llama_sentiments_classfication_cat, save_path)
    if len(sys.argv) == 1:
        save_path = '/home/featurize/work/projects/text_classification_sentiment_analysis/results/llama_outputs_two_medium_examples.xlsx'
        df_llama_sentiments_classfication_cat = llama_text_classification_sentiment.generate_classification_and_sentiment_v2(df_review_text, classification_label)
        llama_text_classification_sentiment.save_result(df_llama_sentiments_classfication_cat, save_path)