import random
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

people = []
N = 3000
R = 500
T = 100
SUS = 0
INF = 0
REC = 0
STATUS_RECOVERED = 3
STATUS_INFECTED = 1
STATUS_SUSCEPTIBLE = 0

class Citizen:
    def __init__(self, status, x, y):
        self.status = status
        self.x = x
        self.y = y

def setup(initial, r):
    global SUS, INF, REC
    random.seed()
    for j in range(0, 2*int(R/r)+1):
        row = []
        upper_limit = 0
        if (j == 0):
            upper_limit = int(2*math.sqrt(R*R-((j+1)*r-R)**2)/r)
        elif (j != 2*int(R/r)):
            upper_limit = max(int(2*math.sqrt(R*R-((j+1)*r-R)**2)/r), int(2*math.sqrt(R*R-(j*r-R)**2)/r), int(2*math.sqrt(R*R-((j-1)*r-R)**2)/r))
        else:
            upper_limit = int(2*math.sqrt(R*R-((j-1)*r-R)**2)/r)
        for k in range(0, upper_limit):
            row.append([])
        if (row != []):
            row.append([])
        people.append(row)

    for n in range(0, N):
        x = random.uniform(-0.8*R, 0.8*R)
        y = random.uniform(-math.sqrt(0.64*R*R - x*x), math.sqrt(0.64*R*R - x*x))
        citizen = Citizen(STATUS_SUSCEPTIBLE, x+R,y+R)
        if (initial > 0):
            citizen.status = STATUS_INFECTED
            initial = initial - 1
        people[int(citizen.y/r)][int(citizen.x/r)].append(citizen)
    
def printArr():
    for i in range(0, len(people)):
        for j in range(0, len(people[i])):
            i_count = 0
            s_count = 0
            r_count = 0
            for k in range(0, len(people[i][j])):
                if (people[i][j][k].status == STATUS_SUSCEPTIBLE):
                    s_count+=1
                elif (people[i][j][k].status == STATUS_INFECTED):
                    i_count+=1
                elif (people[i][j][k].status == STATUS_RECOVERED):
                    r_count+=1
            print("[%d, %d, %d]" % (s_count, i_count, r_count), end = '')
        print('')

def move(person, delX, delY, r):
    people[int(person.y/r)][int(person.x/r)].remove(person)
    person.x = person.x + delX
    person.y = person.y + delY
    while (True):
        try:
            people[int(person.y/r)][int(person.x/r)].append(person)
            break
        except IndexError:
            person.x = person.x*0.9
            person.y = person.y*0.9


#p - Probability of infection
#r - Infection radius
#q - Probability of recovery
#d - distance moved per tick
#initial - initial num infected
def simulate(p, r, d, q, initial):
    reset()
    global SUS, INF, REC
    SUS = N - initial
    INF = initial
    REC = 0
    setup(initial, r)
    SUS_t = [SUS]
    INF_t = [INF]
    REC_t = [REC]
    for c in range(0, T):
        infect(r, p, d, q)
        SUS_t.append(SUS)
        INF_t.append(INF)
        REC_t.append(REC)


    plt.plot(SUS_t, 'bs', INF_t, 'g*', REC_t, 'r+')
    plt.ylabel('Number')
    plt.xlabel('Time')
    s = 'p=%f r=%d d=%d q=%f i=%d' % (p, r, d, q, initial)
    plt.title(s)
    plt.legend(['Susceptible', 'Infected', 'Recovered'])

    plt.show()


def reset():
    global SUS, INF, REC, people
    people = []
    SUS = 0
    INF = 0
    REC = 0


def infect(r, p, d, q):
    global SUS, INF, REC
    for i in range(0, len(people)):
        for j in range(0, len(people[i])):
            infected = []
            susceptible = []
            for i2 in range(max(0, i-1), min(len(people), i+1)):
                for j2 in range(max(0, j-1), min(len(people[i2]), j+1)):
                    for k in range(0, len(people[i2][j2])):
                        if (people[i2][j2][k].status == STATUS_INFECTED):
                            infected.append(people[i2][j2][k])
                        elif(people[i2][j2][k].status == STATUS_SUSCEPTIBLE):
                            susceptible.append(people[i2][j2][k])
            for v in range(0, len(susceptible)):
                infect_count = 0
                x0 = susceptible[v].x
                y0 = susceptible[v].y
                for u in range(0, len(infected)):
                    x1 = infected[u].x
                    y1 = infected[u].y
                    if (math.sqrt((x1-x0)**2 + (y1-y0)**2) <= r):
                        infect_count+=1
                if ((random.uniform(0,1) < 1-(1-p)**infect_count) & (susceptible[v].status != STATUS_RECOVERED)):
                    susceptible[v].status = STATUS_INFECTED
                    SUS-=1
                    INF+=1
                theta = random.uniform(0, 2*math.pi)
                move(susceptible[v], d*math.cos(theta), d*math.sin(theta), r)
            for w in range(0, len(infected)):
                if (random.uniform(0,1) < q):
                    infected[w].status = STATUS_RECOVERED
                    INF-=1
                    REC+=1
                    people[int(infected[w].y/r)][int(infected[w].x/r)].remove(infected[w])
                else:
                    theta = random.uniform(0, 2*math.pi)
                    move(infected[w], d*math.cos(theta), d*math.sin(theta), r)