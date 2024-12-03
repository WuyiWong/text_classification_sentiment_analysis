from common.script_base import ScriptBase
import ast
import re
class ParseOutput(ScriptBase):

    def parse_output_sentiment_classification(self, decoded_output, categories, review_text):
        """
        Purpose:
            这个函数使用来解析输出，将输出解析成每个类别，和对应类别的sentiment
        Input:
            1. outputs: 是tokenizer decode 的输出。
            2. categories: 是reviews text的类别，包括：
                categories: = ['Usage Scenarios and Applicability', 'Price and Value', 'Shipping and Packaging', 
                                'Design and Appearance', 'Product Quality', 'Size and Fit', 
                                'Washing and Maintenance', 'Overall Satisfaction', 'Comfort', 
                                'Brand and Customer Service', 'Others']
            3. review_text: 这是具体的评论内容
        Output:
            sentiments_dict: 一个可以为每个类别输出情感倾向的字典(dict)
        """
        sentiments_dict = {'review_text': review_text}

        # 初始化所有类别的值为 None
        for category in categories:
            sentiments_dict[category] = None

        # 解析 decoded_output
        lines = decoded_output.strip().split('\n')
        # index = 0 # 初始化index 用来作为正确输出的结尾index
        for i, element in enumerate(lines):
            if '-' not in element:
                index = i
                break
        lines = lines[: index]
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                parts = line[1:].split(':')
            else:
                parts = line.split(':') # 这里eg: parts = ['Design and Appearance', 'Negative', ...]
            if len(parts) >= 2:
                category_name = parts[0].strip()
                sentiment = parts[1].strip()
                # 将情感赋值给对应类别
                sentiments_dict[category_name] = sentiment

        return sentiments_dict
    
    def parse_output_sentiment_classification_v2(self, classification_sentiment_list, predict_categories_stage2_residual, categories, review_text):
        """
        Purpose:
            这个函数使用来解析输出，将输出解析成每个类别，和对应类别的sentiment
            ps:
                这里添加了新功能：判断这个类别是否是在 stage2 生成的分类。如果是，并且 情感倾向判定不为 'Neutral', 则将情感赋值为对应类别
        Input:
            1. decoded_output: 是tokenizer decode 的输出。
            2. predict_categories_stage2_residual: 是在文本分类中stage2输出的新结果，不在stage1中
            3. categories: 是reviews text的类别，包括：
                categories: = ['Usage Scenarios and Applicability', 'Price and Value', 'Shipping and Packaging', 
                                'Design and Appearance', 'Product Quality', 'Size and Fit', 
                                'Washing and Maintenance', 'Overall Satisfaction', 'Comfort', 
                                'Brand and Customer Service']
            4. review_text: 这是具体的评论内容
        Output:
            sentiments_dict: 一个可以为每个类别输出情感倾向的字典(dict)
        """
        sentiments_dict = {'review_text': review_text}

        # 初始化所有类别的值为 None
        for category in categories:
            sentiments_dict[category] = None

        # 判断 classification_sentiment_list 的每个元素是否是tuple
        if all(isinstance(item, tuple) for item in classification_sentiment_list): 
            for pair in classification_sentiment_list:
                category = pair[0].strip()
                sentiment = pair[1].strip()
                if sentiment not in ['Positive', 'Negative', 'Neutral']:
                    continue
                if category in predict_categories_stage2_residual:
                    if sentiment != 'Neutral':
                        # 将情感赋值给对应类别
                        sentiments_dict[category] = sentiment
                elif category in categories:
                    sentiments_dict[category] = sentiment
        # 判断 classification_sentiment_list 的每个元素是否是 string
        elif all(isinstance(item, str) for item in classification_sentiment_list):
            for index in range(0, len(classification_sentiment_list), 2):
                classification_sentiment_list_ = classification_sentiment_list[index: index+2]
                category = classification_sentiment_list_[index]
                sentiment = classification_sentiment_list_[index+1]

                if category in predict_categories_stage2_residual:
                    if sentiment != 'Neutral':
                        # 将情感赋值给对应类别
                        sentiments_dict[category] = sentiment
                else:
                    sentiments_dict[category] = sentiment

        return sentiments_dict
    
    def parse_decoded_output(self, decoded_output_ori):
        classification_sentiment_list = list(set(re.findall(r"\('([^']+)', '([^']+)'\)", decoded_output_ori)))

        if len(classification_sentiment_list) == 0:
            end_index = decoded_output_ori.find('assistant')
            start_index = decoded_output_ori.rfind(':')
        
            if end_index > 0:
                decoded_output = decoded_output_ori[:end_index]
            elif start_index > 0:
                decoded_output = decoded_output_ori[start_index:]
            else:
                decoded_output = decoded_output_ori

            classification_sentiment_list = list(set(re.findall(r"\['([^']+)', '([^']+)'\]", decoded_output)))

        return classification_sentiment_list
    
    
    # 提取类别列表
    def extract_categories(self, classification_output, classification_label):
        start = classification_output.find("[")
        end = classification_output.find("]") + 1
        extracted_list = ast.literal_eval(classification_output[start: end])
        
        for category in extracted_list:
            if category not in classification_label:
                print(f"There is no category classified!\n")
                extracted_list = []
        
        return extracted_list