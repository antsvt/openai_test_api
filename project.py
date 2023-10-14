import openai
import pandas as pd

API_KEY = "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"
file = "./data/reviews_5_balanced.json.gz"

df = pd.read_json(file, lines=True)
df = df.drop(columns=['reviewTime','unixReviewTime'])
df = df.rename(columns={'reviewText': 'text'})

df['sentiment'] = 'OTHER'
df.loc[df['overall'] > 3, 'sentiment'] = 'POSITIVE'
df.loc[df['overall'] < 3, 'sentiment'] = 'NEGATIVE'

# Removing unecessary columns to keep a simple dataframe
df.drop(columns=['overall', 'reviewerID', 'summary'],
        inplace=True)

print(df.sample(5))

review_number= 4
review_text = df['text'].iloc[review_number]
print (review_text)

instructPrompt = f"""
You will be provided with a customer review of a product on an online e-commerce website. You have to understand the context of the review
and classify the sentiment into three categories - POSITIVE or NEGATIVE or OTHER.
POSITIVE - this category indicates that the user was happy with the product and liked it
NEGATIVE - this category indicates that the user was unhappy with the product and did not like it
OTHER - please output this category if you cannot tell what the review is

Only provide the determined category and nothing else. I don't want any explanations.

Review Text: {review_text}

Sentiment:
"""

print (instructPrompt)

openai.api_key = API_KEY
chatOutput = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                      {"role": "user", "content": instructPrompt}
                                                      ]
                                          )

print(chatOutput.choices[0].message.content)
print(df['sentiment'].iloc[review_number])