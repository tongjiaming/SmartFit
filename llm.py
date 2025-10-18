from dotenv import load_dotenv
import requests
import os
import json


def model_proxy(model, txt):
    load_dotenv()
    if model == "claude-opus-4-1-20250805-thinking":
        api_key = os.getenv("MODEL_PROXY_KEY_1")
    elif model == "gpt-5":
        api_key = os.getenv("MODEL_PROXY_KEY_2")
    else:
        raise

    for i in range(3):
        try:
            url = "https://models-proxy.stepfun-inc.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            messages = [{"role":"user", "content": txt}]

            data = {
                "model": model,
                "max_tokens": 20000,
                "messages": messages
            }

            response = requests.post(url, headers=headers, json=data)
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(e)
    return ""


def set_goal(age, gender, weight, height, activity, goal_time, goal_weight):
    for i in range(3):
        try:
            prompt = f'''
                我性别{gender}，今年{age}岁，身高{height}cm，体重{weight}kg，日常生活习惯为{activity}，希望在{goal_time}周内将体重减至{goal_weight}kg。
                请生成：
                    我的每日基础代谢，单位kcal，只生成数字
                    为了达成我的减肥目标，每日所需热量缺口，单位kcal，只生成数字
                    基于我的目标，你的建议，文字报告，不少于100字
                将以上结果放入一个JSON对象中，不要输出markdown格式，示例
                {{
                    "base_consumption": 1800,
                    "target_deficit": 500,
                    "report": "基于你的情况..."
                }}
            '''
            res = model_proxy("claude-opus-4-1-20250805-thinking", prompt)
            print(res)
            json_obj = json.loads(res)
            return json_obj["base_consumption"], json_obj["target_deficit"], json_obj["report"]
        except Exception as e:
            print(e)
            pass
    return "", "", "获取模型结果失败，请重试"


def set_goal_demo(age, gender, weight, height, activity, goal_time, goal_weight):
    return 1643, 229, "基于你的情况，你的基础代谢率约为1643千卡，考虑久坐生活方式，每日总消耗约1970千卡。要在24周内减重5公斤是一个合理且健康的目标，每日只需229千卡的热量缺口即可实现。建议你每日摄入约1740千卡，配合适度运动如每天快走30分钟或做些简单的力量训练。注意蛋白质摄入充足（每公斤体重1.2-1.5克），多吃蔬菜水果，避免极端节食。定期监测体重变化，根据实际情况调整饮食计划。"


if __name__ == "__main__":
    print(set_goal("25", "男", "80", "175", "久坐", "8", "70"))