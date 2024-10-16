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
            f"Classify the following product review into one or more of the following categories: {categories}, and analyze the sentiment (Positive, Negative, or Neutral) for each category that applies.\n"
            "You do not need to repeat any part of the input. Just output the categories and their corresponding sentiment in the format.\n- Category: Sentiment"
        )
        if examples:
            prompt += f"\n\nHere are some examples:\n{examples}"
        
        prompt += f"\nNow, classify the following review and provide the categories and sentiments only:"
        if review:
            prompt += f"\nReview: '{review}'\nOutput:"
        
        return prompt
    
    def examples_prompt(self):
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
        Review: "Nice cool dress for summer, but sizing is way off."
        Output:
        - Usage Scenarios and Applicability: Positive
        - Size and Fit: Negative
        - Design and Appearance: Positive

        Example 4:
        Review: "The fabric of this product is good and not cheap! The wrinkles were expected because of it being packaged but that can be easily fixed. The color is exactly as pictured and the fit of it is great. I ordered a medium and I'm comfortable in it."
        Output:
        - Shipping and Packaging: Neutral
        - Product Quality: Positive
        - Design and Appearance: Positive
        - Size and Fit: Positive
        - Comfort: Positive

        Example 5:
        Review: "Dress was not the same pattern. It looked cheap. No tags whatsoever to know how to care for it. Ordered normal size and was small looking because of elastic in waist. Wasn't at all flowing like the style. Returning for sure."
        Output:
        - Product Quality: Negative
        - Size and Fit: Negative
        - Washing and Maintenance: Negative
        - Overall Satisfaction: Negative
        - Design and Appearance: Negative

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
        Review: "This is SO CUTE! Not to short for a mature woman, the only downside is the shorts are attached to the dress. So you have to take down the dress when nature calls. But boy oh boy is it cute! I need all the colors!"
        Output:
        - Design and Appearance: Positive
        - Usage Scenarios and Applicability: Neutral
        - Overall Satisfaction: Positive
        """)

        return examples

    def create_classification_prompt(self, review, categories, examples=None):
        prompt = (
            f"Classify the following product review into one or more of the following categories: {', '.join(categories)}.\n"
            "You do not need to repeat any part of the input. Just output the categories that apply in the format\n"
            "- Category."
        )

        if examples:
            prompt += f"\n\nHere are some examples:\n{examples}"
        
        prompt += f"\n\nNow, classify the following review and provide the categories only:\nReview: '{review}'\nOutput:"

        return prompt

    def classification_examples(self):
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
        Review: "Nice cool dress for summer, but sizing is way off."
        Output:
        - Usage Scenarios and Applicability
        - Size and Fit
        - Design and Appearance

        Example 4:
        Review: "The fabric of this product is good and not cheap! The wrinkles were expected because of it being packaged but that can be easily fixed. The color is exactly as pictured and the fit of it is great. I ordered a medium and I'm comfortable in it."
        Output:
        - Shipping and Packaging
        - Product Quality
        - Design and Appearance
        - Size and Fit
        - Comfort

        Example 5:
        Review: "Dress was not the same pattern. It looked cheap. No tags whatsoever to know how to care for it. Ordered normal size and was small looking because of elastic in waist. Wasn't at all flowing like the style. Returning for sure."
        Output:
        - Product Quality
        - Size and Fit
        - Washing and Maintenance
        - Overall Satisfaction
        - Design and Appearance

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
        Review: "This is SO CUTE! Not to short for a mature woman, the only downside is the shorts are attached to the dress. So you have to take down the dress when nature calls. But boy oh boy is it cute! I need all the colors!"
        Output:
        - Design and Appearance
        - Usage Scenarios and Applicability
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
        Categories: Comfort, Price and Value
        Output:
        - Comfort: Positive
        - Price and Value: Negative
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