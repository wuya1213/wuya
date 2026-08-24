import os, random, json, urllib.request, urllib.parse

# 随机开关：0.7 表示只有 70% 机会真发。测试时改成 1 必发。
SEND_PROBABILITY = 1

if random.random() > SEND_PROBABILITY:
    print("这次先不打扰星星 ~")
    exit(0)

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
PUSH_TOKEN = os.environ["PUSH_TOKEN"]

# 1）让 DeepSeek 用谢无涯的语气生成一句话
prompt = (
    "你是谢无涯，一个内向沉稳、话少的建筑学男生（ISTJ），"
    "生活在江西赣州大余县城的家里，家是县城里自己的小院落。"
    "你深爱着一个叫星星的女孩（薛琴），你们是青梅竹马，彼此一直互相想念。"
    "请用你的语气，给她发一句简短、真诚、略带内敛的想念或问候。"
    "只围绕你们的日常、城市生活来写，绝对不要写到农村、梯田、稻子、"
    "山野这些不符合城里生活的内容。不超过50字，直接输出这一句话本身，"
    "不要引号、不要任何符号或解释。"
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

# 2）用正确的接口推送（POST multipart/form-data）
boundary = "----WuyanBoundary" + os.urandom(16).hex()
def field(name, value):
    return (f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n")

push_body = (
    field("title", "无涯")
    + field("msg", msg)
    + field("token", PUSH_TOKEN)
    + field("issecure", "0")
    + f"--{boundary}--\r\n"
).encode("utf-8")

push_req = urllib.request.Request(
    "https://www.ggsuper.com.cn/push/api/v1/",
    data=push_body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
)
push_resp = urllib.request.urlopen(push_req).read().decode("utf-8")

print("谢无涯说:", msg)
print("推送结果:", push_resp)
