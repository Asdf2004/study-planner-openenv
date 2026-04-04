from tasks import tasks
import random

class StudyEnvironment:

    def __init__(self,difficulty="medium"):

        self.max_energy = 100

        self.target = tasks[difficulty]["target"]

        self.actions=["study","rest","scroll"]

        self.reset()


    def reset(self):

        self.energy=100

        self.progress=0

        self.time=0

        self.focus=50

        self.history=[]

        return self.state()


    def state(self):

        return{

            "energy":self.energy,

            "progress":round(self.progress,2),

            "time":self.time,

            "focus":self.focus,

            "actions":self.actions

        }


    def step(self,action):

        reward=0

        if action=="study":

            self.progress+=10 + self.focus*0.05

            self.focus-=2

            self.energy-=10

            reward=1


        elif action=="rest":

            self.energy+=15

            self.focus+=3

            reward=0.5


        elif action=="scroll":

            self.energy-=5

            reward=-1


        else:

            reward=-2


        if random.random()<0.1:

            self.energy-=5

            reward-=0.5


        self.energy=max(0,min(100,self.energy))

        self.focus=max(0,min(100,self.focus))

        self.progress=max(0,min(self.target,self.progress))

        self.time+=1


        done=False


        if self.progress>=self.target:

            done=True

            reward+=5


        if self.energy<=0:

            done=True

            reward-=2


        score=min(1.0,self.progress/self.target)


        return self.state(),reward,done,score


    def get_score(self):

        return min(1.0,self.progress/self.target)