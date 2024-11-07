import os
import sys
from common.script_base import ScriptBase
import textwrap

class PromptTuning(ScriptBase):

    # 定义 Prompt 模板
    def create_prompt_one_mission(self, review, categories, examples=None):
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
    
    def examples_prompt_one_mission_medium_length(self):
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
        Review: "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it’s a good buy."
        Output:
        - Usage Scenarios and Applicability: Positive
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

    def examples_prompt_one_mission_brief_length(self):
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

    def examples_prompt_one_mission_long_length(self):
        examples = textwrap.dedent("""
        Example 1: 
        Review: "This is one of those rare Allegra dresses I have bought that fits perfectly and looks great. My only complaint is that the description states there is a self-tie sash, and the dress I received did not have a sash at all. I am still giving the product five stars because I think the price/quality ratio is excellent. I have ordered a number of Allegra items and returned most because they didn't fit properly. I've also received Allegra dresses with major quality control issues (kind of what you would expect at this price point) in the past. This particular dress is perfect, and I am very happy with it. Note: I am 5' 3", and the hem hits right at my knee."
        Output:
        - Size and Fit: Positive
        - Design and Appearance: Positive
        - Product Quality: Positive
        - Price and Value: Positive
        - Overall Satisfaction: Positive
        - Brand and Customer Service: Neutral

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
        - Size and Fit
        - Design and Appearance
        - Shipping and Packaging
        - Overall Satisfaction
                                   
        Example 4:
        Review: "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!"
        Output:
        - Size and Fit: Positive
        - Design and Appearance: Positive
        - Usage Scenarios and Applicability: Positive
        
        Example 5:
        Review: "Absolutely fell in love with this dress the first time I wore it.  If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress.  It did fit true to size and wasn't too short."
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
        Review: "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy."
        Output:
        - Usage Scenarios and Applicability: Positive
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
                                   
        Example 17:
        Review: "This dress has a cute top half but the layers on the skirt are cut weird and make your hips look big.  The small was a little loose but I wouldn’t size up.  Material is ok.  Doesn’t look like it will wrinkle at all.  Shorter in front and longer in back.  Love the print."                           
        Output:
        - Design and Appearance: Neutral
        - Size and Fit: Negative
        - Product Quality: Neutral
        - Overall Satisfaction: Neutral                           
                                   
        Example 18:
        Review: "I relied on several reviews when picking this dress so I thought I’d leave my own. It’s very cute on and comfy. I am 5’2” and about 128lbs. Almost always order a medium but I saw this runs big. It definitely does.  I ordered a small and ended up using small safety pins at the waist to cinch it in a bit. I could’ve gotten away with the extra small but I can make this work. I would’ve given it five stars except for how large it runs and it arrived with one of the bottoms missing on the right sleeve cuff. They send an extra so I can take care of this as well."
        Output:
        - Design and Appearance: Positive
        - Comfort: Positive
        - Size and Fit: Neutral
        - Shipping and Packaging: Negative
        - Brand and Customer Service: Neutral                                                   

        Example 19:
        Review: "I've purchased multiple items from the brand before and I've never had a problem with anything fitting before this dress. The dress was beautiful and i ordered based on the size chart but all big armed buyers should be wary because my arms did not fit and i had to return it unfortunately."
        Output:
        - Design and Appearance: Positive
        - Size and Fit: Negative
        - Overall Satisfaction: Negative
        - Brand and Customer Service: Neutral                           

        Example 20: 
        Review: "I am super happy with this purchase!! I was a little worried since the model seems to maybe imply the clothes will be junior sizes but I decided to trust the measurements provided by Allegra K because the dress is so pretty and I am glad I did! Im a large and am curvy and it fit so well and looked so cute! I really appreciate Allegra K because it seems usually these styles of clothes run really small but they have realistic sizes for all women and I'm such a fan!! Love everything about it. Thank you!"
        Output:                            
        - Size and Fit: Positive
        - Design and Appearance: Positive
        - Overall Satisfaction: Positive
        - Brand and Customer Service: Positive

        Example 21:
        Review: "Such a lovely color. Material is so soft and flowy. Bought this in medium and it fit slightly loose which was what I wanted. Wish it had an inner lining to it (which is why I'm giving it 4 stars) but other than that, it's such a pretty dress. Note that it was just a tad but more fitted at the chest for me but flowy everywhere else. For reference I'm 36 DD 5'4 and 140 lbs."
        Output:
        - Design and Appearance: Positive
        - Comfort: Positive
        - Size and Fit: Positive
        - Product Quality: Neutral
        - Overall Satisfaction: Positive
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
    
    
    def create_classification_prompt_v2(self, review, categories, classification_examples=None):
        prompt = (
            f"Classify the following product review into one or more of the following categories: {', '.join(categories)}.\n"
            "You do not need to repeat any part of the input. Just output the categories that apply in the format\n"
            "- Category"
        )
        if classification_examples:
            prompt += "\n\nHere are some examples:"
            for idx, example in enumerate(classification_examples, start=1):
                prompt += f"\n\nExample {idx}:\nReview: \"{example['review']}\"\nCategories: {', '.join(example['category'])}\nOutput:"
                for category in example['output']:
                    prompt += f"\n- {category}"
        
        prompt += f"\n\nNow, classify the following review and provide the category only:\nReview: '{review}'\nCategories: {', '.join(categories)}\nOutput:"
        return prompt

    def create_classification_prompt_v3(self, review, categories, classification_examples=None):
        prompt = (
            f"Classify the following product review into one or more of the following categories, considering especially whether there are any comments indicating Overall Satisfaction with the product: {', '.join(categories)}.\n"
            "You do not need to repeat any part of the input. Just output the categories that apply in the format\n"
            "- Category"
        )
        if classification_examples:
            prompt += "\n\nHere are some examples, with particular attention given to comments reflecting Overall Satisfaction:"
            for idx, example in enumerate(classification_examples, start=1):
                prompt += f"\n\nExample {idx}:\nReview: \"{example['review']}\"\nCategories: {', '.join(example['category'])}\nOutput:"
                for category in example['output']:
                    prompt += f"\n- {category}"
        
        prompt += f"\n\nNow, classify the following review and provide the category only:\nReview: '{review}'\nCategories: {', '.join(categories)}\nOutput:"
        return prompt




    def classification_examples_long(self, categories):

        classification_examples = [
            {
                'review': "This is one of those rare Allegra dresses I have bought that fits perfectly and looks great. My only complaint is that the description states there is a self-tie sash, and the dress I received did not have a sash at all. I am still giving the product five stars because I think the price/quality ratio is excellent. I have ordered a number of Allegra items and returned most because they didn't fit properly. I've also received Allegra dresses with major quality control issues (kind of what you would expect at this price point) in the past. This particular dress is perfect, and I am very happy with it. Note: I am 5' 3\", and the hem hits right at my knee.", 
                'category': categories,
                'output': ['Size and Fit', 'Design and Appearance', 'Product Quality', 'Price and Value', 'Overall Satisfaction', 'Brand and Customer Service']
            },
            {
                'review': "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric.",
                'category': categories,  # 动态的 categories 列表
                'output': ['Design and Appearance', 'Comfort', 'Size and Fit', 'Overall Satisfaction']
            },
            {
                'review': "I had high hopes for this but unfortunately ended up having to return. It was very big and unflattering, kind of like a tent. I would say if you are between a L/XL definitely size down. The shipping was fast, but overall just did not like the dress.",
                'category': categories,  # 动态的 categories 列表
                'output': ['Size and Fit', 'Design and Appearance', 'Shipping and Packaging', 'Overall Satisfaction']
            },
            {
                'review': "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!",
                'category': categories,  # 动态的 categories 列表
                'output': ['Size and Fit', 'Design and Appearance', 'Usage Scenarios and Applicability']
            },
            {
                'review': "Absolutely fell in love with this dress the first time I wore it. If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress. It did fit true to size and wasn't too short.",
                'category': categories,
                'output': ['Design and Appearance', 'Size and Fit', 'Product Quality', 'Washing and Maintenance']
            },
            {
                'review': "I got this because I thought it would be breast feeding friendly. It’s is amazing. Super easy to breast feed in, looks awesome with a denim jacket, and makes me look like I wasn’t even pregnant. I have it in four colors. Highly recommend ??",
                'category': categories,
                'output': ['Usage Scenarios and Applicability', 'Design and Appearance', 'Overall Satisfaction']
            },
            {
                'review': "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy.",
                'category': categories,
                'output': ['Usage Scenarios and Applicability', 'Size and Fit', 'Comfort', 'Product Quality', 'Overall Satisfaction']
            },
            {
                'review': "The fabric of this product is good and not cheap! The wrinkles were expected because of it being packaged but that can be easily fixed. The color is exactly as pictured and the fit of it is great. I ordered a medium and I'm comfortable in it.",
                'category': categories,
                'output': ['Shipping and Packaging', 'Product Quality', 'Design and Appearance', 'Size and Fit', 'Comfort']
            },
            {
                'review': "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful.",
                'category': categories,
                'output': ['Design and Appearance', 'Product Quality', 'Color and Appearance', 'Size and Fit']
            },
            {
                'review': "Dress was not the same pattern. It looked cheap. No tags whatsoever to know how to care for it. Ordered normal size and was small looking because of elastic in waist. Wasn't at all flowing like the style. Returning for sure.",
                'category': categories,
                'output': ['Product Quality', 'Size and Fit', 'Washing and Maintenance', 'Overall Satisfaction', 'Design and Appearance']
            },
            {
                'review': "Washed it for the first time and there are strings and hems coming undone all over. Went to exchange or return it and apparently my window closed, such a bummer, it really is a cute dress!",
                'category': categories,
                'output': ['Product Quality', 'Washing and Maintenance', 'Brand and Customer Service', 'Design and Appearance']
            },
            {
                'review': "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red. I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I buy the large?).",
                'category': categories,
                'output': ['Usage Scenarios and Applicability', 'Design and Appearance', 'Product Quality', 'Size and Fit', 'Washing and Maintenance']
            },
            {
                'review': "This dress was sized at a 12 to 14, which should have been fine. Was too small, came all bunched up in a bag and wrinkled, the fabric is not very breathable and I did not care for the dress at all. Looks lovely in the picture, but I actually hated it.",
                'category': categories,
                'output': ['Size and Fit', 'Shipping and Packaging', 'Product Quality', 'Design and Appearance']
            },
            {
                'review': "Very clean product. The fabric, craftsmanship, and underneath slip are all thick and very well made. No cheap materials, no messy stitching, no misalignments. Looks and feels like a dress you could easily pay more money for, at a small chic boutique by the beach...",
                'category': categories,
                'output': ['Product Quality', 'Design and Appearance', 'Price and Value', 'Overall Satisfaction']
            },
            {
                'review': "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered.",
                'category': categories,
                'output': ['Size and Fit', 'Color and Appearance', 'Shipping and Packaging', 'Brand and Customer Service']
            },
            {
                'review': "This is a pretty, flowy dress. It's lightweight enough for summer, but it's not see thru. I love Nemidor dresses, and I plan on buying more of them when they go on sale. They feel good on, and they make you feel good when your wear them.",
                'category': categories,
                'output': ['Design and Appearance', 'Product Quality', 'Comfort', 'Brand and Customer Service', 'Overall Satisfaction']
            },
            {
                'review': "This dress has a cute top half but the layers on the skirt are cut weird and make your hips look big. The small was a little loose but I wouldn’t size up. Material is ok. Doesn’t look like it will wrinkle at all. Shorter in front and longer in back. Love the print.",
                'category': categories,
                'output': ['Design and Appearance', 'Size and Fit', 'Product Quality', 'Overall Satisfaction']
            },
            {
                'review': "I relied on several reviews when picking this dress so I thought I’d leave my own. It’s very cute on and comfy. I am 5’2” and about 128lbs. Almost always order a medium but I saw this runs big. It definitely does. I ordered a small and ended up using small safety pins at the waist to cinch it in a bit. I could’ve gotten away with the extra small but I can make this work. I would’ve given it five stars except for how large it runs and it arrived with one of the bottoms missing on the right sleeve cuff. They send an extra so I can take care of this as well.",
                'category': categories,
                'output': ['Size and Fit', 'Comfort', 'Product Quality', 'Shipping and Packaging', 'Overall Satisfaction']
            },
            {
                'review': "I've purchased multiple items from the brand before and I've never had a problem with anything fitting before this dress. The dress was beautiful and I ordered based on the size chart but all big armed buyers should be wary because my arms did not fit and I had to return it unfortunately.",
                'category': categories,
                'output': ['Size and Fit', 'Design and Appearance', 'Overall Satisfaction', 'Brand and Customer Service']
            },
            {
                'review': "I am super happy with this purchase!! I was a little worried since the model seems to maybe imply the clothes will be junior sizes but I decided to trust the measurements provided by Allegra K because the dress is so pretty and I am glad I did! I'm a large and am curvy and it fit so well and looked so cute! I really appreciate Allegra K because it seems usually these styles of clothes run really small but they have realistic sizes for all women and I'm such a fan!! Love everything about it. Thank you!",
                'category': categories,
                'output': ['Size and Fit', 'Design and Appearance', 'Overall Satisfaction', 'Brand and Customer Service']
            },
            {
                'review': "Such a lovely color. Material is so soft and flowy. Bought this in medium and it fit slightly loose which was what I wanted. Wish it had an inner lining to it (which is why I'm giving it 4 stars) but other than that, it's such a pretty dress. Note that it was just a tad but more fitted at the chest for me but flowy everywhere else. For reference I'm 36 DD 5'4 and 140 lbs.",
                'category': categories,
                'output': ['Design and Appearance', 'Comfort', 'Size and Fit', 'Product Quality', 'Overall Satisfaction']
            }
        ]

        return classification_examples
    
    def classification_examples_medium(self, categories):
        classification_examples = [
            {
                'review': "This is one of those rare Allegra dresses I have bought that fits perfectly and looks great. My only complaint is that the description states there is a self-tie sash, and the dress I received did not have a sash at all. I am still giving the product five stars because I think the price/quality ratio is excellent. I have ordered a number of Allegra items and returned most because they didn't fit properly. I've also received Allegra dresses with major quality control issues (kind of what you would expect at this price point) in the past. This particular dress is perfect, and I am very happy with it. Note: I am 5' 3\", and the hem hits right at my knee.", 
                'category': categories,
                'output': ['Size and Fit', 'Design and Appearance', 'Product Quality', 'Price and Value', 'Overall Satisfaction', 'Brand and Customer Service']
            },
            {
                'review': "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric.",
                'category': categories,  # 动态的 categories 列表
                'output': ['Design and Appearance', 'Comfort', 'Size and Fit', 'Overall Satisfaction']
            },
            {
                'review': "I had high hopes for this but unfortunately ended up having to return. It was very big and unflattering, kind of like a tent. I would say if you are between a L/XL definitely size down. The shipping was fast, but overall just did not like the dress.",
                'category': categories,  # 动态的 categories 列表
                'output': ['Size and Fit', 'Design and Appearance', 'Shipping and Packaging', 'Overall Satisfaction']
            },
            {
                'review': "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!",
                'category': categories,  # 动态的 categories 列表
                'output': ['Size and Fit', 'Design and Appearance', 'Usage Scenarios and Applicability']
            },
            {
                'review': "Absolutely fell in love with this dress the first time I wore it. If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress. It did fit true to size and wasn't too short.",
                'category': categories,
                'output': ['Design and Appearance', 'Size and Fit', 'Product Quality', 'Washing and Maintenance']
            },
            { 
                'review': "Perfect dress for our Kentucky Derby party, and I know I’ll lowest it more than just the one time. Great to dress up with accessories or keep it as is.",
                'category': categories,
                'output': ['Usage Scenarios and Applicability', 'Design and Appearance', 'Overall Satisfaction']
            },
            {
                'review': "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy.",
                'category': categories,
                'output': ['Usage Scenarios and Applicability', 'Size and Fit', 'Comfort', 'Product Quality', 'Overall Satisfaction']
            },
            { 
                'review': "Good quality dress, sewn very well. Purchased in my proper size and it fit really well. I would buy from this seller again. I purchased the light blue and the color was just as expected!",
                'category': categories,
                'output': ['Product Quality', 'Size and Fit', 'Design and Appearance', 'Overall Satisfaction']
            },
            {
                'review': "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful.",
                'category': categories,
                'output': ['Design and Appearance', 'Product Quality', 'Size and Fit']
            },
            { 
                'review': "The dress is cute and neither frumpy or low cut. It is good for any occasion or just to wear a dress for the heck of it.  Easy to wash and requires no ironing. A great deal!",
                'category': categories,
                'output': ['Design and Appearance', 'Usage Scenarios and Applicability', 'Washing and Maintenance', 'Price and Value']
            },
            { 
                'review': "This lovely dress is EXACTLY as pictured and was delivered with speed an care! Bravo!",
                'category': categories,
                'output': ['Design and Appearance', 'Shipping and Packaging', 'Overall Satisfaction']
            },
            {
                'review': "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red. I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I buy the large?).",
                'category': categories,
                'output': ['Usage Scenarios and Applicability', 'Design and Appearance', 'Product Quality', 'Size and Fit', 'Washing and Maintenance']
            },
            { 
                'review': "Such a beautiful and well made dress.  This is my 1st time ordering from this brand.  Quality is excellent.  I ordered a size Small.  I am a 36C  and on the curvy side and fit was just right.  A bigger chest would not fit properly.  I can't wait to order more dresses from this brand.",
                'category': categories,
                'output': ['Product Quality', 'Size and Fit', 'Brand and Customer Service', 'Overall Satisfaction']
            },
            {
                'review': "Very clean product. The fabric, craftsmanship, and underneath slip are all thick and very well made. No cheap materials, no messy stitching, no misalignments. Looks and feels like a dress you could easily pay more money for, at a small chic boutique by the beach...",
                'category': categories,
                'output': ['Product Quality', 'Design and Appearance', 'Price and Value', 'Overall Satisfaction']
            },
            {
                'review': "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered.",
                'category': categories,
                'output': ['Product Quality', 'Size and Fit', 'Design and Appearance', 'Brand and Customer Service', 'Overall Satisfaction']
            }
        ]

        return classification_examples


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
        categories_str = ', '.join(predicted_categories)
        prompt = (
            f"For each of the following product reviews, analyze the sentiment (Positive, Negative, or Neutral) of the following product review for each of the following categories: {categories_str}.\n"
            "You do not need to repeat any part of the input. Just output the categories and their corresponding sentiments in the format:\n"
            "- Category: Sentiment\n"
            "\nPlease analyze only the categories provided and do not add or remove any categories."
        )
        
        if examples:
            prompt += f"\n\nHere are some examples:\n{examples}"
            # prompt += '\n\nHere are some examples:'

        
        prompt += (
            f"\n\nNow, analyze the sentiment for the following review and categories:\nReview: '{review}'"
            "\n\nPlease confirm before outputting: 'All specified categories provided have been analyzed and do not add or remove any categories.'"
            "\n\nOutput:"
        )
        
        
        return prompt
    
    def create_sentiment_prompt_v2(self, review, predicted_categories, examples=None):
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
            "For each of the following product reviews, analyze the sentiment (Positive, Negative, or Neutral) for the specific categories listed for that review. The categories may vary for each review. Do not add new categories or omit any provided categories.\n\n"
            "You do not need to repeat any part of the input. Just output the categories and their corresponding sentiments in the format:\n"
            "- Category: Sentiment"
            "\n\nIMPORTANT: Only analyze the sentiment of categories listed. Do not add new categories or omit any of the given categories."
        )
        
        if examples:
            prompt += "\n\nHere are some examples:"
            for idx, example in enumerate(examples, 1):
                prompt += f"\n\nExample {idx}:\nReview: \"{example['review']}\"\nCategories: {', '.join(example['categories'])}\nOutput:"
                for category, sentiment in example['output'].items():
                    prompt += f"\n- {category}: {sentiment}"
        
        prompt += f"\n\nNow, analyze the sentiment for the following review:\nReview: \"{review}\"\nCategories: {', '.join(predicted_categories)}\nOutput:"
        
        return prompt


    def sentiment_examples(self):
        
        examples = textwrap.dedent("""
        Example 1: 
        Review: "This is one of those rare Allegra dresses I have bought that fits perfectly and looks great. My only complaint is that the description states there is a self-tie sash, and the dress I received did not have a sash at all. I am still giving the product five stars because I think the price/quality ratio is excellent. I have ordered a number of Allegra items and returned most because they didn't fit properly. I've also received Allegra dresses with major quality control issues (kind of what you would expect at this price point) in the past. This particular dress is perfect, and I am very happy with it. Note: I am 5' 3", and the hem hits right at my knee."
        Output:
        - Size and Fit: Positive
        - Design and Appearance: Positive
        - Product Quality: Positive
        - Price and Value: Positive
        - Overall Satisfaction: Positive
        - Brand and Customer Service: Neutral

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
        - Size and Fit
        - Design and Appearance
        - Shipping and Packaging
        - Overall Satisfaction
                                   
        Example 4:
        Review: "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!"
        Output:
        - Size and Fit: Positive
        - Design and Appearance: Positive
        - Usage Scenarios and Applicability: Positive
        
        Example 5:
        Review: "Absolutely fell in love with this dress the first time I wore it.  If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress.  It did fit true to size and wasn't too short."
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
        Review: "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy."
        Output:
        - Usage Scenarios and Applicability: Positive
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
                                   
        Example 17:
        Review: "This dress has a cute top half but the layers on the skirt are cut weird and make your hips look big.  The small was a little loose but I wouldn’t size up.  Material is ok.  Doesn’t look like it will wrinkle at all.  Shorter in front and longer in back.  Love the print."                           
        Output:
        - Design and Appearance: Neutral
        - Size and Fit: Negative
        - Product Quality: Neutral
        - Overall Satisfaction: Neutral                           
                                   
        Example 18:
        Review: "I relied on several reviews when picking this dress so I thought I’d leave my own. It’s very cute on and comfy. I am 5’2” and about 128lbs. Almost always order a medium but I saw this runs big. It definitely does.  I ordered a small and ended up using small safety pins at the waist to cinch it in a bit. I could’ve gotten away with the extra small but I can make this work. I would’ve given it five stars except for how large it runs and it arrived with one of the bottoms missing on the right sleeve cuff. They send an extra so I can take care of this as well."
        Output:
        - Design and Appearance: Positive
        - Comfort: Positive
        - Size and Fit: Neutral
        - Shipping and Packaging: Negative
        - Brand and Customer Service: Neutral                                                   

        Example 19:
        Review: "I've purchased multiple items from the brand before and I've never had a problem with anything fitting before this dress. The dress was beautiful and i ordered based on the size chart but all big armed buyers should be wary because my arms did not fit and i had to return it unfortunately."
        Output:
        - Design and Appearance: Positive
        - Size and Fit: Negative
        - Overall Satisfaction: Negative
        - Brand and Customer Service: Neutral                           

        Example 20: 
        Review: "I am super happy with this purchase!! I was a little worried since the model seems to maybe imply the clothes will be junior sizes but I decided to trust the measurements provided by Allegra K because the dress is so pretty and I am glad I did! Im a large and am curvy and it fit so well and looked so cute! I really appreciate Allegra K because it seems usually these styles of clothes run really small but they have realistic sizes for all women and I'm such a fan!! Love everything about it. Thank you!"
        Output:                            
        - Size and Fit: Positive
        - Design and Appearance: Positive
        - Overall Satisfaction: Positive
        - Brand and Customer Service: Positive

        Example 21:
        Review: "Such a lovely color. Material is so soft and flowy. Bought this in medium and it fit slightly loose which was what I wanted. Wish it had an inner lining to it (which is why I'm giving it 4 stars) but other than that, it's such a pretty dress. Note that it was just a tad but more fitted at the chest for me but flowy everywhere else. For reference I'm 36 DD 5'4 and 140 lbs."
        Output:
        - Design and Appearance: Positive
        - Comfort: Positive
        - Size and Fit: Positive
        - Product Quality: Neutral
        - Overall Satisfaction: Positive
        """)
        return examples
    
    def sentiment_examples_v2(self):
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
                'categories': ['Design and Appearance', 'Shipping and Packaging', 'Overall Satisfaction'],
                'output': {  
                    'Design and Appearance': 'Positive',
                    'Shipping and Packaging': 'Positive',
                    'Overall Satisfaction': 'Positive'
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

