import openai

a_side = "sk-AZ4lkfUPTEt5Bki2xv3KT3B"
b_side = "lbkFJo6pnsChgFziv0QeUjLGm"
openai.api_key = a_side + b_side

def reply(msg):

    remsg = 'chatGPT reply'

    return remsg
    '''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=60,
        temperature=0.5,
        messages=[
            {"role": "assistant", "content": "我是負責處理旅遊問題的AI，我會簡短回答你所問的問題。"},
            {"role": "user", "content":  msg}
        ]
    )
    remsg = response.choices[0].message.content
    
    if '。' or '.' in remsg:
        remsg = remsg.split('。')[0] 
    
    return remsg
'''