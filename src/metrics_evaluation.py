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

    def calculate_metrics(self, **kwargs):

        # 获取ground_truth的结果
        ground_truth_file_path = kwargs.get('ground_truth_file_path', None)
        if ground_truth_file_path == None:
            raise ValueError("The test_file_path does not exist, please check the original path of it")
        df_ground_truth = pd.read_excel(ground_truth_file_path, sheet_name="Sheet2")

        # 获取 llama 模型的结果
        llama_output_file_path = kwargs.get('llama_output_file_path', None)
        df_llama_output = pd.read_excel(llama_output_file_path, sheet_name="Sheet1")

        df_ground_truth = df_ground_truth.iloc[1: 114]
        mask_1 = df_ground_truth['id'].isin(df_llama_output['id'])
        df_ground_truth_match = df_ground_truth.loc[mask_1].reset_index(drop=True)

        # TODO 获取gpt模型的结果
        gpt_output_file_path = kwargs.get('gpt_output_file_path', None)
        df_gpt_output = pd.read_excel(gpt_output_file_path, sheet_name='MKT_标签分类')
        mask_2 = df_gpt_output['id'].isin(df_llama_output['id'])
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
    

if __name__ == "__main__":

    obj = MetricsEvaluation()
    ground_truth_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/metrics_evaluation/GPT-4o_manual_test_set_of_review_sentiment_1031.xlsx'
    llama_output_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/results/llama_outputs_two_medium_examples.xlsx'
    gpt_output_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/schema分类标签结果_MKT_AK数据.xlsx'
    obj.calculate_metrics(
        ground_truth_file_path=ground_truth_file_path,
        llama_output_file_path=llama_output_file_path,
        gpt_output_file_path=gpt_output_file_path
    )