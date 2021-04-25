import random
import time
import matplotlib.pyplot as plt
Pt = 4      #Transmitter power in dbm
Pr = 69     #RSSI
x0 = 0      #x position of the observer
y0 = 0      #y position of the observer
alpha = 2   #constant coefficient for shadowing (Object in the way like walls, window, etc)
x = 0
y = 0
s = 0
gx = []
gy = []
hx = []
hy = []

def objective_function(O):
    x = O[0]     #x-value of particle position
    y = O[1]     #y-value of particle position

    #z is the objective function it minimizes based on variables x and y 
    z = s + (Pr*((x0 - x)**2 + (y0 - y)**2)**(alpha/2)-Pt)**2
    return z

boundary = [(-100, 100), (-100, 100)]  # upper and lower bounds of variables
nvar = 2  # number of variables
maxmin = -1  # if minimization problem, mm = -1; if maximization problem, mm = 1

# parameters OF PSO
nparticle = 100  # number of particles
iterations = 50  # max number of iterations
w = 0.9  # inertial coefficient
c1 = 2  # Personal Acceleration Coefficient
c2 = 2  # Social Acceleration Coefficient

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
    ax.scatter(gx, gy, label= "stars", color= "green", 
            marker= "*", s=30)
    ax.scatter(hx, hy, label= "o", color= "blue", 
            marker= "o", s=30)
    plt.xlabel('x - axis')
    # frequency label
    plt.ylabel('y - axis')
    # plot title
    plt.title('My scatter plot!')
    # showing legend
    plt.legend()
    plt.show()

    
