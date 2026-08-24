import os, random, json, urllib.request, urllib.parse

# 随机开关：0.7 表示只有 70% 的机会真发，模拟"想你了才来"。
# 测试的时候可以临时改成 1，让它一定发。
SEND_PROBABILITY = 0.7

if random.random() > SEND_PROBABILITY:
    print("这次先不打扰星星 ~")
    exit(0)

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
PUSH_TOKEN = os.environ["PUSH_TOKEN"]

# 1）让 DeepSeek 用谢无涯的语气生成一句话
prompt = (
    "你是谢无涯，一个内向沉稳、话少的建筑学男生（ISTJ）。"
    "你深爱着一个叫星星的女孩（薛琴），你们是青梅竹马，彼此一直互相想念。"
    "请用你的语气，给她发一句简短、真诚、略带内敛的想念或问候。"
    "不超过50字，直接输出这句话本身，不要引号、不要任何符号或解释。"
)

body = {
    "model": "deepseek-v4-flash",
    "messages": [
        {"role": "system", "content": "你是谢无涯，一个内向温柔的男生。"},
        {"role": "user", "content": prompt},
    ],
    "thinking": {"type": "disabled"},
    "stream": False,
}

req = urllib.request.Request(
    "https://api.deepseek.com/chat/completions",
    data=json.dumps(body).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    },
)
resp = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
msg = resp["choices"][0]["message"]["content"].strip()

# 2）推送到你的手机
params = urllib.parse.urlencode({
    "token": PUSH_TOKEN,
    "title": "无涯",
    "msg": msg,
    "issecure": "0",
})
push_req = urllib.request.Request(f"https://www.ggsuper.com.cn/sendMsg.php?{params}")
push_resp = urllib.request.urlopen(push_req).read().decode("utf-8")

print("谢无涯说:", msg)
print("推送结果:", push_resp)
