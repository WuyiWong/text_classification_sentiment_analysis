from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch


mode_path = 'D:/llm_data/unslothLlama-3.2-1B-Instruct'
tokenizer = AutoTokenizer.from_pretrained(mode_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(mode_path, device_map="gpu:0",torch_dtype=torch.bfloat16, trust_remote_code=True).eval()



review = '''I received this sweatshirt and the first thing I noticed was the color was not like the picture (I understand screens show different colors as well). After trying it on I decided I liked the color and the size fit well. It is warm and comfy. I will be wearing at work which is very cold.  '''
prompt = f"review is {review}, classify the  review and provide the categorys? Less than 4 categories "
content = '''
Classify the following product review into one or more of the following categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others.
You do not need to repeat any part of the input. Just output the categories that apply in the format
- Category

Here are some examples:

Example 1:
Review: "This is one of those rare Allegra dresses I have bought that fits perfectly and looks great. My only complaint is that the description states there is a self-tie sash, and the dress I received did not have a sash at all. I am still giving the product five stars because I think the price/quality ratio is excellent. I have ordered a number of Allegra items and returned most because they didn't fit properly. I've also received Allegra dresses with major quality control issues (kind of what you would expect at this price point) in the past. This particular dress is perfect, and I am very happy with it. Note: I am 5' 3", and the hem hits right at my knee."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Size and Fit
- Design and Appearance
- Product Quality
- Price and Value
- Overall Satisfaction
- Brand and Customer Service

Example 2:
Review: "This dress was pretty bulky and not so flowy looking like in the photos. I felt uncomfortable in it. Didn't wear it for long. Even with the tie backs it was just too big for me. Too much fabric."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Design and Appearance
- Comfort
- Size and Fit
- Overall Satisfaction

Example 3:
Review: "I had high hopes for this but unfortunately ended up having to return. It was very big and unflattering, kind of like a tent. I would say if you are between a L/XL definitely size down. The shipping was fast, but overall just did not like the dress."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Size and Fit
- Design and Appearance
- Shipping and Packaging
- Overall Satisfaction

Example 4:
Review: "This dress fits so well and is very flattering! I'm 5 foot 4 and weigh 125 lbs and bought a size small. It is a little on the longer size since I am shorter but it is still so cute and perfect for weddings, grad parties, etc!"
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Size and Fit
- Design and Appearance
- Usage Scenarios and Applicability

Example 5:
Review: "Absolutely fell in love with this dress the first time I wore it. If you are going to be a one and done person this dress is for you. But after the first wash the stitching came out and there is now a hole in the back of the dress. It did fit true to size and wasn't too short."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Design and Appearance
- Size and Fit
- Product Quality
- Washing and Maintenance

Example 6:
Review: "I got this because I thought it would be breast feeding friendly. It’s is amazing. Super easy to breast feed in, looks awesome with a denim jacket, and makes me look like I wasn’t even pregnant. I have it in four colors. Highly recommend ??"
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Usage Scenarios and Applicability
- Design and Appearance
- Overall Satisfaction

Example 7:
Review: "It's a great summer dress! It is light and flowy. It is true to size and comfortable! The material is polyester and it just didn't feel like great quality. I took a star off because material seems a little cheap but other than that it's a good buy."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Usage Scenarios and Applicability
- Size and Fit
- Comfort
- Product Quality
- Overall Satisfaction

Example 8:21`
Review: "The fabric of this product is good and not cheap! The wrinkles were expected because of it being packaged but that can be easily fixed. The color is exactly as pictured and the fit of it is great. I ordered a medium and I'm comfortable in it."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Shipping and Packaging
- Product Quality
- Design and Appearance
- Size and Fit
- Comfort

Example 9:
Review: "This dress is as described except for the neckline. It is a little bit higher than in the pictures. Other than that it’s exactly as I expected it to be. The material isn’t too thin and the length is perfect. The sleeve are pretty and the color is beautiful."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Design and Appearance
- Product Quality
- Color and Appearance
- Size and Fit

Example 10:
Review: "Dress was not the same pattern. It looked cheap. No tags whatsoever to know how to care for it. Ordered normal size and was small looking because of elastic in waist. Wasn't at all flowing like the style. Returning for sure."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Product Quality
- Size and Fit
- Washing and Maintenance
- Overall Satisfaction
- Design and Appearance

Example 11:
Review: "Washed it for the first time and there are strings and hems coming undone all over. Went to exchange or return it and apparently my window closed, such a bummer, it really is a cute dress!"
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Product Quality
- Washing and Maintenance
- Brand and Customer Service
- Design and Appearance

Example 12:
Review: "I had to have a red dress for a sorority red dress gala. Polka dot, but nevertheless red. I tried four amazon dresses, and this was the cutest and nicest material. It seems like it will wash well. The medium is very generous (or did I buy the large?)."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Usage Scenarios and Applicability
- Design and Appearance
- Product Quality
- Size and Fit
- Washing and Maintenance

Example 13:
Review: "This dress was sized at a 12 to 14, which should have been fine. Was too small, came all bunched up in a bag and wrinkled, the fabric is not very breathable and I did not care for the dress at all. Looks lovely in the picture, but I actually hated it."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Size and Fit
- Shipping and Packaging
- Product Quality
- Design and Appearance

Example 14:
Review: "Very clean product. The fabric, craftsmanship, and underneath slip are all thick and very well made. No cheap materials, no messy stitching, no misalignments. Looks and feels like a dress you could easily pay more money for, at a small chic boutique by the beach..."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Product Quality
- Design and Appearance
- Price and Value
- Overall Satisfaction

Example 15:
Review: "The material is Soft and flows well, no stretch but due to the style stretch is not really needed if you order the proper size. Fit as expected and the color slightly more teal than the picture shows. Merchant delivered what was advertised and I am happy that I ordered."
Categories: Usage Scenarios and Applicability, Price and Value, Shipping and Packaging, Design and Appearance, Product Quality, Size and Fit, Washing and Maintenance, Overall Satisfaction, Comfort, Brand and Customer Service, Others
Output:
- Size and Fit
- Color and Appearance
- Shipping and Packaging
- Brand and Customer Service
'''


messages = [
        {"role": "system", "content": content},
        {"role": "user", "content": prompt}
]

input_ids = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
model_inputs = tokenizer([input_ids], return_tensors="pt").to('cuda')
generated_ids = model.generate(model_inputs.input_ids,max_new_tokens=512)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]



print(response)





