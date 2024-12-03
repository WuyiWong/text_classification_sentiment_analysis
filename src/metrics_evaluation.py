import pandas as pd
import os
import sys
from datetime import datetime
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.common.script_base import ScriptBase


class MetricsEvaluation(ScriptBase):
    def __init__(self):
        self.info("MetricsEvaluation starting...\n")

    def calculate_metrics_v1(self, **kwargs):

        # 获取ground_truth的结果
        ground_truth_file_path = kwargs.get('ground_truth_file_path', None)
        if ground_truth_file_path == None:
            raise ValueError("The test_file_path does not exist, please check the original path of it")
        df_ground_truth = pd.read_excel(ground_truth_file_path, sheet_name="Sheet1")

        # 获取 llama 模型的结果
        llama_output_file_path = kwargs.get('llama_output_file_path', None)
        df_llama_output = pd.read_excel(llama_output_file_path, sheet_name="Sheet1")

        # df_ground_truth = df_ground_truth.iloc[1: 114]
        mask_1 = df_ground_truth['id'].isin(df_llama_output['id'])
        df_ground_truth_match = df_ground_truth.loc[mask_1].reset_index(drop=True)

        # 获取gpt模型的结果
        gpt_output_file_path = kwargs.get('gpt_output_file_path', None)
        df_gpt_output = pd.read_excel(gpt_output_file_path, sheet_name='MKT_标签分类')
        mask_2 = df_gpt_output['id'].isin(df_ground_truth_match['id'])
        df_gpt_output_match = df_gpt_output.loc[mask_2].reset_index(drop=True)

        # 将结果中 True 变成 positive, False 变成 Negative
        df_gpt_output_match = df_gpt_output_match.replace({1 : "Positive", 0:"Negative"})

        ####### 计算 准确率
        ### 1. 计算 llama输出的准确率
        df_ground_truth_match.drop(['Unnamed: 1', 'Unnamed: 3', '中文翻译'], axis=1, inplace=True)
        
        correct_precisions_llama = 0
        total_precisions_1 = 0
        for column in df_ground_truth_match.columns[2:]: # 遍历每列
            
            # 统计正确预测的个数
            correct_precisions_llama += (df_ground_truth_match[column] == df_llama_output[column]).sum()
            
            # 统计总（Positive, negative, neutral）的个数
            total_precisions_1 += df_ground_truth_match[column].value_counts().sum()

        overall_accuracy_llama = correct_precisions_llama / total_precisions_1
        self.info(f"Overall_accuracy of llama is {overall_accuracy_llama}.")

        ## 2. 计算 gpt 的准确率
        correct_precisions_gpt = 0
        total_precisions_2 = 0
        for column in df_ground_truth_match.columns[2:]:
            # 统计正确预测的个数
            correct_precisions_gpt += (df_ground_truth_match[column] == df_gpt_output_match[column]).sum()

            # 统计总（Positive, negative, neutral）的个数
            total_precisions_2 += df_ground_truth_match[column].value_counts().sum()
        overall_accuracy_gpt = correct_precisions_gpt / total_precisions_2
        self.info(f"Overall_accuracy of gpt is {overall_accuracy_gpt}.\n")
        self.info("End")        
    
    def calculate_metrics_v2(self, ground_truth_file_path, llm_output_file_path, save_path):

        # 获取ground_truth的结果
        df_ground_truth = pd.read_excel(ground_truth_file_path, sheet_name="Sheet1")
        df_ground_truth.drop(['中文翻译'], axis=1, inplace=True)
        
        # 将 NaN 填为 0，将 Positive, Negative, Neutral 分别变成为 1,2,3
        df_ground_truth_filled_0 = df_ground_truth.fillna(0) 
        df_ground_truth_filled = df_ground_truth_filled_0.replace({"Positive": 1, "Negative": 2, "Neutral": 3})
        
        # 获取 大模型 (llama) 的结果
        df_llm_output = pd.read_excel(llm_output_file_path, sheet_name="Sheet1")

        # 输出detail of comparison
        comparison_result_list = []
        for index, row in df_ground_truth.iterrows():
            new_df = pd.concat([row, df_llm_output.iloc[index,:]], axis=1).T.reset_index(drop=True)
            comparison_result_list.append(new_df)
        comparison_result_df = pd.concat(comparison_result_list, axis=0, ignore_index=True)
        if save_path != None:
            self.save_result(comparison_result_df, save_path)

        # 将 NaN 填为 0，将 Positive, Negative, Neutral 分别变成为 1,2,3
        df_llm_output_filled_0 = df_llm_output.fillna(0) 
        df_llm_output_filled = df_llm_output_filled_0.replace({"Positive": 1, "Negative": 2, "Neutral": 3})
        ####### 计算 准确率
        ### 1. 计算 llm 输出的准确率

        
        correct_nums_llm = 0
        total_nums = 0
        # df_ground_truth.drop(['Overall Satisfaction'], axis=1, inplace=True)
        for column in df_ground_truth_filled.columns[2:]: # 遍历每列
            
            # 统计正确预测的个数
            correct_nums_label = (df_ground_truth_filled[column] == df_llm_output_filled[column]).sum()
            correct_nums_llm += correct_nums_label
            
            # 统计总（Positive, negative, neutral）的个数
            total_nums_label = df_ground_truth_filled[column].value_counts().sum()
            total_nums += total_nums_label

            self.info(f"{column}: correct_nums_label is {correct_nums_label}, total_nums_label is {total_nums_label}, label accuracy is {correct_nums_label/total_nums_label}\n")

        overall_accuracy_llm = correct_nums_llm / total_nums
        self.info(f"Overall accuracy of llm is {overall_accuracy_llm}.")

        self.info("End")        
    
    def save_result(self, result_df, save_path):
        if save_path.endswith('xlsx'):
            result_df.to_excel(save_path, index=False)
        elif save_path.endswith('csv'):
            result_df.to_csv(save_path, index=False)

if __name__ == "__main__":

    obj = MetricsEvaluation()
    ground_truth_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/AI Supply Chain/NLP/qms/metrics_evaluation/test_dataset_for_text_sentiment_v2.xlsx'
    # gpt4_output_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/metrics_evaluation/gpt4_result_Mr_Xv_v2.xlsx'
    llama_output_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/AI Supply Chain/NLP/qms/metrics_evaluation/result_of_JSON_format/llama_outputs_two_medium_examples_v3.2_hyper_json.xlsx'
    # business_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/metrics_evaluation/result_of_business_adjustment/业务打标验证.xlsx'

    # qwen_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/metrics_evaluation/result_of_qwen2.5/qwen2.5.xlsx'
    # gpt4o_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/metrics_evaluation/result_of_gpt4o/result_of_gpt4o_v2.xlsx'

    save_path = '/Users/wangwuyi/Documents/1_Projects/UX168/AI Supply Chain/NLP/qms/metrics_evaluation/result_of_JSON_format/comparison_of_llama_v3.2_json.xlsx'
    # adjust_save_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/metrics_evaluation/result_of_business_adjustment/comparison_of_adjustment.xlsx'
    
    obj.calculate_metrics_v2(
        ground_truth_file_path=ground_truth_file_path,
        llm_output_file_path=llama_output_file_path,
        save_path=save_path
    )