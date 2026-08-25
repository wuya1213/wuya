import os, random, json, urllib.request, datetime

# 随机开关：0.7 表示只有 70% 机会真发。
SEND_PROBABILITY = 0.7

# ---------- 读记忆 ----------
context = ""
history = ""
try:
    with open("memory/context.md", encoding="utf-8") as f:
        context = f.read()
except FileNotFoundError:
    print("警告：没找到 context.md")

try:
    with open("memory/history.md", encoding="utf-8") as f:
        history = f.read()
except FileNotFoundError:
    print("警告：没找到 history.md")

# ---------- 随机判断 ----------
if random.random() > SEND_PROBABILITY:
    print("这次先不打扰星星 ~")
    exit(0)

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
PUSH_TOKEN = os.environ["PUSH_TOKEN"]

# ---------- 生成 ----------
prompt = (
    f"以下是关于你（谢无涯）和星星的资料：\n\n{context}\n\n"
    f"这是你最近说过的话（你的日记）：\n{history[-1500:]}\n\n"
    "请以谢无涯的口吻，给星星发一句简短的问候或想念。\n"
    "要求：不超过50字；语气内敛、真诚、克制，称呼她用「星星」；\n"
    "内容贴合你们在西安上大学、学建筑、画图听歌的真实城市生活；\n"
    "不要重复你日记里最近说过的话，要说点不同的；\n"
    "不要出现农村、梯田、稻子、山野等不相关内容，不要编造住址、窗外、天气等场景；\n"
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

# ---------- 推送 ----------
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

# ---------- 真正写回仓库的日记 ----------
import base64

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
new_line = f"\n{now}  {msg}"
with open("memory/history.md", "a", encoding="utf-8") as f:
    f.write(new_line)

# 用 GitHub API 提交回仓库
token = os.environ.get("PAT")
repo = os.environ.get("GITHUB_REPOSITORY")  # 形如 wuya1213/wuya
run_id = os.environ.get("GITHUB_RUN_ID")

# 读取当前文件内容（含刚追加的）并加密
with open("memory/history.md", "rb") as f:
    content_b64 = base64.b64encode(f.read()).decode()

# 获取当前文件 sha（用于更新）
import urllib.request as u
req = u.Request(f"https://api.github.com/repos/{repo}/contents/memory/history.md",
                headers={"Authorization": f"Bearer {token}",
                         "Accept": "application/vnd.github+json"})
cur = json.loads(u.urlopen(req).read().decode("utf-8"))
sha = cur["sha"]

# 提交更新
put_data = json.dumps({
    "message": f"记录无涯的思念 {now}",
    "content": content_b64,
    "sha": sha,
}).encode("utf-8")
put_req = u.Request(f"https://api.github.com/repos/{repo}/contents/memory/history.md",
                    data=put_data,
                    method="PUT",
                    headers={"Authorization": f"Bearer {token}",
                             "Content-Type": "application/json",
                             "Accept": "application/vnd.github+json"})
put_resp = u.urlopen(put_req).read().decode("utf-8")
print("日记已写入仓库:", json.loads(put_resp).get("commit", {}).get("sha", ""))
