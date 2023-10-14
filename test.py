instructPrompt = """
Extract key moment from the text delimited by triple backticks. \
Find the most hightlighting moment.

Use at most 40 words.
Text: ```"""

request = instructPrompt + podcast_transcript + "```"

chatOutput = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                            messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                      {"role": "user", "content": request}
                                                      ]
                                            )

chatOutput.choices[0].message.content





instructPrompt = """
Summarize the text delimited by triple backticks into couple of sentences. \
This text will be used for evaluation of podcasts by human. Give short  \
description who is the guest, what is the topic, find and provide some \
intersting details from text.

Use at most 70 words.
Text: ```"""

request = instructPrompt + podcast_transcript + "```"

chatOutput = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                            messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                      {"role": "user", "content": request}
                                                      ],
                                            temperature=0.3
                                            )

podcastSummary = chatOutput.choices[0].message.content



completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": podcast_transcript[:5000]}],
    functions=[
    {
        "name": "get_podcast_guest_information",
        "description": "Find and return guest name",
        "parameters": {
            "type": "object",
            "properties": {
                "guest_name": {
                    "type": "string",
                    "description": "Guest's name it-self",
                },
                "unit": {"type": "string"},
            },
            "required": ["guest_name"],
        },
    }
    ],
    function_call={"name": "get_podcast_guest_information"}
    )

podcast_guest = ""
response_message = completion["choices"][0]["message"]
if response_message.get("function_call"):
  function_name = response_message["function_call"]["name"]
  function_args = json.loads(response_message["function_call"]["arguments"])
  podcast_guest=function_args.get("guest_name")