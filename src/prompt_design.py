import os
import sys
from common.script_base import ScriptBase
import textwrap

class PromptTuning(ScriptBase):

    # 定义 Prompt 模板
    def create_zero_shot_prompt(self, review, categories, examples=None):
        """
        Generates a zero-shot prompt for classification and sentiment analysis without including examples in the main body.
        The examples are passed separately and used only when needed to inform the model.
        
        Args:
        - review: The product review to classify.
        - categories: The predefined categories to classify the review into.
        - examples: A string containing all the examples, passed once to avoid repeated input.

        Returns:
        - A prompt that only includes instructions and the review, with no repeated examples.
        """
        prompt = (
            f"Classify the following product review into one or more of the following categories: {', '.join(categories)}. And analyze the sentiment (Positive, Negative, or Neutral) for each category that applies.\n"
            "You do not need to repeat any part of the input. Just output the categories and their corresponding sentiment in the format.\n- Category: Sentiment"
        )
        if examples:
            prompt += f"\n\nHere are some examples:\n{examples}"
        
        prompt += f"\nNow, classify the following review and provide the categories and sentiments only:"
        if review:
            prompt += f"\nReview: '{review}'\nOutput:"
        
        return prompt
    
    def examples_prompt_long(self):
        # 定义例子 prompt 模版
        examples = textwrap.dedent(f"""
        Example 1: 
        Review: "The fabric of this clothing is very comfortable, but the price is a bit high."
        Output:
        - Comfort: Positive
        - Price and Value: Negative

        Example 2:
        Review: "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric."
        Output:
        - Design and Appearance: Negative
        - Comfort: Negative
        - Size and Fit: Negative
        - Overall Satisfaction: Negative

        Example 3:
        Review: "I had high hopes for this but unfortunately ended up having to return. It was very big and unflattering, kind of like a tent. I would say if you are between a L/XL definitely size down. The shipping was fast, but overall just did not like the dress."
        Output:
        - Size and Fit: Negative
        - Design and Appearance: Negative
        - Shipping and Packaging: Positive
        - Overall Satisfaction: Negative
                                   
        Example 4:
        Review: "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!"
        Output:
        - Size and Fit: Positive
        - Design and Appearance: Positive
        - Usage Scenarios and Applicability: Positive
        
        Example 5:
        Review: "Absolutely fell in love with this dress the first time I wore it.  If ur going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress.  It did fit true to size and wasn't too short."
        Output:
        - Design and Appearance: Positive
        - Size and Fit: Positive
        - Product Quality: Negative
        - Washing and Maintenance: Negative                      

        Example 6:
        Review: "I got this because I thought it would be breast feeding friendly.  It’s is amazing.  Super easy to breast feed in, looks awesome with a denim jacket, and makes me look like I wasn’t even pregnant.  I have it in four colors.  Highly recommend ??"
        Output:
        - Usage Scenarios and Applicability: Positive
        - Design and Appearance: Positive
        - Overall Satisfaction: Positive

        Example 7:
        Review: "It’s a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it’s a good buy."
        Output:
        Usage Scenarios and Applicability: Positive
        - Size and Fit: Positive
        - Comfort: Positive
        - Product Quality: Neutral
        - Overall Satisfaction: Positive
        
        Example 8:
        Review: "The fabric of this product is good and not cheap! The wrinkles were expected because of it being packaged but that can be easily fixed. The color is exactly as pictured and the fit of it is great. I ordered a medium and I'm comfortable in it."
        Output:
        - Shipping and Packaging: Neutral
        - Product Quality: Positive
        - Design and Appearance: Positive
        - Size and Fit: Positive
        - Comfort: Positive

        Example 9:
        Review: "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful."                           
        Output:
        - Design and Appearance: Positive
        - Product Quality: Positive
        - Color and Appearance: Positive
        - Size and Fit: Positive                           

        Example 10:
        Review: "Dress was not the same pattern. It looked cheap. No tags whatsoever to know how to care for it. Ordered normal size and was small looking because of elastic in waist. Wasn't at all flowing like the style. Returning for sure."
        Output:
        - Product Quality: Negative
        - Size and Fit: Negative
        - Washing and Maintenance: Negative
        - Overall Satisfaction: Negative
        - Design and Appearance: Negative

        Example 11:
        Review: "Washed it for the first time and there are strings and hems coming undone all over. Went to exchange or return it and apparently my window closed , such a bummer, it really us a cute dress!"
        Output:
        - Product Quality: Negative
        - Washing and Maintenance: Negative
        - Brand and Customer Service: Negative
        - Design and Appearance: Positive                           

        Example 12:                           
        Review: "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red.I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I  buy the large?)."                           
        Output:
        - Usage Scenarios and Applicability: Positive
        - Design and Appearance: Positive
        - Product Quality: Positive
        - Size and Fit: Neutral
        - Washing and Maintenance: Positive                           

        Example 13:
        Review: "This dress was sized at a 12 to 14, which should have been fine . Was too small, came all bunched up in a bag and wrinkled, the fabric is not very breathable and I did not care for the dress at all. Looks lovely in the picture, but I actually hated it."
        Output:
        - Size and Fit: Negative
        - Shipping and Packaging: Negative
        - Product Quality: Negative
        - Design and Appearance: Negative                           

        Example 14:
        Review: "Very clean product. The fabric, craftsmanship, and underneath slip are all thick and very well made. No cheap materials, no messy stitching, no misalignments. Looks and feels like a dress you could easily pay more money for, at a small chic boutique by the beach..."
        Output:
        - Product Quality: Positive
        - Design and Appearance: Positive
        - Price and Value: Positive
        - Overall Satisfaction: Positive
                                   
        Example 15: 
        Review: "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered."
        Output:
        - Size and Fit: Positive                           
        - Color and Appearance: Neutral                           
        - Shipping and Packaging: Positive
        - Brand and Customer Service: Positive

        Example 16:                           
        Review: "This is a pretty, flowy dress. It's lightweight enough for summer, but it's not see thru. I love Nemidor dresses, and I plan on buying more of them when they go on sale. They feel good on, and they make you feel good when your wear them."                           
        Output:
        - Design and Appearance: Positive
        - Product Quality: Positive
        - Comfort: Positive
        - Brand and Customer Service: Positive
        - Overall Satisfaction: Positive                                                       

        """)

        return examples

    def examples_prompt(self):
        # 定义例子 prompt 模版
        examples = textwrap.dedent(f"""
        Example 1:
        Review: "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric."
        Output:
        - Design and Appearance: Negative
        - Comfort: Negative
        - Size and Fit: Negative
        - Overall Satisfaction: Negative

        Example 2:
        Review: "I had high hopes for this but unfortunately ended up having to return. It was very big and unflattering, kind of like a tent. I would say if you are between a L/XL definitely size down. The shipping was fast, but overall just did not like the dress."
        Output:
        - Size and Fit: Negative
        - Design and Appearance: Negative
        - Shipping and Packaging: Positive
        - Overall Satisfaction: Negative
                                   
        Example 3:
        Review: "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!"
        Output:
        - Size and Fit: Positive
        - Design and Appearance: Positive
        - Usage Scenarios and Applicability: Positive
        
        Example 4:
        Review: "Absolutely fell in love with this dress the first time I wore it.  If ur going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress.  It did fit true to size and wasn't too short."
        Output:
        - Design and Appearance: Positive
        - Size and Fit: Positive
        - Product Quality: Negative
        - Washing and Maintenance: Negative                      

        Example 5:
        Review: "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful."                           
        Output:
        - Design and Appearance: Positive
        - Product Quality: Positive
        - Color and Appearance: Positive
        - Size and Fit: Positive                           

        Example 6:
        Review: "Washed it for the first time and there are strings and hems coming undone all over. Went to exchange or return it and apparently my window closed , such a bummer, it really us a cute dress!"
        Output:
        - Product Quality: Negative
        - Washing and Maintenance: Negative
        - Brand and Customer Service: Negative
        - Design and Appearance: Positive                           

        Example 7:
        Review: "This dress was sized at a 12 to 14, which should have been fine . Was too small, came all bunched up in a bag and wrinkled, the fabric is not very breathable and I did not care for the dress at all. Looks lovely in the picture, but I actually hated it."
        Output:
        - Size and Fit: Negative
        - Shipping and Packaging: Negative
        - Product Quality: Negative
        - Design and Appearance: Negative                           

        Example 8:
        Review: "Very clean product. The fabric, craftsmanship, and underneath slip are all thick and very well made. No cheap materials, no messy stitching, no misalignments. Looks and feels like a dress you could easily pay more money for, at a small chic boutique by the beach..."
        Output:
        - Product Quality: Positive
        - Design and Appearance: Positive
        - Price and Value: Positive
        """)

        return examples



    def create_classification_prompt(self, review, categories, examples=None):
        prompt = (
            f"Classify the following product review into one or more of the following categories: {', '.join(categories)}.\n"
            "You do not need to repeat any part of the input. Just output the categories that apply in the format\n"
            "- Category"
        )

        if examples:
            prompt += f"\n\nHere are some examples:\n{examples}"
        
        prompt += f"\nNow, classify the following review and provide the categories only:\nReview: '{review}'\nOutput:"

        return prompt

    def classification_examples_long(self):
        examples = textwrap.dedent("""
        Example 1: 
        Review: "The fabric of this clothing is very comfortable, but the price is a bit high."
        Output:
        - Comfort
        - Price and Value

        Example 2:
        Review: "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric."
        Output:
        - Design and Appearance
        - Comfort
        - Size and Fit
        - Overall Satisfaction

        Example 3:
        Review: "I had high hopes for this but unfortunately ended up having to return. It was very big and unflattering, kind of like a tent. I would say if you are between a L/XL definitely size down. The shipping was fast, but overall just did not like the dress."
        Output:
        - Size and Fit
        - Design and Appearance
        - Shipping and Packaging
        - Overall Satisfaction
                                   
        Example 4:
        Review: "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!"
        Output:
        - Size and Fit
        - Design and Appearance
        - Usage Scenarios and Applicability
        
        Example 5:
        Review: "Absolutely fell in love with this dress the first time I wore it.  If ur going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress.  It did fit true to size and wasn't too short."
        Output:
        - Design and Appearance
        - Size and Fit
        - Product Quality
        - Washing and Maintenance                      

        Example 6:
        Review: "I got this because I thought it would be breast feeding friendly.  It’s is amazing.  Super easy to breast feed in, looks awesome with a denim jacket, and makes me look like I wasn’t even pregnant.  I have it in four colors.  Highly recommend ??"
        Output:
        - Usage Scenarios and Applicability
        - Design and Appearance
        - Overall Satisfaction

        Example 7:
        Review: "It’s a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it’s a good buy."
        Output:
        Usage Scenarios and Applicability
        - Size and Fit
        - Comfort
        - Product Quality
        - Overall Satisfaction
        
        Example 8:
        Review: "The fabric of this product is good and not cheap! The wrinkles were expected because of it being packaged but that can be easily fixed. The color is exactly as pictured and the fit of it is great. I ordered a medium and I'm comfortable in it."
        Output:
        - Shipping and Packaging
        - Product Quality
        - Design and Appearance
        - Size and Fit
        - Comfort

        Example 9:
        Review: "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful."                           
        Output:
        - Design and Appearance
        - Product Quality
        - Color and Appearance
        - Size and Fit                           

        Example 10:
        Review: "Dress was not the same pattern. It looked cheap. No tags whatsoever to know how to care for it. Ordered normal size and was small looking because of elastic in waist. Wasn't at all flowing like the style. Returning for sure."
        Output:
        - Product Quality
        - Size and Fit
        - Washing and Maintenance
        - Overall Satisfaction
        - Design and Appearance

        Example 11:
        Review: "Washed it for the first time and there are strings and hems coming undone all over. Went to exchange or return it and apparently my window closed , such a bummer, it really us a cute dress!"
        Output:
        - Product Quality
        - Washing and Maintenance
        - Brand and Customer Service
        - Design and Appearance                           

        Example 12:                           
        Review: "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red.I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I  buy the large?)."                           
        Output:
        - Usage Scenarios and Applicability
        - Design and Appearance
        - Product Quality
        - Size and Fit
        - Washing and Maintenance                           

        Example 13:
        Review: "This dress was sized at a 12 to 14, which should have been fine . Was too small, came all bunched up in a bag and wrinkled, the fabric is not very breathable and I did not care for the dress at all. Looks lovely in the picture, but I actually hated it."
        Output:
        - Size and Fit
        - Shipping and Packaging
        - Product Quality
        - Design and Appearance                           

        Example 14:
        Review: "Very clean product. The fabric, craftsmanship, and underneath slip are all thick and very well made. No cheap materials, no messy stitching, no misalignments. Looks and feels like a dress you could easily pay more money for, at a small chic boutique by the beach..."
        Output:
        - Product Quality
        - Design and Appearance
        - Price and Value
        - Overall Satisfaction
                                   
        Example 15: 
        Review: "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered."
        Output:
        - Size and Fit                           
        - Color and Appearance                           
        - Shipping and Packaging
        - Brand and Customer Service

        Example 16:                           
        Review: "This is a pretty, flowy dress. It's lightweight enough for summer, but it's not see thru. I love Nemidor dresses, and I plan on buying more of them when they go on sale. They feel good on, and they make you feel good when your wear them."                           
        Output:
        - Design and Appearance
        - Product Quality
        - Comfort
        - Brand and Customer Service
        - Overall Satisfaction  
        """)
        return examples
    
    def classification_examples(self):
        examples = textwrap.dedent("""
        Example 1:
        Review: "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric."
        Output:
        - Design and Appearance
        - Comfort
        - Size and Fit
        - Overall Satisfaction

        Example 2:
        Review: "I had high hopes for this but unfortunately ended up having to return. It was very big and unflattering, kind of like a tent. I would say if you are between a L/XL definitely size down. The shipping was fast, but overall just did not like the dress."
        Output:
        - Size and Fit
        - Design and Appearance
        - Shipping and Packaging
        - Overall Satisfaction
                                   
        Example 3:
        Review: "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!"
        Output:
        - Size and Fit
        - Design and Appearance
        - Usage Scenarios and Applicability
        
        Example 4:
        Review: "Absolutely fell in love with this dress the first time I wore it.  If ur going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress.  It did fit true to size and wasn't too short."
        Output:
        - Design and Appearance
        - Size and Fit
        - Product Quality
        - Washing and Maintenance                      

        Example 5:
        Review: "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful."                           
        Output:
        - Design and Appearance
        - Product Quality
        - Color and Appearance
        - Size and Fit                           

        Example 6:
        Review: "Washed it for the first time and there are strings and hems coming undone all over. Went to exchange or return it and apparently my window closed , such a bummer, it really us a cute dress!"
        Output:
        - Product Quality
        - Washing and Maintenance
        - Brand and Customer Service
        - Design and Appearance                           

        Example 7:
        Review: "This dress was sized at a 12 to 14, which should have been fine . Was too small, came all bunched up in a bag and wrinkled, the fabric is not very breathable and I did not care for the dress at all. Looks lovely in the picture, but I actually hated it."
        Output:
        - Size and Fit
        - Shipping and Packaging
        - Product Quality
        - Design and Appearance                           

        Example 8:
        Review: "Very clean product. The fabric, craftsmanship, and underneath slip are all thick and very well made. No cheap materials, no messy stitching, no misalignments. Looks and feels like a dress you could easily pay more money for, at a small chic boutique by the beach..."
        Output:
        - Product Quality
        - Design and Appearance
        - Price and Value
        - Overall Satisfaction
        """)
        return examples


    def create_sentiment_prompt(self, review, predicted_categories, examples=None):
        """
        生成情感分析的提示（prompt），指导模型对指定类别进行情感分析。

        Args:
            review (str): 需要分析的产品评论。
            predicted_categories (list): 预测的类别列表。
            examples (str, optional): 示例字符串，用于指导模型。

        Returns:
            str: 生成的提示字符串。
        """
        prompt = (
            f"Analyze the sentiment (Positive, Negative, or Neutral) of the following product review for each of the following categories: {', '.join(predicted_categories)}.\n"
            "You do not need to repeat any part of the input. Just output the categories and their corresponding sentiments in the format:\n"
            "- Category: Sentiment"
        )
        
        if examples:
            prompt += f"\n\nHere are some examples:\n{examples}"
        
        prompt += f"\n\nNow, analyze the sentiment for the following review and categories:\nReview: '{review}'\nOutput:"
        
        return prompt
    
    def sentiment_examples(self):
        
        examples = textwrap.dedent("""
        Example 1: 
        Review: "The fabric of this clothing is very comfortable, but the price is a bit high."
        Output:
        - Comfort: Positive
        - Price and Value: Negative

        Example 2:
        Review: "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric."
        Output:
        - Design and Appearance: Negative
        - Comfort: Negative
        - Size and Fit: Negative
        - Overall Satisfaction: Negative

        Example 3:
        Review: "I had high hopes for this but unfortunately ended up having to return. It was very big and unflattering, kind of like a tent. I would say if you are between a L/XL definitely size down. The shipping was fast, but overall just did not like the dress."
        Output:
        - Size and Fit: Negative
        - Design and Appearance: Negative
        - Shipping and Packaging: Positive
        - Overall Satisfaction: Negative
                                   
        Example 4:
        Review: "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!"
        Output:
        - Size and Fit: Positive
        - Design and Appearance: Positive
        - Usage Scenarios and Applicability: Positive
        
        Example 5:
        Review: "Absolutely fell in love with this dress the first time I wore it.  If ur going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress.  It did fit true to size and wasn't too short."
        Output:
        - Design and Appearance: Positive
        - Size and Fit: Positive
        - Product Quality: Negative
        - Washing and Maintenance: Negative                      

        Example 6:
        Review: "I got this because I thought it would be breast feeding friendly.  It’s is amazing.  Super easy to breast feed in, looks awesome with a denim jacket, and makes me look like I wasn’t even pregnant.  I have it in four colors.  Highly recommend ??"
        Output:
        - Usage Scenarios and Applicability: Positive
        - Design and Appearance: Positive
        - Overall Satisfaction: Positive

        Example 7:
        Review: "It’s a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it’s a good buy."
        Output:
        Usage Scenarios and Applicability: Positive
        - Size and Fit: Positive
        - Comfort: Positive
        - Product Quality: Neutral
        - Overall Satisfaction: Positive
        
        Example 8:
        Review: "The fabric of this product is good and not cheap! The wrinkles were expected because of it being packaged but that can be easily fixed. The color is exactly as pictured and the fit of it is great. I ordered a medium and I'm comfortable in it."
        Output:
        - Shipping and Packaging: Neutral
        - Product Quality: Positive
        - Design and Appearance: Positive
        - Size and Fit: Positive
        - Comfort: Positive

        Example 9:
        Review: "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful."                           
        Output:
        - Design and Appearance: Positive
        - Product Quality: Positive
        - Color and Appearance: Positive
        - Size and Fit: Positive                           

        Example 10:
        Review: "Dress was not the same pattern. It looked cheap. No tags whatsoever to know how to care for it. Ordered normal size and was small looking because of elastic in waist. Wasn't at all flowing like the style. Returning for sure."
        Output:
        - Product Quality: Negative
        - Size and Fit: Negative
        - Washing and Maintenance: Negative
        - Overall Satisfaction: Negative
        - Design and Appearance: Negative

        Example 11:
        Review: "Washed it for the first time and there are strings and hems coming undone all over. Went to exchange or return it and apparently my window closed , such a bummer, it really us a cute dress!"
        Output:
        - Product Quality: Negative
        - Washing and Maintenance: Negative
        - Brand and Customer Service: Negative
        - Design and Appearance: Positive                           

        Example 12:                           
        Review: "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red.I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I  buy the large?)."                           
        Output:
        - Usage Scenarios and Applicability: Positive
        - Design and Appearance: Positive
        - Product Quality: Positive
        - Size and Fit: Neutral
        - Washing and Maintenance: Positive                           

        Example 13:
        Review: "This dress was sized at a 12 to 14, which should have been fine . Was too small, came all bunched up in a bag and wrinkled, the fabric is not very breathable and I did not care for the dress at all. Looks lovely in the picture, but I actually hated it."
        Output:
        - Size and Fit: Negative
        - Shipping and Packaging: Negative
        - Product Quality: Negative
        - Design and Appearance: Negative                           

        Example 14:
        Review: "Very clean product. The fabric, craftsmanship, and underneath slip are all thick and very well made. No cheap materials, no messy stitching, no misalignments. Looks and feels like a dress you could easily pay more money for, at a small chic boutique by the beach..."
        Output:
        - Product Quality: Positive
        - Design and Appearance: Positive
        - Price and Value: Positive
        - Overall Satisfaction: Positive
                                   
        Example 15: 
        Review: "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered."
        Output:
        - Size and Fit: Positive                           
        - Color and Appearance: Neutral                           
        - Shipping and Packaging: Positive
        - Brand and Customer Service: Positive

        Example 16:                           
        Review: "This is a pretty, flowy dress. It's lightweight enough for summer, but it's not see thru. I love Nemidor dresses, and I plan on buying more of them when they go on sale. They feel good on, and they make you feel good when your wear them."                           
        Output:
        - Design and Appearance: Positive
        - Product Quality: Positive
        - Comfort: Positive
        - Brand and Customer Service: Positive
        - Overall Satisfaction: Positive 
        """)
        return examples
    
    # 提取类别列表
    def extract_categories(self, classification_output):
        lines = classification_output.strip().split('\n')
        categories = []
        for line in lines:
            line = line.strip('- ').strip()
            if line:
                categories.append(line)
        return categories