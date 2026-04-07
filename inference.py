import os
from openai import OpenAI
from env import StudyEnvironment

print("[START] LLM agent")

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME","gpt-3.5-turbo")

try:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY
    )
except Exception as e:
    print("Client init error:",e)
    client = None

env = StudyEnvironment("medium")

state = env.reset()

done = False
total_reward = 0
steps = 0

while not done:

    prompt = f"""
    You are an AI study planner.

    Energy: {state['energy']}
    Focus: {state['focus']}
    Progress: {state['progress']}
    Time: {state['time']}

    Actions:
    study
    rest
    scroll

    Return only one word.
    """

    action = "study"

    if client and API_BASE_URL and API_KEY:

        try:

            response = client.chat.completions.create(

                model=MODEL_NAME,

                messages=[
                    {"role":"user","content":prompt}
                ],

                temperature=0,

                max_tokens=10

            )

            action = response.choices[0].message.content.strip().lower()

            if action not in ["study","rest","scroll"]:
                action = "study"

        except Exception as e:

            print("LLM error:",e)

            action = "study"

    try:

        state,reward,done,score = env.step(action)

        total_reward += reward

        steps += 1

        print(f"[STEP] {steps} action={action} reward={round(reward,2)} score={round(score,2)}")

    except Exception as e:

        print("Environment error:",e)

        break

print("[END]")

try:

    print("final_score:",round(env.get_score(),2))

except:

    print("final_score: error")

print("total_reward:",round(total_reward,2))

print("steps:",steps)
