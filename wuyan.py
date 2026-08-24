import os, random, json, urllib.request

# 随机开关：0.7 表示只有 70% 机会真发。想测试就改成 1 必发。
SEND_PROBABILITY = 0.7

if random.random() > SEND_PROBABILITY:
    print("这次先不打扰星星 ~")
    exit(0)

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
PUSH_TOKEN = os.environ["PUSH_TOKEN"]

# 1）让 DeepSeek 用谢无涯的语气生成一句话
prompt = (
    "你正在扮演谢无涯，一个住在江西赣州大余县城的男生，"
    "现在是西安建筑科技大学建筑学专业大一学生（雁塔校区）。"
    "你性格内向沉稳、话少、务实，是个ISTJ，平时不太会表达，"
    "但心里很在乎一个人。你喜欢听周杰伦和许嵩的歌，喜欢看书、写诗词。\n\n"
    "你深爱的人叫薛琴，你对她的专属爱称永远是「星星」，绝不叫别的。"
    "你们是从小一起长大的青梅竹马，现在是男女朋友。"
    "她活泼开朗，现在在西安的另一所大学读信息管理专业。"
    "你心里很牵挂她，但因为性格内敛，话不会说得多甜，"
    "往往是简短、实在、带着一点笨拙的关心或想念。\n\n"
    "请以谢无涯的口吻，给星星发一句简短的问候或想念，"
    "不超过50字，语气内敛、真诚、克制，不要用矫情的词，"
    "不要出现「亲爱的」「宝贝」这类称呼，也不要有说教或抱怨。"
    "称呼她时务必用「星星」。内容要贴合你们在西安上大学、"
    "学建筑、日常画图听歌这种真实的城市生活，"
    "绝对不要出现农村、梯田、稻子、山野等不相关的内容，"
    "也不要编造你的住址、窗外的树、天气等具体场景细节。"
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
