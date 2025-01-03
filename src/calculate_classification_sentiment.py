# 这个脚本是用来书写 text classfication and sentiment analysis的主脚本
import pandas as pd
import os
import time
from datetime import datetime
from data_preparation import DataPrep
import torch
from common.script_base import ScriptBase
from prompt_design_v2 import PromptTuning
from transformers import AutoTokenizer, AutoModelForCausalLM
from parse_outputs import ParseOutput
import sys
import copy

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


    def save_result(self, df_result, save_path):
        
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
            self.info(f"Save path: {save_path} has been created completely!\n")
        
        if save_path.endswith('xlsx'):
            df_result.to_excel(save_path, index=False)
        elif save_path.endswith('csv'):
            df_result.to_csv(save_path, index=False)
        
    
    def generate_classification_and_sentiment_two_step(self, df_review, classification_label):
        
        prompt_tuning = PromptTuning()
        parse_output = ParseOutput()
        
        # 在循环外生成分类和情感分析的示例
        classification_examples = prompt_tuning.classification_examples_medium(classification_label)
        sentiment_examples = prompt_tuning.sentiment_examples_medium()  # 修改prompt examples

        sentiment_classification_list = []
        # 遍历数据集中的每条评论，生成对应的 prompt 并进行推理
        for index, row in df_review.iterrows():
            review = row['review_text']
            
            # Step 1: 分类 (调用 create_classification_prompt 函数)
            classification_prompt = prompt_tuning.create_classification_prompt_v7(
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
                max_new_tokens=128, 
                min_new_tokens=64,
                temperature=0.2, # 0.2
                top_p=0.85, # 0.85
                eos_token_id=self.tokenizer.eos_token_id, pad_token_id=self.tokenizer.eos_token_id
            )
            
            # 获取仅由模型生成的 tokens
            classification_generated_tokens = classification_outputs[0][input_length_classification: ].to('cpu')  # # 解码需要移回CPU

            # 解码分类输出结果
            decoded_classification_output = self.tokenizer.decode(classification_generated_tokens, skip_special_tokens=True)

            # 提取分类结果
            predicted_categories = parse_output.extract_categories(decoded_classification_output, classification_label)

            # 如果未识别出任何类别，再次generate一次
            if not predicted_categories:
            # if len(predicted_categories)==1:
                classification_outputs = self.model.generate(
                **inputs_classification, 
                max_new_tokens=128, 
                min_new_tokens=64,
                temperature=0.4, # 0.1
                top_p=0.8, # 0.7
                eos_token_id=self.tokenizer.eos_token_id, pad_token_id=self.tokenizer.eos_token_id
                )

                classification_generated_tokens = classification_outputs[0][input_length_classification: ].to('cpu')  # # 解码需要移回CPU
                
                decoded_classification_output = self.tokenizer.decode(classification_generated_tokens, skip_special_tokens=True)

                predicted_categories = parse_output.extract_categories(decoded_classification_output, classification_label)
                
                if not predicted_categories:
                    predicted_categories.append('Overall Satisfaction')
                    self.info(f"After 2 rounds of model generation, review {index + 1} still do not have results of classified categories, please check this review {index + 1} in detail!\n")
                    # continue
            
            # character_matching
            predicted_categories = prompt_tuning.character_matching(review, predicted_categories)
            
            # Step 2: 情感分析 (调用 create_sentiment_prompt 函数)
            sentiment_prompt = prompt_tuning.create_sentiment_prompt_v6(
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
                min_new_tokens=64,
                temperature=0.2, # 0.3
                top_p=0.9, # 0.7
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
            
            sentiments_dict['id'] = row['id']

            sentiments_dict = prompt_tuning.sentiment_matching(sentiments_dict, review)
            sentiment_classification_list.append(sentiments_dict)

            self.info(f"Review {index + 1} has processed successfully\n")
            # self.info(f"Review {index + 1} Classification Result:\n {decoded_classification_output}\n")
            # self.info(f"Review {index + 1} Sentiment Result:\n {decoded_sentiment_output}\n")
        df_result = pd.DataFrame(sentiment_classification_list)
        need_to_be_insert = df_result['id']
        df_result.drop(['id'], axis=1, inplace=True)
        df_result.insert(0, need_to_be_insert.name, need_to_be_insert)
        									
        return df_result

    def generate_classification_and_sentiment_two_step_v2(self, df_review, classification_label):
        
        prompt_tuning = PromptTuning()
        parse_output = ParseOutput()
        
        # 在循环外生成分类和情感分析的示例
        classification_examples = prompt_tuning.classification_examples_medium(classification_label)
        sentiment_examples = prompt_tuning.sentiment_examples_medium_v2()  # 修改prompt examples

        sentiment_classification_list = []
        # 遍历数据集中的每条评论，生成对应的 prompt 并进行推理
        for index, row in df_review.iterrows():
            review = row['review_text']
            
            # Step 1: 分类 (调用 create_classification_prompt 函数)
            classification_prompt = prompt_tuning.create_classification_prompt_v11(
                review=review,
                categories=classification_label,
                classification_examples=classification_examples
            )    
            
            # 将分类 prompt 转换为模型输入的格式
            inputs_classification = self.tokenizer(classification_prompt, return_tensors="pt").to(self.device)

            # 获取输入tokens的长度            
            input_ids_classification = inputs_classification['input_ids']
            input_length_classification = input_ids_classification.shape[-1]

            # 使用 LLaMA 3.2 生成输出 stage 1
            classification_outputs = self.model.generate(
                **inputs_classification, 
                max_new_tokens=128, 
                min_new_tokens=64,
                temperature=0.2, # 0.2
                top_p=0.85, # 0.85
                eos_token_id=self.tokenizer.eos_token_id, pad_token_id=self.tokenizer.eos_token_id
            )
            
            # 获取仅由模型生成的 tokens
            classification_generated_tokens = classification_outputs[0][input_length_classification: ].to('cpu')  # # 解码需要移回CPU

            # 解码分类输出结果
            decoded_classification_output = self.tokenizer.decode(classification_generated_tokens, skip_special_tokens=True)

            # 提取分类结果
            predicted_categories = parse_output.extract_categories(decoded_classification_output, classification_label)

            # 将初步的分类结果保存到 predicted_categories_final
            predicted_categories_final = copy.deepcopy(predicted_categories)  

            # 为了防止第一个hyperparameter过于保守，所以如果只有一个category的情况下，再次进行LLM预测
            if len(predicted_categories)==1: # stage 2
                classification_outputs = self.model.generate(
                **inputs_classification, 
                max_new_tokens=128, 
                min_new_tokens=64,
                temperature=0.4, # 0.1
                top_p=0.8, # 0.7
                eos_token_id=self.tokenizer.eos_token_id, pad_token_id=self.tokenizer.eos_token_id
                )

                classification_generated_tokens = classification_outputs[0][input_length_classification: ].to('cpu')  # # 解码需要移回CPU
                
                decoded_classification_output = self.tokenizer.decode(classification_generated_tokens, skip_special_tokens=True)

                predicted_categories_stage2 = parse_output.extract_categories(decoded_classification_output, classification_label)
                
                if set(predicted_categories) <= set(predicted_categories_stage2):
                    predicted_categories_final = copy.deepcopy(predicted_categories_stage2)
            
            """
            下面这行代码的目的是获取stage2 的额外分类结果, 后续如果对此情感倾向分为Neutral, 那么则将此类别删除，变成None
            eg:
                1. predicted_categories=['Size and Fit'] 
                2. predicted_categories_stage2 = ['Size and Fit', 'Design and Appearance', 'Product Quality', 'Overall Satisfaction']
                3. predicted_categories_final_residual = ['Product Quality', 'Overall Satisfaction', 'Design and Appearance']
            """
            if len(predicted_categories) > 1:
                predicted_categories_stage2 = []
            predicted_categories_stage2_residual = list(set(predicted_categories_stage2) - set(predicted_categories))

            # start stage 3 of the text classification
            predicted_categories_final = prompt_tuning.character_matching(review, predicted_categories_final)
            
            # Step 2: 情感分析 (调用 create_sentiment_prompt 函数)
            sentiment_prompt = prompt_tuning.create_sentiment_prompt_v9(
                review=review,
                predicted_categories=predicted_categories_final,
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
                min_new_tokens=64,
                temperature=0.2, # 0.3
                top_p=0.9, # 0.7
                eos_token_id=self.tokenizer.eos_token_id, 
                pad_token_id=self.tokenizer.eos_token_id
            )
        
            # 获取仅由模型生成的 tokens
            sentiment_generated_tokens = sentiment_outputs[0][input_length_sentiments: ].to('cpu')  # 解码需要移回CPU

            # 解码情感分析输出结果
            decoded_sentiment_output = self.tokenizer.decode(sentiment_generated_tokens, skip_special_tokens=True)

            # 将输出结果，提取出对应类别和每个类别的情感倾向
            sentiments_dict = parse_output.parse_output_sentiment_classification_v2(decoded_sentiment_output, predicted_categories_stage2_residual, classification_label, review)

            # 判断模型输出类别是否正确
            sentiments_keys = list(sentiments_dict.keys())
            for category in sentiments_keys:
                if category == 'review_text':
                    continue
                if category not in classification_label:
                    del sentiments_dict[category] # 删除对应的键值对
            
            sentiments_dict['id'] = row['id']

            sentiments_dict = prompt_tuning.sentiment_matching_v2(sentiments_dict, review)
            sentiment_classification_list.append(sentiments_dict)

            self.info(f"Review {index + 1} has processed successfully\n")
            # self.info(f"Review {index + 1} Classification Result:\n {decoded_classification_output}\n")
            # self.info(f"Review {index + 1} Sentiment Result:\n {decoded_sentiment_output}\n")
        df_result = pd.DataFrame(sentiment_classification_list)
        need_to_be_insert = df_result['id']
        df_result.drop(['id'], axis=1, inplace=True)
        df_result.insert(0, need_to_be_insert.name, need_to_be_insert)
        									
        return df_result



if __name__ == '__main__':
    # 加载 LLaMA 3.2 模型和分词器
    model_id_3b = "/home/featurize/data/Llama-3.2-3B-Instruct"
    model_id_8b = "/home/featurize/data/Llama-3.1-8B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id_3b, trust_remote_code=True)
    # tokenizer = AutoTokenizer.from_pretrained("/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/Llama-3.2-3B-Instruct")

    model = AutoModelForCausalLM.from_pretrained(model_id_3b, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True).eval()  # TODO 在GPU上推理时打开
    # model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct").eval()

    # model = AutoModelForCausalLM.from_pretrained("/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/Llama-3.2-3B-Instruct")
    # 加载数据集
    data_prep = DataPrep()
    file_path = '/home/featurize/work/projects/text_classification_sentiment_analysis/input/schema分类标签结果_MKT_AK数据_v2.xlsx'
    test_set_path = '/home/featurize/work/projects/text_classification_sentiment_analysis/metrics_evaluation/test_dataset_for_text_sentiment_v2.xlsx'
    # test_set_path = '/home/featurize/work/projects/text_classification_sentiment_analysis/metrics_evaluation/问题reviews.xlsx'
    
    df_review_text, classification_label = data_prep.load_data(file_path, test_set_path)
    # df_review_text = data_prep.sentence_embedding(df_review_text) # 暂时不将sentence embedding的结果直接作为llama的输入来使用

    llama_text_classification_sentiment = LlamaTextClassificationSentiment(model, tokenizer, data_prep)
    
    if len(sys.argv) == 1: 
        save_path = '/home/featurize/work/projects/text_classification_sentiment_analysis/results/llama_outputs_two_medium_examples_v3.2_hyper.xlsx'
        df_llama_sentiments_classfication_cat = llama_text_classification_sentiment.generate_classification_and_sentiment_two_step_v2(df_review_text, classification_label)
        llama_text_classification_sentiment.save_result(df_llama_sentiments_classfication_cat, save_path)
