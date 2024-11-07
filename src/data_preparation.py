import pandas as pd
import os
import time
from sentence_transformers import SentenceTransformer
from datetime import datetime
import tqdm

'''
首先对您的 .csv 数据集进行清理，确保 review_text 和相关的标签列有效。
同时，我们使用 Sentence-BERT 生成每条评论的语义嵌入，这将作为 prompt 的一部分输入。
'''
class DataPrep(object):
    def load_data(self, gpt_file_path, test_set_path):
        if gpt_file_path.endswith('xlsx'):
            df_mtk = pd.read_excel(gpt_file_path, sheet_name='MKT_标签分类')
            df_ak = pd.read_excel(gpt_file_path, sheet_name='AK_标签分类')
        elif gpt_file_path.endswith('csv'):
            df_mtk = pd.read_csv(gpt_file_path)
            df_ak = pd.read_csv(gpt_file_path)

        df_test_set = pd.read_excel(test_set_path, sheet_name='Sheet1')
        
        # 删除空的 review_text
        df_mtk = df_mtk.dropna(subset=['review_text'])
        df_ak = df_ak.dropna(subset=['review_text'])
        df_ak.rename(columns={'review_id': 'id'}, inplace=True)
        
        # 读取 classification_label
        position_index = df_mtk.columns.get_loc('review_text')
        classification_label = df_mtk.columns[position_index+1: ]
        
        # 给 classification_label 赋值 “Others” 标签
        classification_label_list = list(classification_label)

        # 合并这两个 df_mtk 和 df_ak 的 review_text
        review_df_mtk = df_mtk.loc[:, ['id', 'review_text']] # Series
        review_df_ak = df_ak.loc[:, ['id', 'review_text']] # Series
        # df_review_text = pd.concat([review_df_mtk, review_df_ak], axis=0, ignore_index=True).to_frame(name='review_text') # dataframe
        df_review_text = pd.concat([review_df_mtk, review_df_ak], axis=0, ignore_index=True)

        df_review_text_filtered = df_review_text.loc[df_review_text['id'].isin(df_test_set['id'])].reset_index(drop=True)

        return df_review_text_filtered, classification_label_list
        
    def sentence_embedding(self, df_review_text):
        # 加载 Sentence-Bert 模型来生成语义嵌入
        sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        tqdm.pandas(desc="Processing...")
        df_review_text['embedding'] = df_review_text['review_text'].progress_apply(lambda x: sentence_model.encode(x)) 
        
        return df_review_text
    
if __name__ == "__main__":
    data_prep = DataPrep()
    gpt_file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms/schema分类标签结果_MKT_AK数据.xlsx'
    test_set_path = None
    df_review_text, classification_label = data_prep.load_data(
        gpt_file_path=gpt_file_path,
        test_set_path=test_set_path

    )
    df_review_text = data_prep.sentence_embedding(df_review_text)