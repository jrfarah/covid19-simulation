#------------- imports -------------#
import matplotlib.pyplot as plt  
import numpy as np 
import os
from progress.bar import Bar
import copy


## class begins ##
class Particle():

    def __init__(self, x, y, xprime, yprime, color='blue', infected=False, quarantine=False):


        ## position attributes ##

        self.xpos = x
        self.ypos = y

        ## velocity attributes ##

        self.xvel = xprime
        self.yvel = yprime

        ## color attributes ##
        self.color = color

        ## infection attributes ##
        self.infected = infected
        self.recovered = False
        self.infectionTime = 99999
        self.infectionLength = 15
        self.quarantine = quarantine


    def printParticle(self):

        print ("[self.xpos: {0}]".format(self.xpos))
        print ("[self.ypos: {0}]".format(self.ypos))
        print ("[self.xvel: {0}]".format(self.xvel))
        print ("[self.yvel: {0}]".format(self.yvel))
        print ("[self.color: {0}]".format(self.color))

## class ends ##


## evolution function begins ##
def evolve(particles, simTime=0):

    for p, particle in enumerate(particles):

        (x, y) = copy.copy(particle.xpos), copy.copy(particle.ypos)


        if (simTime - particle.infectionTime) >= 15:
            particle.infected = False
            particle.recovered = True 
            particle.color = 'blue'


        ## interaction force ##
        for p2, particle2 in enumerate(particles[p+1:]):

            particle, particles[p+1+p2] = collisionForce(particle, particle2, simTime=simTime)

        ## force of gravity ##
        # particle = force(particle, yacc=-0.4)

        if not particle.quarantine: 
            newX = particle.xpos + particle.xvel
            newY = particle.ypos + particle.yvel

            particle.xpos = newX
            particle.ypos = newY

            particle = wallForce(particle)

        elif particle.quarantine:
            particle.xpos = x 
            particle.ypos = y

        particles[p] = particle

    return particles

## evolution function ends ##

## force function begins ##
def force(particle, xacc=0, yacc=0):

    newVelX = particle.xvel + xacc
    newVelY = particle.yvel + yacc

    particle.xvel = newVelX
    particle.yvel = newVelY

    return particle



def interactionForce(particle1, particle2, k=1./9.):
    
    distance = ((particle1.xpos - particle2.xpos)**2. + (particle1.ypos-particle2.ypos)**2.)**0.5   
    
    acceleration = k / (distance**2.) 
    angle21 = np.arctan2(particle1.ypos-particle2.ypos, particle1.xpos - particle2.xpos)
    angle12 = np.arctan2(particle2.ypos-particle1.ypos, particle2.xpos - particle1.xpos)

    xacc = acceleration*np.cos(angle21)
    yacc = acceleration*np.sin(angle21)

    particle1.xvel += xacc
    particle1.yvel += yacc

    xacc = acceleration*np.cos(angle12)
    yacc = acceleration*np.sin(angle12)

    particle2.xvel += xacc
    particle2.yvel += yacc

    return particle1, particle2


def calculateCollisionVelocities(v1, v2):

    if v1 == 0:
        return 0., -v2
    if v2 == 0:
        return -v1, 0.

    v2p = (v1 + v2 + np.sqrt(v1**2. + v2**2. - 2*v1*v2)) / 2.
    v2m = (v1 + v2 - np.sqrt(v1**2. + v2**2. - 2*v1*v2)) / 2.

    if v2p/abs(v2p) != v2/abs(v2):
        v2f = v2p
    else:
        v2f = v2m

    v1f = v1 + v2 - v2f

    return v1f, v2f

def collisionForce(particle1, particle2, simTime=0):

    distance = ((particle1.xpos - particle2.xpos)**2. + (particle1.ypos-particle2.ypos)**2.)**0.5

    if distance > 0.3:
        return particle1, particle2

    ## calculate the new x velocities ##
    newx1, newx2 = calculateCollisionVelocities(particle1.xvel, particle2.xvel)

    particle1.xvel = newx1
    particle2.xvel = newx2

    ## calculate the new x velocities ##
    newy1, newy2 = calculateCollisionVelocities(particle1.yvel, particle2.yvel)

    particle1.yvel = newy1
    particle2.yvel = newy2

    if particle1.infected is True:
        if particle2.recovered is False:
            particle2.infected = True
            particle2.infectionTime = simTime
            particle2.color = 'red'

    if particle2.infected is True:
        if particle1.recovered is False:
            particle1.infected = True
            particle1.infectionTime = simTime
            particle1.color = 'red'

    return particle1, particle2



def wallForce(particle):

    distanceToLeftWall = particle.xpos
    distanceToRightWall = 10 - particle.xpos

    distanceToFloor = particle.ypos
    distanceToCeiling = 10 - particle.ypos

    if distanceToFloor < 0.01 or distanceToCeiling < 0.01:
        particle.yvel *= -1

    if distanceToLeftWall < 0.01 or distanceToRightWall < 0.01:
        particle.xvel *= -1

    if particle.xpos < 0:
        particle.xpos = 0.02

    if particle.xpos > 10:
        particle.xpos = 9.98

    if particle.ypos < 0:
        particle.ypos = 0.02

    if particle.ypos > 10:
        particle.ypos = 9.98


    return particle 


## force function ends ##

## plot function begins ##
def plotParticles(particles, t=0):

    healthies = []
    infecteds = []
    recovereds = []
    for particle in particles:

        ## show particle ##
        plt.scatter(particle.xpos, particle.ypos, c=particle.color)
        # particle.printParticle()

        if particle.infected is False and particle.recovered is False:
            healthies.append(particle)

        elif particle.infected is True:
            infecteds.append(particle)

        elif particle.recovered is True:
            recovereds.append(particle)

    ## set axis limits ##
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.title("time={0}".format(t))

    plt.savefig("output/{0:03d}.jpg".format(i))
    plt.clf()

    return (len(healthies)/float(len(particles)), len(infecteds)/float(len(particles)), float(len(recovereds))/len(particles))



## plot function ends ##

## create universe ##
particles = []
# particles.append(Particle(0.2, 5, 0.5, 1.5))
# particles.append(Particle(8, 5, -0.5, 1.5, color='pink'))
NUM_PARTICLES = 50
PERCENTAGE_QUARANTINE = 0.4
quarantine_list = [True for i in range(int(PERCENTAGE_QUARANTINE*100))] + [False for i in range(int((1-PERCENTAGE_QUARANTINE)*100))]
for i in range(NUM_PARTICLES):
    randx = np.random.uniform(1, 9)
    randy = np.random.uniform(1, 9)
    randvelx = np.random.uniform(-2, 2)
    randvely = np.random.uniform(-2, 2)
    # print "[randx, randy, randvelx, randvely: {0} {1} {2} {3}]".format(randx, randy, randvelx, randvely)
    quarantined = np.random.choice(quarantine_list)
    if quarantined:
        randvelx = 0
        randvely = 0
    particles.append(Particle(randx, randy, randvelx, randvely, color='green', quarantine=quarantined))

## infect last particle ##
particles[-1].infected = True
particles[-1].color = 'red'


MAX_TIME = 100
hp = []
ip = []
rp = []
bar = Bar("Simulation frame", max=MAX_TIME)
for i in range(MAX_TIME):
    bar.next()
    particles = evolve(particles, simTime=i)
    (h, inf, r) = plotParticles(particles, t=i)
    hp.append(h)
    ip.append(inf)
    rp.append(r)
bar.finish()


## plot diagnostics ##
plt.plot(hp, label='healthy')
plt.plot(ip, label='infected')
plt.plot(rp, label='recovereds')

plt.xlabel("Time")
plt.ylabel("Percentage")
plt.legend()

plt.savefig("diagnostic.pdf")
plt.clf()


## convert the results in output to a gif ##
os.system("convert -delay 10 -loop 0 output/*.jpg animation.mp4")