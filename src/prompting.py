
# 定义 Prompt 模板
def create_few_shot_prompt(review, embedding):
    prompt = f"""
    Review semantic embedding: {embedding}

    Classify the following product review into one or more of the following categories: ["Fabric", "Size", "Color", "Comfort", "Price", "Quality", "Shipping", "Service", "Packaging", "Overall Experience"], 
    and also analyze the sentiment (Positive, Negative, or Neutral) for each category that applies.

    例子1:
    Review: "这件衣服的面料非常舒适，价格有点贵"
    Category and Sentiment:
    - Fabric: Positive
    - Price: Negative

    例子2:
    Review: "这双鞋的颜色比图片上深一些，质量还不错"
    Category and Sentiment:
    - Color: Neutral
    - Quality: Positive

    例子3:
    Review: "物流太慢，包装也有破损"
    Category and Sentiment:
    - Shipping: Negative
    - Packaging: Negative

    例子4:
    Review: "这件衣服的面料舒适度还行，但是尺码偏小，服务态度很差"
    Category and Sentiment:
    - Fabric: Neutral
    - Size: Negative
    - Service: Negative

    Now classify the following review:
    Review: "{review}"
    """
    return prompt

