import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
)

# 推荐使用最新的模型名（旧名 deepseek-v4-flash 仍然可用）
MODEL = "deepseek-flash"

messages = []

print("简单连续对话程序（输入 exit / quit / 退出 结束）")
print("-" * 40)

while True:
    user_input = input("你: ").strip()

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit", "退出", "q"}:
        print("对话结束，再见！")
        break

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        assistant_message = response.choices[0].message
        messages.append(assistant_message)

        print(f"AI: {assistant_message.content}\n")

    except Exception as e:
        print(f"请求出错: {e}")
        # 出错时把刚才加进去的用户消息撤掉，避免历史污染
        messages.pop()