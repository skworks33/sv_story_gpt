import os
import requests
import random
import openai

# 1. 環境変数からAPIキーとWebhook URLを取得
openai.api_key = os.environ["OPENAI_API_KEY"]
slack_webhook_url = os.environ["SLACK_WEBHOOK_URL"]

def ask_chatgpt(question):
    try:
        # 3. ChatGPTに質問を投げる
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "日本語で返答してください。"
                },
                {
                    "role": "user",
                    "content": f"{question}",
                },
            ],
        )
        

        # 4. 質問の結果を取得
        answer = response.choices[0]["message"]["content"].strip()
        print(answer)

        return answer

    except Exception as e:
        print(f"Error: {e}")
        return None

def post_to_slack(text):
    try:
        # 5. Slackへの投稿
        response = requests.post(
            slack_webhook_url,
            json={"text": text}
        )

        if response.status_code != 200:
            raise ValueError(f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":

    filename = "sv.txt"

    # スクリプトのあるディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # カレントディレクトリを変更
    os.chdir(script_dir)

    # 空のリストを用意
    data_list = []

    # ファイルを開いて、内容を1行ずつ読み込む
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            # 改行文字を削除してリストに追加
            data_list.append(line.strip())

    # リストからランダムに1つ選択
    selected_item = random.choice(data_list)

    # 質問を設定
    question = f"あなたはプロの作家です。以下の入力文はある企業が培ってきたマインドの中の１つです。制約条件を元に文章を作成してください。\n\n制約条件: ###\n* '入力文(マインド)'に関連した興味深い話題を500文字以内で作成してください。\n* 禁止用語は一切使わないでください。\n###\n\n入力文(マインド): ###\n{selected_item}\n###\n\n禁止用語: ###\n社訓\n社員\n買収\n本社\n###"

    # ChatGPTに質問し、結果を取得
    answer = ask_chatgpt(question)

    if answer:
        # 結果をSlackに投稿
        slack_message = f"おはようございます。\n本日のフレーズは「{selected_item}」です。\n\n{answer}"
        post_to_slack(slack_message)
    else:
        print("Failed to get an answer from ChatGPT.")

