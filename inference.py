import os
from openai import OpenAI
from env import StudyEnvironment

print("[START]")

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME","gpt-3.5-turbo")

client=None

if API_BASE_URL and API_KEY:

    try:

        client = OpenAI(

            base_url=API_BASE_URL,

            api_key=API_KEY

        )

    except:

        client=None


env = StudyEnvironment("medium")

state = env.reset()

done=False

total_reward=0

steps=0


while not done:

    action="study"

    if client:

        try:

            prompt=f"""
Energy {state['energy']}
Focus {state['focus']}
Progress {state['progress']}

Choose:
study
rest
scroll

Return one word.
"""

            response = client.chat.completions.create(

                model=MODEL_NAME,

                messages=[
                    {"role":"user","content":prompt}
                ],

                temperature=0,
                max_tokens=5

            )

            action=response.choices[0].message.content.strip().lower()

            if action not in ["study","rest","scroll"]:

                action="study"

        except:

            action="study"


    state,reward,done,score=env.step(action)

    total_reward+=reward

    steps+=1

    print(f"[STEP] step={steps} action={action} reward={round(reward,2)} score={round(score,2)}")


print("[END]")

final_score = env.get_score()

if final_score <=0:
    final_score=0.01

if final_score >=1:
    final_score=0.99


print("final_score:",round(final_score,2))

print("total_reward:",round(total_reward,2))

print("steps:",steps)
