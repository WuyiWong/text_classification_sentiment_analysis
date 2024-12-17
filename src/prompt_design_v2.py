import os
import sys
from common.script_base import ScriptBase
import textwrap
import pandas as pd 
import json
class PromptTuning(ScriptBase):

    # 定义 Prompt 模板
    def create_classification_prompt_v7(self, review, categories, classification_examples=None):
        prompt = (
            "Classify the following product review into one or more of the following categories: \n- Price and Value\n- Shipping and Packaging\n- Design and Appearance\n- Product Quality\n- Fabric\n- Size and Fit\n- Washing and Maintenance\n- Comfort\n- Usage Scenarios and Applicability"
            "\n\n### Instructions:"
            "\nFocus on identifying relevant categories based on specific keywords or review content. Prioritize the following categories with these guidelines:"
            "\n\n1. **Size and Fit**: Assign this category if the review mentions words like 'size', 'fit', 'true to size', 'tight', 'loose', or similar terms related to how the product fits."
            "\n2. **Product Quality**: Assign this category if the review comments on the product's overall quality, such as durability, craftsmanship, or reliability. Indicators include terms like 'well-made', 'poor build', 'high-quality', or 'cheaply-made'."
            "\n3. **Fabric**: Assign this category if the review discusses the product's material or texture. Look for terms like 'fabric', 'material', 'soft', 'itchy', or descriptions of tactile experiences."
            "\n\n### Important Notes:"
            "\n- Avoid assigning unrelated categories if the review lacks clear indicators."
            "\n- Prioritize the most relevant categories if there is overlap between them."
            "\n- Use the examples below for reference."
        )

        if classification_examples:
            prompt += "\n\n### Examples:"
            for idx, example in enumerate(classification_examples, start=1):
                prompt += f"\nReview: \"{example['review']}\"\nOutput:"
                for category in example['output']:
                    prompt += f"\n- {category}"
        
        prompt += f"\n\nNow, analyze the following review:\nReview: '{review}'\nOutput:"
        return prompt

    def create_classification_prompt_v8(self, review, categories, classification_examples=None):
        prompt = (
            f"Classify the following product review into one or more of the following categories: {', '.join(categories)}."
            "\n\n### Instructions:"
            "\nFocus on identifying relevant categories based on specific keywords or review content. Prioritize the following categories with these guidelines:"
            "\n\n1. **Size and Fit**: Assign this category if the review mentions words like 'size', 'fit', 'true to size', 'tight', 'loose', or similar terms related to how the product fits."
            "\n2. **Product Quality**: Assign this category if the review comments on the product's overall quality or build, durability, craftsmanship, or reliability. Indicators include terms like 'cheap', 'well-made', 'poor build', 'poor quality', 'high-quality', 'flimsy', or 'cheaply-made'. If the review mentions material-specific issues (e.g., 'cheap fabric'), assign both Product Quality and Fabric."
            "\n3. **Fabric**: Assign this category if the review explicitly discusses the product's material, feel, or texture. Look for terms like 'fabric', 'thin', 'material', 'stretchy', 'breathable', 'soft', 'itchy', or descriptions of tactile experiences. If the material is criticized as part of a broader quality issue, label both Fabric and Product Quality."
            "\n4. **Design and Appearance**: Assign this category if the review discusses the product's visual aspects, such as patterns, prints, colors, or overall style. Look for words or phrases like 'different than shown,' 'color mismatch,' 'not as described visually,' 'design,' 'print,' 'pattern,' 'color,' 'cute,' 'stylish,' or similar."
            "\n5. **Price and Value**: Assign this category only if the review directly/explicitly discusses cost, price, affordability, or perceived value for money. Do not assign this category for general dissatisfaction with the product unless price or value is mentioned explicitly (e.g., 'for the price,' 'affordable,' 'expensive')."
            "\n\n### Important Notes:"
            "\n- Avoid assigning unrelated categories if there are no explicit indicators in the review."
            "\n- Use the examples below for reference."
        )

        if classification_examples:
            prompt += "\n\n### Examples:"
            for idx, example in enumerate(classification_examples, start=1):
                prompt += f"\n\nReview: \"{example['review']}\"\nOutput:"
                for category in example['output']:
                    prompt += f"\n- {category}"
        
        prompt += f"\n\nNow, analyze the following review:\nReview: '{review}'\nOutput:"
        return prompt


    def create_classification_prompt_v9(self, review, categories, classification_examples=None):
        prompt = (
            f"Classify the following product review into one or more of the following categories: {', '.join(categories)}."
            "\n\n### Instructions:"
            "\nFocus on identifying relevant categories based on specific keywords or review content. Prioritize the following categories with these guidelines:"
            "\n\n1. **Size and Fit**: Assign this category only if the review explicitly discusses size, fit, or related terms such as 'true to size,' 'tight,' 'loose,' 'perfect fit,' or similar phrases. Avoid assigning this category for general positive terms like 'perfect' unless they explicitly describe fit."
            "\n2. **Product Quality**: Assign this category if the review comments on the product's overall build, durability, craftsmanship, or reliability. This includes issues like stitching problems, misaligned seams, or other construction flaws. Indicators include terms like 'cheap', 'well-made', 'poor build', 'poor quality', 'high-quality', 'flimsy', or 'cheaply-made'. If material-related issues (e.g., 'thin fabric') are part of these flaws, assign both Product Quality and Fabric."
            "\n3. **Fabric**: Assign this category if the review explicitly discusses the product's material, feel, or texture. Look for terms like 'fabric,' 'thin,' 'material,' 'stretchy,' 'breathable,' 'soft,' 'itchy,' or 'cheap fabric.' Critiques of material (e.g., 'thin material' or 'cheap fabric') should always include Fabric. If these critiques are part of broader quality issues (e.g., seams unraveling or poor stitching), assign both Fabric and Product Quality."
            "\n4. **Design and Appearance**: Assign this category if the review discusses the product's visual aspects, such as patterns, prints, colors, or overall style. Look for words or phrases like 'different than shown,' 'color mismatch,' 'not as described visually,' 'design,' 'print,' 'pattern,' 'color,' 'cute,' 'stylish,' or similar."
            "\n5. **Price and Value**: Assign this category only if the review explicitly discusses cost, price, affordability, value-for-money, or perceived value for money (e.g., 'worth the price,' 'expensive,' 'great deal'). General critiques like 'cheap' should be assigned to Product Quality unless directly tied to price (e.g., 'cheap for the price'). Do not assign this category for general dissatisfaction negative experiences unless price or value is mentioned explicitly."
            "\n\n### Important Notes:"
            "\n- Avoid assigning unrelated categories if there are no explicit indicators in the review."
            "\n- Use the examples below for reference."
        )

        if classification_examples:
            prompt += "\n\n### Examples:"
            for idx, example in enumerate(classification_examples, start=1):
                prompt += f"\n\nReview: \"{example['review']}\"\nOutput:"
                for category in example['output']:
                    prompt += f"\n- {category}"
        
        prompt += f"\n\nNow, analyze the following review:\nReview: '{review}'\nOutput:"
        return prompt

    def create_classification_prompt_v10(self, review, categories, classification_examples=None):
        # Define the system message for task context
        
        system_message_dict = {
                "role": "system",
                "content": {
                    "Persona": f"You are a multi-label text classifier. You task is to classify product reviews into one or more of the following categories: {', '.join(categories)}.",
                    "Instructions": [
                        "Focus on identifying relevant categories based on specific keywords or review content.", 
                        "Prioritize the following categories with these guidelines:",
                        "Size and Fit: Assign this category if the review mentions words like 'size', 'fit', 'true to size', 'tight', 'loose', or similar terms related to how the product fits.",
                        "Product Quality: Assign this category if the review comments on the product's overall quality or build, durability, craftsmanship, or reliability. Indicators include terms like 'cheap', 'well-made', 'poor build', 'poor quality', 'high-quality', 'flimsy', or 'cheaply-made'. If the review mentions material-specific issues (e.g., 'cheap fabric'), assign both Product Quality and Fabric.",
                        "Fabric: Assign this category if the review explicitly discusses the product's material, feel, or texture. Look for terms like 'fabric', 'thin', 'material', 'stretchy', 'breathable', 'soft', 'itchy', or descriptions of tactile experiences. If the material is criticized as part of a broader quality issue, label both Fabric and Product Quality.",
                        "Design and Appearance: Assign this category if the review discusses the product's visual aspects, such as patterns, prints, colors, or overall style. Look for words or phrases like 'different than shown,' 'color mismatch,' 'not as described visually,' 'design,' 'print,' 'pattern,' 'color,' 'cute,' 'stylish,' or similar.",
                    ],
                    "ImportantNotes": [
                        "Avoid assigning unrelated categories if there are no explicit indicators in the review.",
                        "Use the examples below for reference."
                    ],
                    "OutputFormat": "Return the classification strictly in the format: [CATEGORY, CATEGORY, ...]. Do not provide explanations or additional text. If no categories apply, return: ['No applicable categories'].",
                    "Examples": []
                }
            }
        user_message_dict = {
                "role": "user",
                "content": f"Classify the following review: '{review}'\nOutput:"
            }
        
        # Add examples to the system message if provided
        if classification_examples:
            for idx, example in enumerate(classification_examples, start=1):
                example_entry = {
                    "Review": example['review'],
                    "Output": example['output']
                }
                system_message_dict["content"]['Examples'].append(example_entry)
        
        messages = [system_message_dict, user_message_dict]
        
        return messages


    
    def create_classification_prompt_v11(self, review, categories, classification_examples=None):
        """
        创建多标签分类任务的消息格式。

        Args:
            review (str): 待分类的评论文本。
            categories (list): 分类任务中的类别列表。
            classification_examples (list): 示例数据列表（可选），用于提供模型参考。

        Returns:
            list: 包含 `system` 和 `user` 消息的字典列表。
        """
        # Define the system message for task context
        system_message_dict = {
                "role": "system",
                "content": {
                    "Persona": f"You are a multi-label text classifier. You task is to classify product reviews into one or more of the following categories: {', '.join(categories)}.",
                    "Instructions": [
                        "Focus on identifying relevant categories based on specific keywords or review content.", 
                        "Prioritize the following categories with these guidelines:",
                        "Size and Fit: Assign this category only if the review explicitly discusses size, fit, or related terms such as 'true to size,' 'tight,' 'loose,' 'perfect fit,' or similar phrases. Avoid assigning this category for general positive terms like 'perfect' unless they explicitly describe fit.",
                        "Product Quality: Assign this category if the review comments on the product's overall build, durability, craftsmanship, or reliability. This includes issues like stitching problems, misaligned seams, or other construction flaws. Indicators include terms like 'cheap', 'well-made', 'poor build', 'poor quality', 'high-quality', 'flimsy', or 'cheaply-made'. If material-related issues (e.g., 'thin fabric') are part of these flaws, assign both Product Quality and Fabric.",
                        "Fabric: Assign this category if the review explicitly discusses the product's material, feel, or texture. Look for terms like 'fabric,' 'thin,' 'material,' 'stretchy,' 'breathable,' 'soft,' 'itchy,' or 'cheap fabric.' Critiques of material (e.g., 'thin material' or 'cheap fabric') should always include Fabric. If these critiques are part of broader quality issues (e.g., seams unraveling or poor stitching), assign both Fabric and Product Quality.",
                        "Design and Appearance: Assign this category if the review discusses the product's visual aspects, such as patterns, prints, colors, or overall style. Look for words or phrases like 'different than shown,' 'color mismatch,' 'not as described visually,' 'design,' 'print,' 'pattern,' 'color,' 'cute,' 'stylish,' or similar.",
                    ],
                    "ImportantNotes": [
                        "Avoid assigning unrelated categories if there are no explicit indicators in the review.",
                        "Use the examples below for reference."
                    ],
                    "OutputFormat": "Return the classification strictly in the format: [CATEGORY, CATEGORY, ...]. Do not provide explanations or additional text. If no categories apply, return: ['No applicable categories'].",
                    "Examples": []
                }
            }
        user_message_dict = {
                "role": "user",
                "content": f"Classify the following review: '{review}'\nOutput:"
            }
        
        # Add examples to the system message if provided
        if classification_examples:
            for idx, example in enumerate(classification_examples, start=1):
                example_entry = {
                    "Review": example['review'],
                    "Output": example['output']
                }
                system_message_dict["content"]['Examples'].append(example_entry)
        
        messages = [system_message_dict, user_message_dict]

        return messages


    
    def classification_examples_medium(self, categories):
        # JSON format
        classification_examples = [
            {
                "review": "The fabric pattern was completely different from the pictures. I expected floral but received stripes. The fit was fine, but the pattern was disappointing.",
                "output": ["Fabric", "Design and Appearance"]
            },
            {
                "review": "The color and pattern were not as advertised. I expected vibrant colors, but they were dull and unappealing. Tight fit on the bust as well.",
                "output": ["Design and Appearance", "Size and Fit"]
            },
            {
                "review": "The dress looks beautiful, but the floral pattern was not what I expected. It looked more faded than in the pictures.",
                "output": ["Design and Appearance"]
            },
            {
                "review": "This dress is made of breathable cotton, which is perfect for summer.",
                "output": ["Fabric", "Usage Scenarios and Applicability"]
            },
            {
                "review": "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric.",
                "output": ["Design and Appearance", "Comfort", "Size and Fit"]
            },
            {
                "review": "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!",
                "output": ["Size and Fit", "Design and Appearance", "Usage Scenarios and Applicability"]
            },
            {
                "review": "Absolutely fell in love with this dress the first time I wore it. If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress. It did fit true to size and wasn't too short.",
                "output": ["Size and Fit", "Product Quality", "Washing and Maintenance"]
            },
            {
                "review": "Perfect dress for our Kentucky Derby party, and I know I’ll lowest it more than just the one time. Great to dress up with accessories or keep it as is.",
                "output": ["Usage Scenarios and Applicability", "Design and Appearance"]
            },
            {
                "review": "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy.",
                "output": ["Product Quality", "Fabric", "Size and Fit", "Usage Scenarios and Applicability", "Comfort"]
            },
            {
                "review": "Good quality dress, sewn very well. Purchased in my proper size and it fit really well. I would buy from this seller again. I purchased the light blue and the color was just as expected!",
                "output": ["Product Quality", "Size and Fit", "Design and Appearance"]
            },
            {
                "review": "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful.",
                "output": ["Design and Appearance", "Fabric", "Product Quality", "Size and Fit"]
            },
            {
                "review": "The dress is cute and neither frumpy or low cut. It is good for any occasion or just to wear a dress for the heck of it.  Easy to wash and requires no ironing. A great deal!",
                "output": ["Design and Appearance", "Usage Scenarios and Applicability", "Washing and Maintenance", "Price and Value"]
            },
            {
                "review": "This lovely dress is EXACTLY as pictured and was delivered with speed an care! Bravo!",
                "output": ["Design and Appearance", "Shipping and Packaging"]
            },
            {
                "review": "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red. I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I buy the large?).",
                "output": ["Usage Scenarios and Applicability", "Design and Appearance", "Fabric", "Product Quality", "Size and Fit", "Washing and Maintenance"]
            },
            {
                "review": "Such a beautiful and well made dress.  This is my 1st time ordering from this brand.  Quality is excellent.  I ordered a size Small.  I am a 36C  and on the curvy side and fit was just right.  A bigger chest would not fit properly.  I can't wait to order more dresses from this brand.",
                "output": ["Product Quality", "Size and Fit"]
            },
            {
                "review": "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered.",
                "output": ["Fabric", "Size and Fit", "Design and Appearance"]
            },
            {
                "review": "This dress is affordable and worth every penny for its quality.",
                "output": ["Price and Value", "Product Quality"]
            },
            {
                "review": "This dress is beautiful and worth the price. I feel like I got a great deal for such high quality!",
                "output": ["Price and Value", "Product Quality"]
            },
            {
                "review": "The dress's color was completely different from the pictures. I expected red but received pink. The quality also seemed much lower than expected.",
                "output": ["Design and Appearance", "Product Quality"]
            },
            {
                "review": "The package was damaged when it arrived, and the product quality was poor.",
                "output": ["Shipping and Packaging", "Product Quality"]
            },
            {
                "review": "The product looked very different than the pictures, and the material felt cheap.",
                "output": ["Design and Appearance", "Product Quality"]
            },
            {
                "review": "This dress is so different from the photos! The material feels cheap, and it’s definitely not worth what I paid. Very let down!",
                "output": ["Design and Appearance", "Product Quality", "Fabric", "Price and Value"]
            },
            {
                "review": "The fabric is thin and feels very cheap. The overall quality of the stitching and craftsmanship is poor as well.",
                "output": ["Fabric", "Product Quality"]
            },
            {
                "review": "The material feels soft and comfortable, but the stitching is poor and started unraveling after one use.",
                "output": ["Fabric", "Product Quality", "Comfort"]
            },
            {
                "review": "The quality of the material is poor for the price. Disappointed!!",
                "output": ["Price and Value", "Product Quality", "Fabric"]
            }
        ]


        return classification_examples



    def classification_examples_long(self, categories):
        classification_examples = [
            {
                'review': "The fabric pattern was completely different from the pictures. I expected floral but received stripes. The fit was fine, but the pattern was disappointing.",
                'output': ['Fabric', 'Design and Appearance']
            },
            {
                'review': "The color and pattern were not as advertised. I expected vibrant colors, but they were dull and unappealing. Tight fit on the bust as well.",
                'output': ['Design and Appearance', 'Size and Fit']
            },
            {
                'review': "The dress looks beautiful, but the floral pattern was not what I expected. It looked more faded than in the pictures.",
                'output': ['Design and Appearance']
            },
            {
                'review': "This dress is made of breathable cotton, which is perfect for summer.",
                'output': ['Fabric', 'Usage Scenarios and Applicability']
            },
            {
                'review': "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric.",
                'output': ['Design and Appearance', 'Comfort', 'Size and Fit']
            },
            {
                'review': "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!",
                'output': ['Size and Fit', 'Design and Appearance', 'Usage Scenarios and Applicability']
            },
            {
                'review': "Absolutely fell in love with this dress the first time I wore it. If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress. It did fit true to size and wasn't too short.",
                'output': ['Size and Fit', 'Product Quality', 'Washing and Maintenance']
            },
            { 
                'review': "Perfect dress for our Kentucky Derby party, and I know I’ll lowest it more than just the one time. Great to dress up with accessories or keep it as is.",
                'output': ['Usage Scenarios and Applicability', 'Design and Appearance']
            },
            {
                'review': "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy.",
                'output': ['Product Quality', 'Fabric', 'Size and Fit', 'Usage Scenarios and Applicability', 'Comfort']
            },
            { 
                'review': "Good quality dress, sewn very well. Purchased in my proper size and it fit really well. I would buy from this seller again. I purchased the light blue and the color was just as expected!",
                'output': ['Product Quality', 'Size and Fit', 'Design and Appearance']
            },
            {
                'review': "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful.",
                'output': ['Design and Appearance', 'Fabric', 'Product Quality', 'Size and Fit']
            },
            { 
                'review': "The dress is cute and neither frumpy or low cut. It is good for any occasion or just to wear a dress for the heck of it.  Easy to wash and requires no ironing. A great deal!",
                'output': ['Design and Appearance', 'Usage Scenarios and Applicability', 'Washing and Maintenance', 'Price and Value']
            },
            { 
                'review': "This lovely dress is EXACTLY as pictured and was delivered with speed an care! Bravo!",
                'output': ['Design and Appearance', 'Shipping and Packaging']
            },
            {
                'review': "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red. I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I buy the large?).",
                'output': ['Usage Scenarios and Applicability', 'Design and Appearance', 'Fabric', 'Product Quality', 'Size and Fit', 'Washing and Maintenance']
            },
            { 
                'review': "Such a beautiful and well made dress.  This is my 1st time ordering from this brand.  Quality is excellent.  I ordered a size Small.  I am a 36C  and on the curvy side and fit was just right.  A bigger chest would not fit properly.  I can't wait to order more dresses from this brand.",
                'output': ['Product Quality', 'Size and Fit']
            },
            {
                'review': "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered.",
                'output': ['Fabric', 'Size and Fit', 'Design and Appearance']
            },
            {
                'review': "This dress is affordable and worth every penny for its quality.",
                'output': ['Price and Value', 'Product Quality']
            },
            {
                'review': "This dress is beautiful and worth the price. I feel like I got a great deal for such high quality!",
                'output': ['Price and Value', 'Product Quality']
            },
            {
                'review': "The dress's color was completely different from the pictures. I expected red but received pink. The quality also seemed much lower than expected.",
                'output': ['Design and Appearance', 'Product Quality']
            },
            {
                'review': "The package was damaged when it arrived, and the product quality was poor.",
                'output': ['Shipping and Packaging', 'Product Quality']
            },
            {
                'review': "This dress is so different from the photos! The material feels cheap, and it’s definitely not worth what I paid. Very let down!",
                'output': ['Design and Appearance', 'Product Quality', 'Fabric', 'Price and Value']   
            },
            {
                'review': "The fabric is thin and feels very cheap. The overall quality of the stitching and craftsmanship is poor as well.",
                'output': ['Fabric', 'Product Quality']
            },
            {
                'review': "The material feels soft and comfortable, but the stitching is poor and started unraveling after one use.",
                'output': ['Fabric', 'Product Quality', 'Comfort']
            },
            {
                'review': "The quality of the material is poor for the price. Disappointed!!",
                'output': ['Price and Value', 'Product Quality', 'Fabric']
            },
            { 
                'review': "The fabric is very thin and feels cheap. The stitching is poor, and the seams started unraveling after one use.",
                'output': ['Fabric', 'Product Quality']
            },
            {
                'review': "The shorts were also put on wrong so the seams are out instead of facing inward.",
                'output': ['Product Quality']
            },
            {
                'review': "The shorts are very thin and super big. Runs very big.",
                'output': ['Fabric', 'Size and Fit']
            },
            { 
                'review': "This dress is perfect for summer events. It's light, flowy, and stylish.",
                'output': ['Fabric', 'Design and Appearance', 'Usage Scenarios and Applicability']
            }
            
        ]


        return classification_examples




    def create_sentiment_prompt_v5(self, review, predicted_categories, examples=None):
        """
        Generates a sentiment analysis prompt guiding the model to analyze specified categories.

        Args:
            review (str): The product review to analyze.
            predicted_categories (list): The list of categories to analyze.
            examples (list of dict, optional): A list of example dictionaries with 'review', 'categories', and 'output' keys.

        Returns:
            str: The generated prompt string.
        """
        prompt = (
            "Given the product review and its relevant categories, analyze the sentiment (Positive, Negative, or Neutral) for the each categories listed. The categories may vary for each review. Do not add new categories or omit any provided categories."
            "\n\nIMPORTANT:"
            "\n1. If the review contains terms like 'thin', 'too thin', 'thinner', 'cheap feel', 'flimsy', 'poor quality', 'scratchy' or other similar descriptions, especially related to Product Quality, assign a Negative sentiment for that category."
            "\n2. For Product Quality, if terms such as 'nice', 'so nice', 'material is nice', or 'the material is so nice' are present, indicate Positive sentiment for that category."
            "\n3. For Size and Fit, if terms such as 'too big', 'too small', 'tight', 'loose', 'snug', 'fit perfect', or 'true to size' are present, evaluate the sentiment based on whether the fit met expectations (e.g., 'too big' or 'too small' typically indicate Negative sentiment, while 'true to size' or 'fit perfect' indicates Positive sentiment)."
            "\n\nIf a category lacks clear indicators of sentiment, assign a Neutral sentiment for that category."
            "\n\nOutput format:"            
            "\n- Category: Sentiment"
            # "\n\nIMPORTANT: Only analyze the sentiment of categories listed. Do not add new categories or omit any of the given categories."
        )
        
        if examples:
            prompt += "\n\nHere are some examples:"
            for idx, example in enumerate(examples, 1):
                prompt += f"\n\nExample {idx}:\nReview: \"{example['review']}\"\nCategories: {', '.join(example['categories'])}\nOutput:"
                for category, sentiment in example['output'].items():
                    prompt += f"\n- {category}: {sentiment}"
        
        prompt += f"\n\nNow, analyze the sentiment for the following review:\nReview: \"{review}\"\nCategories: {', '.join(predicted_categories)}\nOutput:"
        
        return prompt


    def create_sentiment_prompt_v6(self, review, predicted_categories, examples=None):
        """
        Generates a sentiment analysis prompt guiding the model to analyze specified categories.

        Args:
            review (str): The product review to analyze.
            predicted_categories (list): The list of categories to analyze.
            examples (list of dict, optional): A list of example dictionaries with 'review', 'categories', and 'output' keys.

        Returns:
            str: The generated prompt string.
        """
        prompt = (
            "Given the product review and its relevant categories, analyze the sentiment (Positive, Negative, or Neutral) for the each categories listed. The categories may vary for each review. Do not add new categories or omit any provided categories."
            "\n\nIMPORTANT:"
            "\n1. If the review contains terms like 'different', 'thin', 'too thin', 'thinner', 'cheap feel', 'flimsy', 'poor quality', 'scratchy' or other similar descriptions, especially related to Product Quality, assign a Negative sentiment for that category."
            "\n2. For Product Quality, if terms such as 'nice', 'so nice', 'material is nice', or 'the material is so nice' are present, indicate Positive sentiment for that category."
            "\n3. For Size and Fit, if terms such as 'too big', 'too small', 'tight', 'tighter', 'loose', 'snug', 'fit perfect', or 'true to size' are present, evaluate the sentiment based on whether the fit met expectations (e.g., 'too big' or 'too small' typically indicate Negative sentiment, while 'true to size' or 'fit perfect' indicates Positive sentiment)."
            "\n4. For Design and Appearance, if terms such as 'different', 'hate it', or 'not expected' are present, indicate Negative sentiment for that category. If terms like 'beautiful', 'perfect', 'cute style', 'pretty', or 'great' are present, indicate Positive sentiment for that category"
            "\n\nIf a category lacks clear indicators of sentiment, assign a Neutral sentiment for that category."
            "\n\nOutput format:"            
            "\n- Category: Sentiment"
            # "\n\nIMPORTANT: Only analyze the sentiment of categories listed. Do not add new categories or omit any of the given categories."
        )
        
        if examples:
            prompt += "\n\nHere are some examples:"
            for idx, example in enumerate(examples, 1):
                prompt += f"\n\nExample {idx}:\nReview: \"{example['review']}\"\nCategories: {', '.join(example['categories'])}\nOutput:"
                for category, sentiment in example['output'].items():
                    prompt += f"\n- {category}: {sentiment}"
        
        prompt += f"\n\nNow, analyze the sentiment for the following review:\nReview: \"{review}\"\nCategories: {', '.join(predicted_categories)}\nOutput:"
        
        return prompt

    def create_sentiment_prompt_v7(self, review, predicted_categories, examples=None):
        """
        Generates a sentiment analysis prompt guiding the model to analyze specified categories.

        Args:
            review (str): The product review to analyze.
            predicted_categories (list): The list of categories to analyze.
            examples (list of dict, optional): A list of example dictionaries with 'review', 'categories', and 'output' keys.

        Returns:
            str: The generated prompt string.
        """
        prompt = (
            "Given the product review and its relevant categories, analyze the sentiment (Positive, Negative, or Neutral) for the each categories listed. The categories may vary for each review. Do not add new categories or omit any provided categories."
            "\n\nIMPORTANT:"
            # "\n1. If the review contains terms like 'thin', 'too thin', 'thinner', 'cheap feel', 'flimsy', 'poor quality', 'scratchy' or other similar descriptions, especially related to Product Quality, assign a Negative sentiment for that category."
            "\n1. If the review contains terms like 'different', 'material is different', 'thin', 'too thin', 'thinner', 'cheap feel', 'flimsy', 'poor quality', 'scratchy' or other similar descriptions, especially related to Product Quality, assign a Negative sentiment for that category."
            "\n2. For Product Quality, if terms such as 'nice', 'so nice', 'material is nice', or 'the material is so nice' are present, indicate Positive sentiment for that category."
            #"\n3. For Size and Fit, if terms such as 'too big', 'too small', 'tight', 'tighter', 'loose', 'snug', 'fit perfect', or 'true to size' are present, evaluate the sentiment based on whether the fit met expectations (e.g., 'too big' or 'too small' typically indicate Negative sentiment, while 'true to size' or 'fit perfect' indicates Positive sentiment)."
            "\n3. For Size and Fit, if terms such as 'too big', 'too small', 'tight', 'loose', 'snug', 'fit perfect', or 'true to size' are present, evaluate the sentiment based on whether the fit met expectations (e.g., 'too big' or 'too small' typically indicate Negative sentiment, while 'true to size' or 'fit perfect' indicates Positive sentiment)."
            "\n\nIf a category lacks clear indicators of sentiment, assign a Neutral sentiment for that category."
            "\n\nOutput format:"            
            "\n- Category: Sentiment"
            # "\n\nIMPORTANT: Only analyze the sentiment of categories listed. Do not add new categories or omit any of the given categories."
        )
        
        if examples:
            prompt += "\n\nHere are some examples:"
            for idx, example in enumerate(examples, 1):
                prompt += f"\n\nExample {idx}:\nReview: \"{example['review']}\"\nCategories: {', '.join(example['categories'])}\nOutput:"
                for category, sentiment in example['output'].items():
                    prompt += f"\n- {category}: {sentiment}"
        
        prompt += f"\n\nNow, analyze the sentiment for the following review:\nReview: \"{review}\"\nCategories: {', '.join(predicted_categories)}\nOutput:"
        
        return prompt


    def create_sentiment_prompt_v8(self, review, predicted_categories, examples=None):
        """
        Generates a sentiment analysis prompt guiding the model to analyze specified categories.

        Args:
            review (str): The product review to analyze.
            predicted_categories (list): The list of categories to analyze.
            examples (list of dict, optional): A list of example dictionaries with 'review', 'categories', and 'output' keys.

        Returns:
            str: The generated prompt string.
        """
        prompt = (
            "Given the product review and its relevant categories, analyze the sentiment (Positive, Negative, or Neutral) for each category listed. The sentiment should reflect the tone and context of the review for the specific category. Do not add new categories or omit any provided categories."
            "\n\n###Instructions:"
            "\n1. Analyze the sentiment (Positive, Negative, or Neutral) for each category based on the review."
            "\n2. Assign **Positive Sentiment** for satisfaction, approval, or good experiences."
            "\n3. Assign **Negative Sentiment** for dissatisfaction, criticism, or bad experiences."
            "\n4. Assign **Neutral Sentiment** if the review lacks clear positive or negative indicators for a category."
        )
        if examples:
            prompt += "\n\n### Examples:"
            for idx, example in enumerate(examples, 1):
                prompt += f"\n\nReview: \"{example['review']}\"\nCategories: {', '.join(example['categories'])}\nOutput:"
                for category, sentiment in example['output'].items():
                    prompt += f"\n- {category}: {sentiment}"
        
        prompt += f"\n\nNow, analyze the following review:\nReview: \"{review}\"\nCategories: {', '.join(predicted_categories)}\nOutput:"
        
        return prompt

    def create_sentiment_prompt_v9(self, review, predicted_categories, examples=None):
        """
        Generates a sentiment analysis prompt in JSON format.

        Args:
            review (str): The product review to analyze.
            predicted_categories (list): The list of categories to analyze.
            examples (list of dict, optional): A list of example dictionaries with 'review', 'categories', and 'output' keys.

        Returns:
            dict: A JSON-formatted prompt.
        """
        # Define the system message with task context and instructions
        system_message_json = {
            "role": "system",
            "content": {
                "Persona": "You are a sentiment analyzer tasked with determining the sentiment (Positive, Negative, or Neutral) for specified categories based on product reviews. Follow strict guidelines for accuracy and consistency.",
                "Instructions": [
                    "You will be provided with a product review and a list of categories to analyze.",
                    "For each category, analyze the sentiment based on the review content.",
                    "Assign 'Positive' sentiment for satisfaction, approval, or good experiences. Examples include: 'love it,' 'perfect fit,' 'looks great.' Subtle positivity includes: 'fit to size,' 'just as expected,' 'comfortable and flowy.'",
                    "Assign 'Negative' sentiment for dissatisfaction, criticism, or bad experiences.",
                    "Assign 'Neutral' sentiment only if there are no clear positive or negative indicators for a category."
                ],
                "ImportantNotes": [
                    "Only return the output strictly in the format: [(CATEGORY, SENTIMENT), ...].",
                    "Examples include: [('Fabric', 'Negative'), ('Design and Appearance', 'Positive')].",
                    "Do not add any additional text, explanations, or variations in the format",
                    "Use the examples below for reference."
                ],
                "OutputFormat": "Return the output of sentiment analysis strictly in the format: [('CATEGORY', 'SENTIMENT'), ...]. Examples include: [('Fabric', 'Negative'), ('Design and Appearance', 'Positive')].",
                "Examples": []
            }
        }

        user_message_json = {
            "role": "user",
            "content": f"Review: '{review}'\nCategories: {predicted_categories}\nOutput:"
        }

        if examples:
            for idx, example in enumerate(examples, 1):
                example_entry = {
                    "Review": example["review"],
                    "Categories": example["categories"],
                    "Output": list(example["output"].items())
                }
                system_message_json['content']['Examples'].append(example_entry)

        return [system_message_json, user_message_json]

    def create_sentiment_prompt_v10(self, review, predicted_categories, examples=None):
        """
        Generates a sentiment analysis prompt in JSON format.

        Args:
            review (str): The product review to analyze.
            predicted_categories (list): The list of categories to analyze.
            examples (list of dict, optional): A list of example dictionaries with 'review', 'categories', and 'output' keys.

        Returns:
            dict: A JSON-formatted prompt.
        """
        # Define the system message with task context and instructions
        system_message_json = {
            "role": "system",
            "content": {
                "Persona": "You are a sentiment analyzer tasked with determining the sentiment (Positive, Negative, or Neutral) for specified categories based on product reviews. Follow strict guidelines for accuracy and consistency.",
                "Instructions": [
                    "You will be provided with a product review and a list of categories to analyze.",
                    "For each category, analyze the sentiment based on the review content.",
                    "Assign 'Positive' sentiment for satisfaction, approval, or good experiences. Examples include: 'love it,' 'perfect fit,' 'looks great.' Subtle positivity includes: 'fit to size,' 'just as expected,' 'comfortable and flowy.'",
                    "Assign 'Negative' sentiment for dissatisfaction, criticism, or bad experiences.",
                    "Assign 'Neutral' sentiment only if there are no clear positive or negative indicators for a category."
                ],
                "ImportantNotes": [
                    "Only return the output strictly as a JSON object: [(CATEGORY, SENTIMENT), ...].",
                    "Examples include: [('Fabric', 'Negative'), ('Design and Appearance', 'Positive')].",
                    "Do not add any additional text, explanations, or variations in the format",
                    "Use the examples below for reference."
                ],
                "OutputFormat": "Return the output of sentiment analysis strictly in the format: [('CATEGORY', 'SENTIMENT'), ...]. Examples include: [('Fabric', 'Negative'), ('Design and Appearance', 'Positive')].",
                "Examples": []
            }
        }

        user_message_json = {
            "role": "user",
            "content": f"Review: '{review}'\nCategories: {predicted_categories}\nOutput:"
        }

        if examples:
            for idx, example in enumerate(examples, 1):
                example_entry = {
                    "Review": example["review"],
                    "Categories": example["categories"],
                    "Output": list(example["output"].items())
                }
                system_message_json['content']['Examples'].append(example_entry)

        return [system_message_json, user_message_json]



    
    def sentiment_examples_medium(self):
        examples = [
            {
                'review': "The fabric pattern was completely different from the pictures. I expected floral but received stripes. The fit was fine, but the pattern was disappointing.",
                'categories': ['Fabric', 'Design and Appearance'],
                'output': {
                    'Fabric': 'Negative',
                    'Design and Appearance': 'Negative'
                }
            },
            {
                'review': "The color and pattern were not as advertised. I expected vibrant colors, but they were dull and unappealing. Tight fit on the bust as well.",
                'categories': ['Design and Appearance', 'Size and Fit'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Size and Fit': 'Negative'
                }
            },
            {
                'review': "The dress looks beautiful, but the floral pattern was not what I expected. It looked more faded than in the pictures.",
                'categories': ['Design and Appearance'],
                'output':{
                    'Design and Appearance': 'Neutral'
                }
            },
            {
                'review': "This dress is made of breathable cotton, which is perfect for summer.",
                'categories': ['Fabric', 'Usage Scenarios and Applicability'],
                'output':{
                    'Fabric': 'Positive',
                    'Usage Scenarios and Applicability':'Positive'
                }
            },
            {
                'review': "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric.",
                'categories': ['Design and Appearance', 'Comfort', 'Size and Fit'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Comfort': 'Negative',
                    'Size and Fit': 'Negative'
                }
            },
            {
                'review': "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!",
                'categories': ['Size and Fit', 'Design and Appearance', 'Usage Scenarios and Applicability'],
                'output': {
                    'Design and Appearance': 'Positive',
                    'Usage Scenarios and Applicability': 'Positive',
                    'Size and Fit': 'Positive'
                }
            },
            {
                'review': "Absolutely fell in love with this dress the first time I wore it. If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress. It did fit true to size and wasn't too short.",
                'categories': ['Size and Fit', 'Product Quality', 'Washing and Maintenance'],
                'output': {
                    'Size and Fit': 'Positive',
                    'Product Quality': 'Negative',
                    'Washing and Maintenance': 'Negative'
                }
            },
            { 
                'review': "Perfect dress for our Kentucky Derby party, and I know I’ll lowest it more than just the one time. Great to dress up with accessories or keep it as is.",
                'categories': ['Usage Scenarios and Applicability', 'Design and Appearance'],
                'output': {
                    'Usage Scenarios and Applicability': 'Positive',
                    'Design and Appearance': 'Positive'
                }
            },
            {
                'review': "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy.",
                'categories': ['Product Quality', 'Fabric', 'Size and Fit', 'Usage Scenarios and Applicability', 'Comfort'],
                'output': {
                    'Product Quality': 'Negative',
                    'Fabric': 'Negative',
                    'Size and Fit': 'Positive',
                    'Usage Scenarios and Applicability': 'Positive',
                    'Comfort': 'Positive'

                }
            },
            { 
                'review': "Good quality dress, sewn very well. Purchased in my proper size and it fit really well. I would buy from this seller again. I purchased the light blue and the color was just as expected!",
                'categories': ['Product Quality', 'Size and Fit', 'Design and Appearance'],
                'output': {
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive',
                    'Design and Appearance': 'Positive'
                }
            },
            {
                'review': "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful.",
                'categories': ['Design and Appearance', 'Fabric', 'Product Quality', 'Size and Fit'],
                'output': {
                    'Design and Appearance': 'Positive',
                    'Fabric': 'Positive',
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive'
                }
            },
            { 
                'review': "The dress is cute and neither frumpy or low cut. It is good for any occasion or just to wear a dress for the heck of it.  Easy to wash and requires no ironing. A great deal!",
                'categories': ['Design and Appearance', 'Usage Scenarios and Applicability', 'Washing and Maintenance', 'Price and Value'],
                'output': {
                    'Design and Appearance': 'Positive',
                    'Usage Scenarios and Applicability': 'Positive',
                    'Washing and Maintenance': 'Positive',
                    'Price and Value': 'Positive'
                }
            },
            { 
                'review': "This lovely dress is EXACTLY as pictured and was delivered with speed an care! Bravo!",
                'categories': ['Design and Appearance', 'Shipping and Packaging'],
                'output': {
                    'Design and Appearance': 'Positive',
                    'Shipping and Packaging': 'Positive'
                }
            },
            {
                'review': "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red. I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I buy the large?).",
                'categories': ['Usage Scenarios and Applicability', 'Design and Appearance', 'Fabric', 'Product Quality', 'Size and Fit', 'Washing and Maintenance'],
                'output': {
                    'Usage Scenarios and Applicability': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Fabric': 'Positive',
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive',
                    'Washing and Maintenance': 'Positive'
                }
            },
            { 
                'review': "Such a beautiful and well made dress.  This is my 1st time ordering from this brand.  Quality is excellent.  I ordered a size Small.  I am a 36C  and on the curvy side and fit was just right.  A bigger chest would not fit properly.  I can't wait to order more dresses from this brand.",
                'categories': ['Product Quality', 'Size and Fit'],
                'output': {
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive'
                }
            },
            {
                'review': "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered.",
                'categories': ['Fabric', 'Size and Fit', 'Design and Appearance'],
                'output': {
                    'Fabric': 'Positive',
                    'Size and Fit': 'Positive',
                    'Design and Appearance': 'Positive'
                }
            },
            {
                'review': "This dress is affordable and worth every penny for its quality.",
                'categories': ['Price and Value', 'Product Quality'],
                'output': {
                    'Price and Value': 'Positive',
                    'Product Quality': 'Positive'
                }
            },
            {
                'review': "This dress is beautiful and worth the price. I feel like I got a great deal for such high quality!",
                'categories': ['Price and Value', 'Product Quality'],
                'output': {
                    'Price and Value': 'Positive',
                    'Product Quality': 'Positive'
                }
            },
            {
                'review': "The dress's color was completely different from the pictures. I expected red but received pink. The quality also seemed much lower than expected.",
                'categories': ['Design and Appearance', 'Product Quality'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Product Quality': 'Negative'
                }
            },
            {
                'review': "The package was damaged when it arrived, and the product quality was poor.",
                'categories': ['Shipping and Packaging', 'Product Quality'],
                'output': {
                    'Shipping and Packaging': 'Negative',
                    'Product Quality': 'Negative'
                }
            },
            {
                'review': "The product looked very different than the pictures, and the material felt cheap.",
                'categories': ['Design and Appearance', 'Product Quality'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Product Quality': 'Negative'
                }
            },
            {
                'review': "This dress is so different from the photos! The material feels cheap, and it’s definitely not worth what I paid. Very let down!",
                'categories': ['Design and Appearance', 'Product Quality', 'Fabric', 'Price and Value'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Product Quality': 'Negative',
                    'Fabric': 'Negative',
                    'Price and Value': 'Negative'
                }   
            },
            {
                'review': "The fabric is thin and feels very cheap. The overall quality of the stitching and craftsmanship is poor as well.",
                'categories': ['Fabric', 'Product Quality'],
                'output': {
                    'Fabric': 'Negative',
                    'Product Quality': 'Negative'
                }
            },
            {
                'review': "The material feels soft and comfortable, but the stitching is poor and started unraveling after one use.",
                'categories': ['Fabric', 'Product Quality', 'Comfort'],
                'output': {
                    'Fabric': 'Positive',
                    'Product Quality': 'Negative',
                    'Comfort': 'Positive'
                }
            },
            {
                'review': "The quality of the material is poor for the price. Disappointed!!",
                'categories': ['Price and Value', 'Product Quality', 'Fabric'],
                'output': {
                    'Price and Value': 'Negative',
                    'Product Quality': 'Negative',
                    'Fabric': 'Negative'
                }
            }
        ]
        return examples

    def sentiment_examples_medium_v2(self):
        # JSON format
        examples = [
            {
                "review": "The fabric pattern was completely different from the pictures. I expected floral but received stripes. The fit was fine, but the pattern was disappointing.",
                "categories": ["Fabric", "Design and Appearance"],
                "output": {
                    "Fabric": "Negative",
                    "Design and Appearance": "Negative"
                }
            },
            {
                "review": "The color and pattern were not as advertised. I expected vibrant colors, but they were dull and unappealing. Tight fit on the bust as well.",
                "categories": ["Design and Appearance", "Size and Fit"],
                "output": {
                    "Design and Appearance": "Negative",
                    "Size and Fit": "Negative"
                }
            },
            {
                "review": "The dress looks beautiful, but the floral pattern was not what I expected. It looked more faded than in the pictures.",
                "categories": ["Design and Appearance"],
                "output": {
                    "Design and Appearance": "Neutral"
                }
            },
            {
                "review": "This dress is made of breathable cotton, which is perfect for summer.",
                "categories": ["Fabric", "Usage Scenarios and Applicability"],
                "output": {
                    "Fabric": "Positive",
                    "Usage Scenarios and Applicability": "Positive"
                }
            },
            {
                "review": "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric.",
                "categories": ["Design and Appearance", "Comfort", "Size and Fit"],
                "output": {
                    "Design and Appearance": "Negative",
                    "Comfort": "Negative",
                    "Size and Fit": "Negative"
                }
            },
            {
                "review": "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!",
                "categories": ["Size and Fit", "Design and Appearance", "Usage Scenarios and Applicability"],
                "output": {
                    "Design and Appearance": "Positive",
                    "Usage Scenarios and Applicability": "Positive",
                    "Size and Fit": "Positive"
                }
            },
            {
                "review": "Absolutely fell in love with this dress the first time I wore it. If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress. It did fit true to size and wasn't too short.",
                "categories": ["Size and Fit", "Product Quality", "Washing and Maintenance"],
                "output": {
                    "Size and Fit": "Positive",
                    "Product Quality": "Negative",
                    "Washing and Maintenance": "Negative"
                }
            },
            {
                "review": "Perfect dress for our Kentucky Derby party, and I know I’ll lowest it more than just the one time. Great to dress up with accessories or keep it as is.",
                "categories": ["Usage Scenarios and Applicability", "Design and Appearance"],
                "output": {
                    "Usage Scenarios and Applicability": "Positive",
                    "Design and Appearance": "Positive"
                }
            },
            {
                "review": "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy.",
                "categories": ["Product Quality", "Fabric", "Size and Fit", "Usage Scenarios and Applicability", "Comfort"],
                "output": {
                    "Product Quality": "Negative",
                    "Fabric": "Negative",
                    "Size and Fit": "Positive",
                    "Usage Scenarios and Applicability": "Positive",
                    "Comfort": "Positive"
                }
            },
            {
                "review": "Good quality dress, sewn very well. Purchased in my proper size and it fit really well. I would buy from this seller again. I purchased the light blue and the color was just as expected!",
                "categories": ["Product Quality", "Size and Fit", "Design and Appearance"],
                "output": {
                    "Product Quality": "Positive",
                    "Size and Fit": "Positive",
                    "Design and Appearance": "Positive"
                }
            },
            {
                "review": "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful.",
                "categories": ["Design and Appearance", "Fabric", "Product Quality", "Size and Fit"],
                "output": {
                    "Design and Appearance": "Positive",
                    "Fabric": "Positive",
                    "Product Quality": "Positive",
                    "Size and Fit": "Positive"
                }
            },
            {
                "review": "The dress is cute and neither frumpy or low cut. It is good for any occasion or just to wear a dress for the heck of it.  Easy to wash and requires no ironing. A great deal!",
                "categories": ["Design and Appearance", "Usage Scenarios and Applicability", "Washing and Maintenance", "Price and Value"],
                "output": {
                    "Design and Appearance": "Positive",
                    "Usage Scenarios and Applicability": "Positive",
                    "Washing and Maintenance": "Positive",
                    "Price and Value": "Positive"
                }
            },
            {
                "review": "This lovely dress is EXACTLY as pictured and was delivered with speed an care! Bravo!",
                "categories": ["Design and Appearance", "Shipping and Packaging"],
                "output": {
                    "Design and Appearance": "Positive",
                    "Shipping and Packaging": "Positive"
                }
            },
            {
                "review": "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red. I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I buy the large?).",
                "categories": ["Usage Scenarios and Applicability", "Design and Appearance", "Fabric", "Product Quality", "Size and Fit", "Washing and Maintenance"],
                "output": {
                    "Usage Scenarios and Applicability": "Positive",
                    "Design and Appearance": "Positive",
                    "Fabric": "Positive",
                    "Product Quality": "Positive",
                    "Size and Fit": "Positive",
                    "Washing and Maintenance": "Positive"
                }
            },
            {
                "review": "Such a beautiful and well made dress.  This is my 1st time ordering from this brand.  Quality is excellent.  I ordered a size Small.  I am a 36C  and on the curvy side and fit was just right.  A bigger chest would not fit properly.  I can't wait to order more dresses from this brand.",
                "categories": ["Product Quality", "Size and Fit"],
                "output": {
                    "Product Quality": "Positive",
                    "Size and Fit": "Positive"
                }
            },
            {
                "review": "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered.",
                "categories": ["Fabric", "Size and Fit", "Design and Appearance"],
                "output": {
                    "Fabric": "Positive",
                    "Size and Fit": "Positive",
                    "Design and Appearance": "Positive"
                }
            },
            {
                "review": "This dress is affordable and worth every penny for its quality.",
                "categories": ["Price and Value", "Product Quality"],
                "output": {
                    "Price and Value": "Positive",
                    "Product Quality": "Positive"
                }
            },
            {
                "review": "This dress is beautiful and worth the price. I feel like I got a great deal for such high quality!",
                "categories": ["Price and Value", "Product Quality"],
                "output": {
                    "Price and Value": "Positive",
                    "Product Quality": "Positive"
                }
            },
            {
                "review": "The dress's color was completely different from the pictures. I expected red but received pink. The quality also seemed much lower than expected.",
                "categories": ["Design and Appearance", "Product Quality"],
                "output": {
                    "Design and Appearance": "Negative",
                    "Product Quality": "Negative"
                }
            },
            {
                "review": "The package was damaged when it arrived, and the product quality was poor.",
                "categories": ["Shipping and Packaging", "Product Quality"],
                "output": {
                    "Shipping and Packaging": "Negative",
                    "Product Quality": "Negative"
                }
            },
            {
                "review": "The product looked very different than the pictures, and the material felt cheap.",
                "categories": ["Design and Appearance", "Product Quality"],
                "output": {
                    "Design and Appearance": "Negative",
                    "Product Quality": "Negative"
                }
            },
            {
                "review": "This dress is so different from the photos! The material feels cheap, and it’s definitely not worth what I paid. Very let down!",
                "categories": ["Design and Appearance", "Product Quality", "Fabric", "Price and Value"],
                "output": {
                    "Design and Appearance": "Negative",
                    "Product Quality": "Negative",
                    "Fabric": "Negative",
                    "Price and Value": "Negative"
                }
            },
            {
                "review": "The fabric is thin and feels very cheap. The overall quality of the stitching and craftsmanship is poor as well.",
                "categories": ["Fabric", "Product Quality"],
                "output": {
                    "Fabric": "Negative",
                    "Product Quality": "Negative"
                }
            },
            {
                "review": "The material feels soft and comfortable, but the stitching is poor and started unraveling after one use.",
                "categories": ["Fabric", "Product Quality", "Comfort"],
                "output": {
                    "Fabric": "Positive",
                    "Product Quality": "Negative",
                    "Comfort": "Positive"
                }
            },
            {
                "review": "The quality of the material is poor for the price. Disappointed!!",
                "categories": ["Price and Value", "Product Quality", "Fabric"],
                "output": {
                    "Price and Value": "Negative",
                    "Product Quality": "Negative",
                    "Fabric": "Negative"
                }
            },
            {
                "review": "The dress fit as expected, but I think the oversized style wasn’t for me. Still, it was cute and comfortable.",
                "categories": ["Size and Fit", "Design and Appearance"],
                "output": {
                    "Size and Fit": "Positive",
                    "Design and Appearance": "Positive"
                }
            },
            {
                "review": "Ordered this smaller because of all the reviews but the lining is NOT too small and is fit to size. I think the dress is just an oversized and flowy style. Dress is very comfortable and cute, might reorder in my correct size.",
                "categories": ["Size and Fit", "Design and Appearance"],
                "output": {
                    "Size and Fit": "Positive",
                    "Design and Appearance": "Positive"
                }
            }
        ]
        return examples




    def sentiment_examples_long(self):
        examples = [
            {
                'review': "The fabric pattern was completely different from the pictures. I expected floral but received stripes. The fit was fine, but the pattern was disappointing.",
                'categories': ['Fabric', 'Design and Appearance'],
                'output': {
                    'Fabric': 'Negative',
                    'Design and Appearance': 'Negative'
                }
            },
            {
                'review': "The color and pattern were not as advertised. I expected vibrant colors, but they were dull and unappealing. Tight fit on the bust as well.",
                'categories': ['Design and Appearance', 'Size and Fit'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Size and Fit': 'Negative'
                }
            },
            {
                'review': "The dress looks beautiful, but the floral pattern was not what I expected. It looked more faded than in the pictures.",
                'categories': ['Design and Appearance'],
                'output':{
                    'Design and Appearance': 'Neutral'
                }
            },
            {
                'review': "This dress is made of breathable cotton, which is perfect for summer.",
                'categories': ['Fabric', 'Usage Scenarios and Applicability'],
                'output':{
                    'Fabric': 'Positive',
                    'Usage Scenarios and Applicability':'Positive'
                }
            },
            {
                'review': "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric.",
                'categories': ['Design and Appearance', 'Comfort', 'Size and Fit'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Comfort': 'Negative',
                    'Size and Fit': 'Negative'
                }
            },
            {
                'review': "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!",
                'categories': ['Size and Fit', 'Design and Appearance', 'Usage Scenarios and Applicability'],
                'output': {
                    'Design and Appearance': 'Positive',
                    'Usage Scenarios and Applicability': 'Positive',
                    'Size and Fit': 'Positive'
                }
            },
            {
                'review': "Absolutely fell in love with this dress the first time I wore it. If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress. It did fit true to size and wasn't too short.",
                'categories': ['Size and Fit', 'Product Quality', 'Washing and Maintenance'],
                'output': {
                    'Size and Fit': 'Positive',
                    'Product Quality': 'Negative',
                    'Washing and Maintenance': 'Negative'
                }
            },
            { 
                'review': "Perfect dress for our Kentucky Derby party, and I know I’ll lowest it more than just the one time. Great to dress up with accessories or keep it as is.",
                'categories': ['Usage Scenarios and Applicability', 'Design and Appearance'],
                'output': {
                    'Usage Scenarios and Applicability': 'Positive',
                    'Design and Appearance': 'Positive'
                }
            },
            {
                'review': "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy.",
                'categories': ['Product Quality', 'Fabric', 'Size and Fit', 'Usage Scenarios and Applicability', 'Comfort'],
                'output': {
                    'Product Quality': 'Negative',
                    'Fabric': 'Negative',
                    'Size and Fit': 'Positive',
                    'Usage Scenarios and Applicability': 'Positive',
                    'Comfort': 'Positive'

                }
            },
            { 
                'review': "Good quality dress, sewn very well. Purchased in my proper size and it fit really well. I would buy from this seller again. I purchased the light blue and the color was just as expected!",
                'categories': ['Product Quality', 'Size and Fit', 'Design and Appearance'],
                'output': {
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive',
                    'Design and Appearance': 'Positive'
                }
            },
            {
                'review': "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful.",
                'categories': ['Design and Appearance', 'Fabric', 'Product Quality', 'Size and Fit'],
                'output': {
                    'Design and Appearance': 'Positive',
                    'Fabric': 'Positive',
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive'
                }
            },
            { 
                'review': "The dress is cute and neither frumpy or low cut. It is good for any occasion or just to wear a dress for the heck of it.  Easy to wash and requires no ironing. A great deal!",
                'categories': ['Design and Appearance', 'Usage Scenarios and Applicability', 'Washing and Maintenance', 'Price and Value'],
                'output': {
                    'Design and Appearance': 'Positive',
                    'Usage Scenarios and Applicability': 'Positive',
                    'Washing and Maintenance': 'Positive',
                    'Price and Value': 'Positive'
                }
            },
            { 
                'review': "This lovely dress is EXACTLY as pictured and was delivered with speed an care! Bravo!",
                'categories': ['Design and Appearance', 'Shipping and Packaging'],
                'output': {
                    'Design and Appearance': 'Positive',
                    'Shipping and Packaging': 'Positive'
                }
            },
            {
                'review': "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red. I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I buy the large?).",
                'categories': ['Usage Scenarios and Applicability', 'Design and Appearance', 'Fabric', 'Product Quality', 'Size and Fit', 'Washing and Maintenance'],
                'output': {
                    'Usage Scenarios and Applicability': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Fabric': 'Positive',
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive',
                    'Washing and Maintenance': 'Positive'
                }
            },
            { 
                'review': "Such a beautiful and well made dress.  This is my 1st time ordering from this brand.  Quality is excellent.  I ordered a size Small.  I am a 36C  and on the curvy side and fit was just right.  A bigger chest would not fit properly.  I can't wait to order more dresses from this brand.",
                'categories': ['Product Quality', 'Size and Fit'],
                'output': {
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive'
                }
            },
            {
                'review': "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered.",
                'categories': ['Fabric', 'Size and Fit', 'Design and Appearance'],
                'output': {
                    'Fabric': 'Positive',
                    'Size and Fit': 'Positive',
                    'Design and Appearance': 'Positive'
                }
            },
            {
                'review': "This dress is affordable and worth every penny for its quality.",
                'categories': ['Price and Value', 'Product Quality'],
                'output': {
                    'Price and Value': 'Positive',
                    'Product Quality': 'Positive'
                }
            },
            {
                'review': "This dress is beautiful and worth the price. I feel like I got a great deal for such high quality!",
                'categories': ['Price and Value', 'Product Quality'],
                'output': {
                    'Price and Value': 'Positive',
                    'Product Quality': 'Positive'
                }
            },
            {
                'review': "The dress's color was completely different from the pictures. I expected red but received pink. The quality also seemed much lower than expected.",
                'categories': ['Design and Appearance', 'Product Quality'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Product Quality': 'Negative'
                }
            },
            {
                'review': "The package was damaged when it arrived, and the product quality was poor.",
                'categories': ['Shipping and Packaging', 'Product Quality'],
                'output': {
                    'Shipping and Packaging': 'Negative',
                    'Product Quality': 'Negative'
                }
            },
            {
                'review': "This dress is so different from the photos! The material feels cheap, and it’s definitely not worth what I paid. Very let down!",
                'categories': ['Design and Appearance', 'Product Quality', 'Fabric', 'Price and Value'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Product Quality': 'Negative',
                    'Fabric': 'Negative',
                    'Price and Value': 'Negative'
                }   
            },
            {
                'review': "The fabric is thin and feels very cheap. The overall quality of the stitching and craftsmanship is poor as well.",
                'categories': ['Fabric', 'Product Quality'],
                'output': {
                    'Fabric': 'Negative',
                    'Product Quality': 'Negative'
                }
            },
            {
                'review': "The material feels soft and comfortable, but the stitching is poor and started unraveling after one use.",
                'categories': ['Fabric', 'Product Quality', 'Comfort'],
                'output': {
                    'Fabric': 'Positive',
                    'Product Quality': 'Negative',
                    'Comfort': 'Positive'
                }
            },
            {
                'review': "The quality of the material is poor for the price. Disappointed!!",
                'categories': ['Price and Value', 'Product Quality', 'Fabric'],
                'output': {
                    'Price and Value': 'Negative',
                    'Product Quality': 'Negative',
                    'Fabric': 'Negative'
                }
            },
            { 
                'review': "The fabric is very thin and feels cheap. The stitching is poor, and the seams started unraveling after one use.",
                'categories': ['Fabric', 'Product Quality'],
                'output': {
                    'Fabric': 'Negative',
                    'Product Quality': 'Negative'
                }
            },
            {
                'review': "The shorts were also put on wrong so the seams are out instead of facing inward.",
                'categories': ['Product Quality'],
                'output': {
                    'Product Quality': 'Negative'
                }
            },
            {
                'review': "The shorts are very thin and super big. Runs very big.",
                'categories': ['Fabric', 'Size and Fit'],
                'output': {
                    'Fabric': 'Negative',
                    'Size and Fit': 'Negative'
                }
            },
            { 
                'review': "This dress is perfect for summer events. It's light, flowy, and stylish.",
                'categories': ['Fabric', 'Design and Appearance', 'Usage Scenarios and Applicability'],
                'output': {
                    'Fabric': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Usage Scenarios and Applicability': 'Positive'
                }
            }
        ]
        return examples



    def sentiment_examples_brief(self):
        examples = [
            {
                'review': "This is one of those rare Allegra dresses I have bought that fits perfectly and looks great. My only complaint is that the description states there is a self-tie sash, and the dress I received did not have a sash at all. I am still giving the product five stars because I think the price/quality ratio is excellent. I have ordered a number of Allegra items and returned most because they didn't fit properly. I've also received Allegra dresses with major quality control issues (kind of what you would expect at this price point) in the past. This particular dress is perfect, and I am very happy with it. Note: I am 5' 3\", and the hem hits right at my knee.",
                'categories': ['Size and Fit', 'Design and Appearance', 'Product Quality', 'Price and Value', 'Overall Satisfaction', 'Brand and Customer Service'],
                'output': {
                    'Size and Fit': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Product Quality': 'Neutral',
                    'Price and Value': 'Positive',
                    'Overall Satisfaction': 'Positive',
                    'Brand and Customer Service': 'Neutral'
                }
            },
            {
                'review': "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric.",
                'categories': ['Design and Appearance', 'Comfort', 'Size and Fit', 'Overall Satisfaction'],
                'output': {
                    'Design and Appearance': 'Negative',
                    'Comfort': 'Negative',
                    'Size and Fit': 'Negative',
                    'Overall Satisfaction': 'Negative'
                }
            },
            {
                'review': "I had high hopes for this but unfortunately ended up having to return. It was very big and unflattering, kind of like a tent. I would say if you are between a L/XL definitely size down. The shipping was fast, but overall just did not like the dress.",
                'categories': ['Size and Fit', 'Design and Appearance', 'Shipping and Packaging', 'Overall Satisfaction'],
                'output': {
                    'Size and Fit': 'Negative',
                    'Design and Appearance': 'Negative',
                    'Shipping and Packaging': 'Positive',
                    'Overall Satisfaction': 'Negative'
                }
            },
            {
                'review': "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!",
                'categories': ['Size and Fit', 'Design and Appearance', 'Usage Scenarios and Applicability'],
                'output': {
                    'Size and Fit': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Usage Scenarios and Applicability': 'Positive'
                }
            },
            {
                'review': "Absolutely fell in love with this dress the first time I wore it.  If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress.  It did fit true to size and wasn't too short.",
                'categories': ['Design and Appearance', 'Size and Fit', 'Product Quality', 'Washing and Maintenance'],
                'output': {
                    'Design and Appearance': 'Positive',
                    'Size and Fit': 'Positive',
                    'Product Quality': 'Negative',
                    'Washing and Maintenance': 'Negative'
                }
            },
            {
                'review': "Perfect dress for our Kentucky Derby party, and I know I’ll lowest it more than just the one time. Great to dress up with accessories or keep it as is.",
                'categories': ['Usage Scenarios and Applicability', 'Design and Appearance', 'Overall Satisfaction'],
                'output': { 
                    'Usage Scenarios and Applicability': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Overall Satisfaction': 'Positive'
                }
            },
            {
                'review': "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy.",
                'categories': ['Usage Scenarios and Applicability', 'Size and Fit', 'Comfort', 'Product Quality', 'Overall Satisfaction'],
                'output': {
                    'Usage Scenarios and Applicability': 'Positive',
                    'Size and Fit': 'Positive',
                    'Comfort': 'Positive',
                    'Product Quality': 'Neutral',
                    'Overall Satisfaction': 'Positive'
                }
            },
            {
                'review': "Good quality dress, sewn very well. Purchased in my proper size and it fit really well. I would buy from this seller again. I purchased the light blue and the color was just as expected!",
                'categories': ['Product Quality', 'Size and Fit', 'Design and Appearance', 'Overall Satisfaction'],
                'output': { 
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Overall Satisfaction': 'Positive'
                }
            },
            {
                'review': "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful.",
                'categories': ['Design and Appearance', 'Product Quality', 'Size and Fit'],
                'output': { 
                    'Design and Appearance': 'Positive',
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Neutral'
                }
            },
            {
                'review': "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red. I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I buy the large?).",
                'categories': ['Usage Scenarios and Applicability', 'Design and Appearance', 'Product Quality', 'Size and Fit', 'Washing and Maintenance'],
                'output': {
                    'Usage Scenarios and Applicability': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Neutral',
                    'Washing and Maintenance': 'Positive'
                }
            },
            {
                'review': "Such a beautiful and well made dress.  This is my 1st time ordering from this brand.  Quality is excellent.  I ordered a size Small.  I am a 36C  and on the curvy side and fit was just right.  A bigger chest would not fit properly.  I can't wait to order more dresses from this brand.",
                'categories': ['Product Quality', 'Size and Fit', 'Brand and Customer Service', 'Overall Satisfaction'],
                'output': { 
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive',
                    'Brand and Customer ': 'Positive',
                    'Overall Satisfaction': 'Positive'
                }
            },
            {
                'review': "Very clean product. The fabric, craftsmanship, and underneath slip are all thick and very well made. No cheap materials, no messy stitching, no misalignments. Looks and feels like a dress you could easily pay more money for, at a small chic boutique by the beach...",
                'categories': ['Product Quality', 'Design and Appearance', 'Price and Value', 'Overall Satisfaction'],
                'output': {
                    'Product Quality': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Price and Value': 'Positive',
                    'Overall Satisfaction': 'Positive'
                }
            },
            { 
                'review': "The material is soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered.",
                'categories': ['Product Quality', 'Size and Fit', 'Design and Appearance', 'Brand and Customer Service', 'Overall Satisfaction'],
                'output': {
                    'Product Quality': 'Positive',
                    'Size and Fit': 'Positive',
                    'Design and Appearance': 'Positive',
                    'Brand and Customer Service': 'Positive',
                    'Overall Satisfaction': 'Positive'
                }
            }
        ]
        return examples


    def character_matching(self, review, categories):

        # for Product Quality
        review = review.lower()
        category_1 = 'Product Quality'
        matching_pool_1 = ['quality']
        for char in matching_pool_1:
            if char in review:
                if category_1 not in categories:
                    categories.append(category_1)
                break
        
        # for Size and Fit
        category_2 = 'Size and Fit'
        matching_pool_2 = ['size', 'fit', 'fits',  'big', 'small', 'tight', 'tighter', 'loose', 'snug']
        for char in matching_pool_2:
            if char in review:
                if category_2 not in categories:
                    categories.append(category_2)
                break

        # for Design and Appearance
        category_3 = 'Design and Appearance'
        matching_pool_3 = ['pattern', 'flowy', 'sew', 'cool', 'cute', 'color', 'design', 'shape', 'pretty', 'flattering', 'look', 'elegant', 'style']
        for char in matching_pool_3:
            if char in review:
                if category_3 not in categories:
                    categories.append(category_3)
                break
        
        # for Price and Value
        category_4 = 'Price and Value'
        matching_pool_4 = ['worth', 'price']
        for char in matching_pool_4:
            if char in review:
                if category_4 not in categories:
                    categories.append(category_4)
                break

        # for Usage Scenarios and Applicability
        category_5 = 'Usage Scenarios and Applicability'
        matching_pool_5 = ['casual', 'festival', 'breastfeeding', 'restroom', 'slip on', 'dressed up', 'heel', 'earring', 'grad','party', 'parties',  'nature call','wedding', 'school', 'university', 'college', 'summer', 'winter', 'occasion']
        for char in matching_pool_5:
            if char in review:
                if category_5 not in categories:
                    categories.append(category_5)
                break

        # for Comfort
        category_6 = 'Comfort'
        matching_pool_6 = ['comfort', 'comfortable', 'comfy']
        for char in matching_pool_6:
            if char in review:
                if category_6 not in categories:
                    categories.append(category_6)
                break
        for char in matching_pool_6:
            if char not in review and 'Comfort' in categories:
                categories.remove('Comfort')

        # for Washing and Maintenance
        category_7 = 'Washing and Maintenance'
        matching_pool_7 = ['steam', 'iron']
        for char in matching_pool_7:
            if char in review:
                if category_7 not in categories:
                    categories.append(category_7)
                break
        
        # for Fabric
        category_8 = 'Fabric'
        matching_pool_8 = ['thin', 'fabric']
        review_replaced = review.replace('think', '_')
        for word in matching_pool_8:
            if word in review_replaced:
                if category_8 not in categories:
                    categories.append(category_8)
                break

        return categories

    def sentiment_matching(self, sentiments_dict_row, review):
        review = review.lower()
        sentiment_series = pd.Series(sentiments_dict_row)
        sentimental = sentiment_series.drop(['review_text', 'id'])
        
        # 判断整体的感情倾向
        value_counts_series = sentimental.value_counts()
        if len(value_counts_series) == 1:
            if value_counts_series.values[0] > 1:
                sentiments_dict_row['Overall Satisfaction'] = value_counts_series.index[0]
        
        return sentiments_dict_row


    def sentiment_matching_v2(self, sentiments_dict_row, review):
        review = review.lower()
        
        # Design and Appearance
        sentiments_pool_1 = ['cute', 'cute style', 'flattering', 'beautiful', 'pretty', 'color', 'cool', 'lining', 'flowy', 'lovely']
        for char in sentiments_pool_1:
            if char in review and sentiments_dict_row['Design and Appearance'] != 'Negative':
                sentiments_dict_row['Design and Appearance'] = 'Positive'
        sentiments_pool_1_1 = ['pretty dress']
        for char in sentiments_pool_1_1:
            if char in review:
                sentiments_dict_row['Design and Appearance'] = 'Positive'

        # Size and Fit
        sentiments_pool_2 = ['small']
        for char in sentiments_pool_2:
            if char in review and sentiments_dict_row['Size and Fit'] != 'Positive':
                sentiments_dict_row['Size and Fit'] = 'Negative'
        sentiments_pool_2_1 = ['fit']
        for char in sentiments_pool_2_1:
            if char in review and sentiments_dict_row['Size and Fit'] != 'Negative':
                sentiments_dict_row['Size and Fit'] = 'Positive'
        sentiments_pool_2_2 = ['tight']
        for char in sentiments_pool_2_2:
            if char in review:
                sentiments_dict_row['Size and Fit'] = 'Negative'

        # Product Quality
        # sentiments_pool_3 = ['cheap', 'itchy']
        # for char in sentiments_pool_3:
        #     if char in review and sentiments_dict_row['Product Quality'] != 'Positive':
        #         sentiments_dict_row['Product Quality'] = 'Negative'
        # sentiments_pool_3_1 = ['material is nice', 'material is pleasant']
        # for char in sentiments_pool_3_1:
        #     if char in review:
        #         sentiments_dict_row['Product Quality'] = 'Positive'
        
        # comfort
        sentiments_pool_4 = ['comfort', 'comfy', 'comfortable']
        for char in sentiments_pool_4:
            if char in review and sentiments_dict_row['Comfort'] != 'Negative':
                sentiments_dict_row['Comfort'] = 'Positive'

        
        # Usage Scenarios and Applicability 
        sentiments_pool_6 = ['nature calls']
        for char in sentiments_pool_6:
            if char in review and sentiments_dict_row['Usage Scenarios and Applicability'] != 'Positive':
                sentiments_dict_row['Usage Scenarios and Applicability'] = 'Negative'

        # Washing and Maintenance
        sentiments_pool_7 = ['steam', 'iron']
        for char in sentiments_pool_7:
            if char in review and sentiments_dict_row['Washing and Maintenance'] != 'Positive':
                sentiments_dict_row['Washing and Maintenance'] = 'Negative'

        # Fabric
        sentiments_pool_8 = ['different', 'itchy']
        for char in sentiments_pool_8:
            if char in review and sentiments_dict_row['Fabric'] == 'Neutral':
                sentiments_dict_row['Fabric'] = 'Negative'
        sentiments_pool_3_1 = ['material is nice', 'material is pleasant']
        for char in sentiments_pool_3_1:
            if char in review:
                sentiments_dict_row['Fabric'] = 'Positive'

        return sentiments_dict_row

        
