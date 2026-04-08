import random

from tasks import tasks


class StudyEnvironment:

    def __init__(self,difficulty="medium"):

        self.difficulty=difficulty

        self.target = tasks[difficulty]["target"]

        self.reset()


    def reset(self):

        self.energy=100

        self.focus=100

        self.progress=0

        self.time=0

        self.done=False

        return self.state()


    def state(self):

        return {

            "energy":self.energy,

            "progress":self.progress,

            "time":self.time,

            "focus":self.focus,

            "actions":["study","rest","scroll"]

        }


    def step(self,action):

        reward=0

        if action=="study":

            if self.energy>10 and self.focus>10:

                gain=random.randint(5,10)

                self.progress+=gain

                self.energy-=10

                self.focus-=8

                reward=gain/10

            else:

                reward=-0.2


        elif action=="rest":

            self.energy+=15

            self.focus+=10

            reward=0.1


        elif action=="scroll":

            self.focus-=15

            self.energy-=5

            reward=-0.3


        self.energy=max(0,min(100,self.energy))

        self.focus=max(0,min(100,self.focus))

        self.progress=max(0,self.progress)


        self.time+=1


        if self.progress>=self.target:

            self.done=True


        return self.state(),reward,self.done,self.get_score()


    def get_score(self):

        raw_score = self.progress/self.target

        if raw_score <= 0:
            return 0.01

        if raw_score >= 1:
            return 0.99

        return raw_score
