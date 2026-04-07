import os
from openai import OpenAI
from env import StudyEnvironment

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

    try:

        state,reward,done,score=env.step(action)

        total_reward+=reward

        steps+=1

    except:

        break


print("final_score:",round(env.get_score(),2))

print("total_reward:",round(total_reward,2))

print("steps:",steps)
