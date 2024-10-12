import pandas as pd
import os
import time
from sentence_transformers import SentenceTransformer
from datetime import datetime

'''
首先对您的 .csv 数据集进行清理，确保 review_text 和相关的标签列有效。
同时，我们使用 Sentence-BERT 生成每条评论的语义嵌入，这将作为 prompt 的一部分输入。
'''
class DataPrep(object):
    def load_data(self, file_path):
        if file_path.endswith('xlsx'):
            df_mtk = pd.read_excel(file_path, sheet_name='MKT_标签分类')
            df_ak = pd.read_excel(file_path, sheet_name='AK_标签分类')
        elif file_path.endswith('csv'):
            df_mtk = pd.read_csv(file_path, sheet_name='MTK_标签分类')
            df_ak = pd.read_csv(file_path, sheet_name='AK_标签分类')
        
        # 删除空的 review_text
        df_mtk = df_mtk.dropna(subset=['review_text'])
        df_ak = df_ak.dropna(subset=['review_text'])
        
        # 读取 classification_label
        position_index = df_mtk.columns.get_loc('review_text')
        classification_label = df_mtk.columns[position_index+1: ]
        
        # 给 classification_label 赋值 “Others” 标签
        classification_label_list = list(classification_label)
        classification_label_list.append('Others')
        classification_label_added = classification_label_list

        # 合并这两个 df_mtk 和 df_ak 的 review_text
        review_df_mtk = df_mtk.loc[:, 'review_text'] # Series
        review_df_ak = df_ak.loc[:, 'review_text'] # Series
        df_review_text = pd.concat([review_df_mtk, review_df_ak], axis=0, ignore_index=True).to_frame(name='review_text') # dataframe
        
        return df_review_text, classification_label_added
        
    def sentence_embedding(self, df_review_text):
        # 加载 Sentence-Bert 模型来生成语义嵌入
        sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        df_review_text['embedding'] = df_review_text.apply(lambda x: sentence_model.encode(x))
        
        return df_review_text_embedding
    
if __name__ == "__main__":
    data_prep = DataPrep()
    file_path = '/Users/wangwuyi/Documents/1_Projects/UX168/NLP/qms支持/schema分类标签结果_MKT_AK数据.xlsx'
    df_review_text, classification_label = data_prep.load_data(file_path=file_path)
    df_review_text_embedding = data_prep.sentence_embedding(df_review_text)