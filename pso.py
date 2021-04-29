import random
import time
import matplotlib.pyplot as plt
Pt = -18      #Transmitter power in dbm
Pt = (1000)*(10**(Pt/10))
Pr = -69     #RSSI
Pr = (1000)*(10**(Pr/10))
x0 = 0      #x position of the observer
y0 = 0      #y position of the observer
alpha = 3   #constant coefficient for shadowing (Object in the way like walls, window, etc)
x = 13
y = 12
s = 0
gx = []
gy = []
hx = []
hy = []
s1 = 0
s2 = 0
s4 = 0
g1 = 0
g2 = 0
g3 = 0
p1 = 0
p2 = 0
p3 = 0

def objective_function(O):
    xx = O[0]     #x-value of particle position
    yy = O[1]     #y-value of particle position

    #z is the objective function it minimizes based on variables x and y 
    z = s + (Pr*((xx - x0)**2 + (yy - y0)**2)**(alpha/2)-Pt)**2
    #print(z)
    return z

boundary = [(-30, 30), (-30, 30)]  # upper and lower bounds of variables
nvar = 2  # number of variables
maxmin = -1  # if minimization problem, mm = -1; if maximization problem, mm = 1

# parameters OF PSO
nparticle = 100  # number of particles
iterations = 50  # max number of iterations
w = 0.7  # inertial coefficient
c1 = 2.05  # Personal Acceleration Coefficient
c2 = 3.2  # Social Acceleration Coefficient

# Visuals
"""
fig = plt.figure()
ax = fig.add_subplot()
fig.show()
plt.title('Optimizing Solution: ')
plt.xlabel("Number of Iterations")
plt.ylabel("Objective Function Value")
"""
class Particle:
    def __init__(self, boundary):
        self.particle_position = []  # particle position
        self.particle_velocity = []  # particle velocity
        self.local_best_particle_position = []  # best position of particle
        self.p_local_best_particle_position = initial_p
        self.p_particle_position = initial_p

        for i in range(nvar):
            self.particle_position.append(random.uniform(boundary[i][0],boundary[i][1]))
            self.particle_velocity.append(random.uniform(-1,1))

    def evaluate(self, objective_function):
        self.p_particle_position = objective_function(self.particle_position)
        if maxmin == -1:
            if self.p_particle_position < self.p_local_best_particle_position:
                self.local_best_particle_position = self.particle_position  # update the local best
                self.p_local_best_particle_position = self.p_particle_position  # update the p of the local best
        if maxmin == 1:
            if self.p_particle_position > self.p_local_best_particle_position:
                self.local_best_particle_position = self.particle_position  # update the local best
                self.p_local_best_particle_position = self.p_particle_position  # update the p of the local best


    def update_velocity(self, global_best_particle_position):
        for i in range(nvar):
            r1 = random.random()
            r2 = random.random()

            personal_velocity = c1 * r1 * (self.local_best_particle_position[i] - self.particle_position[i])
            social_velocity = c2 * r2 * (global_best_particle_position[i] - self.particle_position[i])
            self.particle_velocity[i] = w * self.particle_velocity[i] + personal_velocity + social_velocity

    def update_position(self, boundary):
        for i in range(nvar):
            self.particle_position[i] = self.particle_position[i] + self.particle_velocity[i]

            # check and repair to satisfy the upper boundary
            if self.particle_position[i] > boundary[i][1]:
                self.particle_position[i] = boundary[i][1]
            # check and repair to satisfy the lower boundary
            if self.particle_position[i] < boundary[i][0]:
                self.particle_position[i] = boundary[i][0]

class PSO:
    def __new__(self, objective_function, boundary, nparticle, iterations):
        p_global_best_particle_position = initial_p
        global_best_particle_position = []
        sp = []
        for i in range(nparticle):
            sp.append(Particle(boundary))
        A = []

        for i in range(iterations):
            for j in range(nparticle):
                sp[j].evaluate(objective_function)

                if maxmin == -1:
                    if sp[j].p_particle_position < p_global_best_particle_position:
                        global_best_particle_position = list(sp[j].particle_position)
                        p_global_best_particle_position = float(sp[j].p_particle_position)
                if maxmin == 1:
                    if sp[j].p_particle_position < p_global_best_particle_position:
                        global_best_particle_position = list(sp[j].particle.position)
                        p_global_best_particle_position = float(sp[j].p_particle_position)
            for j in range(nparticle):
                sp[j].update_velocity(global_best_particle_position)
                sp[j].update_position(boundary)

            A.append(p_global_best_particle_position)
            print('Iteration #: ', i, ' value: ', p_global_best_particle_position)
            ax.plot(A, color='b')
            fig.canvas.draw()
            ax.set_xlim(left=max(0, i-iterations),right=i+3)
            time.sleep(0.01)
        print('Final Result: ')
        print('Optimized solution: ', global_best_particle_position)
        print('Objective function value: ', p_global_best_particle_position)
        z = objective_function(global_best_particle_position)
        gx.append(global_best_particle_position[0])
        gy.append(global_best_particle_position[1])  
        return z

if maxmin == -1:
    initial_p = float("inf")

if maxmin == 1:
    initial_p = -float("inf")
count = 0
while(1):
    count += 1
    fig = plt.figure(1)
    ax = fig.add_subplot()
    fig.show()
    plt.title('Optimizing Solution: ')
    plt.xlabel("Number of Iterations")
    plt.ylabel("Objective Function Value")
    x0 = input("Your x coordinate: ")
    print(x0)
    y0 = input("Your y coordinate: ")
    print(y0)
    Pr = input("Measured RSSI Value: ")
    print(Pr)
    x0 = float(x0)
    y0 = float(y0)
    Pr = float(Pr)
    Pr = (1000)*(10**(Pr/10))
    s = s + PSO(objective_function, boundary, nparticle, iterations)
    s = float(s)
    hx.append(x0)
    hy.append(y0)
    plt.title('Optimizing Solution: ')
    plt.xlabel("Number of Iterations")
    plt.ylabel("Objective Function Value")
    plt.show()
    
    fig = plt.figure(2)
    ax = fig.add_subplot(212)
    fig.show()
    sumx = 0
    sumy = 0
    for i in gx:
        sumx = sumx + i
    sumx = sumx / len(gx)
    for j in gy:
        sumy = sumy + j
    sumy = sumy / len(gy)
    ax.scatter(sumx, sumy, label="stars", color="green",marker="*", s=30)
    ax.scatter(hx, hy, label= "o", color= "blue", marker= "o", s=30)
    p = 0
    q = 0
    i = 1
    a = len(gx)
    while i < a:
        p += gx[i-1]
        q += gy[i-1]
        i += 1
    p = p/a
    q = q/a
    ax.scatter(hx, hy, label= "o", color= "blue", marker= "o", s=30)
    
    plt.xlabel('x - axis (meters)')
    # frequency label
    plt.ylabel('y - axis (meters)')
    # plot title
    plt.title('Map')
    # showing legend
    plt.legend()
    plt.show()

    
