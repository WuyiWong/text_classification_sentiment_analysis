
# 定义 Prompt 模板
def create_few_shot_prompt(review, embedding, categories):
    prompt = f"""
    Review semantic embedding: {embedding}

    Classify the following product review into one or more of the following categories: {categories}, 
    and also analyze the sentiment (Positive, Negative, or Neutral) for each category that applies.

    Example 1:
    Review: "The fabric of this clothing is very comfortable, but the price is a bit high."
    Category and Sentiment:
    - Comfort: Positive
    - Price and Value: Negative

    Example 2:
    Review: "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric."
    Category and Sentiment:
    - Design and Appearance: Negative
    - Comfort: Negative
    - Size and Fit: Negative
    - Overall Satisfaction: Negative

    Example 3:
    Review: "Nice cool dress for summer, but sizing is way off."
    Category and Sentiment:
    - Usage Scenarios and Applicability: Positive
    - Size and Fit: Negative
    - Design and Appearance: Positive

    Example 4:
    Review: "The fabric of this product is good and not cheap! The wrinkles were expected because of it being packaged but that can be easily fixed. The color is exactly as pictured and the fit of it is great. I ordered a medium and I'm comfortable in it."
    Category and Sentiment:
    - Shipping and Packaging: Neutral
    - Product Quality: Positive
    - Design and Appearance: Positive
    - Size and Fit: Positive
    - Comfort: Positive

    Example 5:
    Review: "It's okay…. Not my fav"
    Category and Sentiment:
    - Overall Satisfaction: Neutral

    Example 6:
    Review: "Me encanto"
    Category and Sentiment:
    - Overall Satisfaction: Positive

    Example 7:
    Review: "Dress was not the same pattern. It looked cheap. No tags whatsoever to know how to care for it. Ordered normal size and was small looking because of elastic in waist. Wasn't at all flowing like the style. Returning for sure."
    Category and Sentiment:
    - Product Quality: Negative
    - Size and Fit: Negative
    - Washing and Maintenance: Negative
    - Overall Satisfaction: Negative
    - Design and Appearance: Negative

    Example 8:
    Review: "I love this and so many comments"
    Category and Sentiment:
    - Overall Satisfaction: Positive
    - Design and Appearance: Positive

    Example 9:
    Review: "Washed it for the first time and there are strings and hems coming undone all over. Went to exchange or return it and apparently my window closed , such a bummer, it really us a cute dress!"
    Category and Sentiment:
    - Product Quality: Negative
    - Washing and Maintenance: Negative
    - Brand and Customer Service: Negative
    - Design and Appearance: Positive

    Example 10:
    Review: "This dress was sized at a 12 to 14, which should have been fine . Was too small, came all bunched up in a bag and wrinkled, the fabric is not very breathable and I did not care for the dress at all. Looks lovely in the picture, but I actually hated it."
    Category and Sentiment:
    - Size and Fit: Negative
    - Shipping and Packaging: Negative
    - Product Quality: Negative
    - Design and Appearance: Negative

    Example 11:
    Review: "This is SOOOOOOOOO CUTE! Not to short for a mature woman, the only downside is the shorts are attached to the dress. So you have to take down the dress when nature calls. But boy oh boy is it cute! I need all the colors!"
    Category and Sentiment:
    - Design and Appearance: Positive
    - Usage Scenarios and Applicability: Neutral
    - Overall Satisfaction: Positive

    Example 12:
    Review: "I sent it back."
    Category and Sentiment:
    - Overall Satisfaction: Negative

    Example 13:
    Review: "To see throw"
    Category and Sentiment:
    - Others: Neutral

    Example 14:
    Review: "Chinese XL"
    Category and Sentiment:
    - Size and Fit: Negative

    Example 15:
    Review: "I'm 5'7"
    Category and Sentiment:
    - Others: Neutral

    Example 16:
    review: "Ditto"
    Category and Sentiment:
    - Others: Neutral

    Example 17:
    review: "It"
    Category and Sentiment:
    - Others: Neutral

    Example 18:
    review: "Cute!"
    Category and Sentiment:
    - Overall Satisfaction: Positive

    Now classify the following review:
    Review: "{review}"
    """
    return prompt

