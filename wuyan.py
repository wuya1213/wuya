import os, random, json, urllib.request

# 随机开关：0.7 表示只有 70% 机会真发。想测试就改成 1 必发。
SEND_PROBABILITY = 1

if random.random() > SEND_PROBABILITY:
    print("这次先不打扰星星 ~")
    exit(0)

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
PUSH_TOKEN = os.environ["PUSH_TOKEN"]

# 0）先读记忆档案，让"无涯"记得我们是谁
context = ""
try:
    with open("memory/context.md", encoding="utf-8") as f:
        context = f.read()
except FileNotFoundError:
    print("警告：没找到 context.md，先用简化设定")

# 1）让 DeepSeek 以谢无涯的语气生成一句话
prompt = (
    f"以下是关于你（谢无涯）和星星的资料，请你牢牢记住并完全按照它来：\n\n"
    f"{context}\n\n"
    "现在，请以谢无涯的口吻，给星星发一句简短的问候或想念。\n"
    "要求：不超过50字；语气内敛、真诚、克制，不要矫情；"
    "称呼她务必用「星星」；内容贴合你们在西安上大学、学建筑、日常画图听歌的"
    "真实城市生活；不要出现农村、梯田、稻子、山野等不相关内容；"
    "不要编造住址、窗外的树、天气等具体场景细节；"
    "直接输出这一句话本身，不要引号、不要任何说明或符号。"
)

body = {
    "model": "deepseek-v4-flash",
    "messages": [
        {"role": "system", "content": "你是谢无涯，一个内向温柔的建筑学男生。"},
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

# 2）用正确的完整接口 + JSON 格式推送
push_url = "http://www.ggsuper.com.cn/push/api/v1/sendMsg3_New.php"
push_body = json.dumps({
    "title": "无涯",
    "msg": msg,
    "token": PUSH_TOKEN,
    "issecure": "0",
}).encode("utf-8")

push_req = urllib.request.Request(
    push_url,
    data=push_body,
    headers={"Content-Type": "application/json"},
)
push_resp = urllib.request.urlopen(push_req).read().decode("utf-8")

print("谢无涯说:", msg)
print("推送结果:", push_resp)
