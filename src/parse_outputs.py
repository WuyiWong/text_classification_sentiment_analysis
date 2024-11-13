from common.script_base import ScriptBase


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
    
    # 提取类别列表
    def extract_categories(self, classification_output, classification_label):
        lines = classification_output.strip().split('\n')
        
        index = 0 # 初始化index 用来作为正确输出的结尾index
        for i, element in enumerate(lines):
            if '-' not in element:
                index = i
                break
        lines = lines[: index]
        
        categories_list = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                category = line[1:].strip()
            else:
                category = line.strip()
            if category in classification_label and category not in categories_list:
                categories_list.append(category)
        
        return categories_list