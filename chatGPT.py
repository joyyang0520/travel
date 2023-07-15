import openai

a_side = "sk-dbSdL9i73fTGBhZLMthxT3B"
b_side = "lbkFJ35dB0WkQReqkeADsmWc4"
openai.api_key = a_side + b_side

def reply(msg):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=100,
        temperature=0.5,
        messages=[
            {"role": "assistant", "content": "我是負責處理旅遊問題的AI，我會簡短回答你所問的問題。"},
            {"role": "user", "content":  msg}
        ]
    )
    remsg = response.choices[0].message.content
    
    if '。' or '.' in remsg:
        remsg = remsg.split('。')[0]
        
    # print(remsg)
    
    return remsg


# reply("台灣哪裡有熱氣球可以搭")

