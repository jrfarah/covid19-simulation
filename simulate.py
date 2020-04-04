#------------- imports -------------#
import matplotlib.pyplot as plt  
import numpy as np 
import os
from progress.bar import Bar


## class begins ##
class Particle():

    def __init__(self, x, y, xprime, yprime, color='blue'):


        ## position attributes ##

        self.xpos = x
        self.ypos = y

        ## velocity attributes ##

        self.xvel = xprime
        self.yvel = yprime

        ## color attributes ##
        self.color = color


    def printParticle(self):

        print ("[self.xpos: {0}]".format(self.xpos))
        print ("[self.ypos: {0}]".format(self.ypos))
        print ("[self.xvel: {0}]".format(self.xvel))
        print ("[self.yvel: {0}]".format(self.yvel))
        print ("[self.color: {0}]".format(self.color))

## class ends ##


## evolution function begins ##
def evolve(particles):

    for p, particle in enumerate(particles):

        ## interaction force ##
        for p2, particle2 in enumerate(particles[p+1:]):

            particle, particles[p+1+p2] = collisionForce(particle, particle2)
            # particle, particles[p+1+p2]  = interactionForce(particle, particle2)


        ## force of gravity ##
        particle = wallForce(particle)
        particle = force(particle, yacc=-0.4)

        newX = particle.xpos + particle.xvel
        newY = particle.ypos + particle.yvel

        particle.xpos = newX
        particle.ypos = newY

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



def interactionForce(particle1, particle2, k=-1./2.):
    
    distance = ((particle1.xpos - particle2.xpos)**2. + (particle1.ypos-particle2.ypos)**2.)**0.5   

    if distance < 0.5:
        particle1, particle2 = collisionForce(particle1, particle2)
        return particle1, particle2
    
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

    v2p = (v1 + v2 + np.sqrt(v1**2. + v2**2. - 2*v1*v2)) / 2.
    v2m = (v1 + v2 - np.sqrt(v1**2. + v2**2. - 2*v1*v2)) / 2.

    if v2p/abs(v2p) != v2/abs(v2):
        v2f = v2p
    else:
        v2f = v2m

    v1f = v1 + v2 - v2f

    return v1f, v2f

def collisionForce(particle1, particle2):

    distance = ((particle1.xpos - particle2.xpos)**2. + (particle1.ypos-particle2.ypos)**2.)**0.5

    if distance > 0.1:
        return particle1, particle2

    ## calculate the new x velocities ##
    newx1, newx2 = calculateCollisionVelocities(particle1.xvel, particle2.xvel)

    particle1.xvel = newx1
    particle2.xvel = newx2

    ## calculate the new x velocities ##
    newy1, newy2 = calculateCollisionVelocities(particle1.yvel, particle2.yvel)

    particle1.yvel = newy1
    particle2.yvel = newy2

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

    for particle in particles:

        ## show particle ##
        plt.scatter(particle.xpos, particle.ypos, c=particle.color)
        # particle.printParticle()
        particle.printParticle()

    ## set axis limits ##
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.title("time={0}".format(t))

    plt.savefig("output/{0:03d}.jpg".format(i))
    plt.clf()

## plot function ends ##

## create universe ##
particles = []
# particles.append(Particle(0.2, 5, 0.5, 1.5))
# particles.append(Particle(8, 5, -0.5, 1.5, color='pink'))
NUM_PARTICLES = 1
for i in range(NUM_PARTICLES):
    randx = np.random.uniform(1, 9)
    randy = np.random.uniform(1, 9)
    randvelx = np.random.uniform(-1, 1)
    randvely = np.random.uniform(-1, 1)
    # print "[randx, randy, randvelx, randvely: {0} {1} {2} {3}]".format(randx, randy, randvelx, randvely)
    particles.append(Particle(randx, randy, randvelx, randvely, color='blue'))


MAX_TIME = 100
bar = Bar("Simulation frame", max=MAX_TIME)
for i in range(MAX_TIME):
    bar.next()
    particles = evolve(particles)
    plotParticles(particles, t=i)
bar.finish()

## convert the results in output to a gif ##
os.system("convert -delay 10 -loop 0 output/*.jpg animation.mp4")