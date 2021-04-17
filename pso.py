import random
import time
import matplotlib.pyplot as plt

def objective_function(O):
    x = O[0]     #x-value of particle position
    y = O[1]     #y-value of particle position
    nonlin_rule = (x - 1) ** 3 - y + 1
    lin_rule = x + y - 2
    if nonlin_rule > 0:
        p1 = 1
    else:
        p1 = 0
  
    if lin_rule > 0:
        p2 = 1
    else:
        p2 = 0
    #z is the objective function it minimizes based on variables x and y 
    z = (1 - x) ** 2 + 100 * (y - x ** 2) ** 2 + p1 + p2
    return z
  
bounds = [(-1.5, 1.5), (-0.5, 2.5)]  # upper and lower bounds of variables
nvar = 2  # number of variables
maxmin = -1  # if minimization problem, mm = -1; if maximization problem, mm = 1
  
# parameters OF PSO
particle_size = 120  # number of particles
iterations = 200  # max number of iterations
w = 0.8  # inertial coefficient
c1 = 1  # Personal Acceleration Coefficient
c2 = 2  # Social Acceleration Coefficient
  
# Visuals
fig = plt.figure()
ax = fig.add_subplot()
fig.show()
plt.title('Optimizing Solution: ')
plt.xlabel("Number of Iterations")
plt.ylabel("Objective function value")
# ------------------------------------------------------------------------------
class Particle:
    def __init__(self, bounds):
        self.particle_position = []  # particle position
        self.particle_velocity = []  # particle velocity
        self.local_best_particle_position = []  # best position of particle
        self.p_local_best_particle_position = initial_p
        self.p_particle_position = initial_p
        
        for i in range(nvar):
            self.particle_position.append(random.uniform(bounds[i][0],bounds[i][1]))
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
  
    def update_position(self, bounds):
        for i in range(nvar):
            self.particle_position[i] = self.particle_position[i] + self.particle_velocity[i]
  
            # check and repair to satisfy the upper bounds
            if self.particle_position[i] > bounds[i][1]:
                self.particle_position[i] = bounds[i][1]
            # check and repair to satisfy the lower bounds
            if self.particle_position[i] < bounds[i][0]:
                self.particle_position[i] = bounds[i][0]
  
class PSO:
    def __init__(self, objective_function, bounds, particle_size, iterations):
        p_global_best_particle_position = initial_p
        global_best_particle_position = []
        sp = []
        for i in range(particle_size):
            sp.append(Particle(bounds))
        A = []
        
        for i in range(iterations):
            for j in range(particle_size):
                sp[j].evaluate(objective_function)
                
                if maxmin == -1:
                    if sp[j].p_particle_position < p_global_best_particle_position:
                        global_best_particle_position = list(sp[j].particle_position)
                        p_global_best_particle_position = float(sp[j].p_particle_position)
                if maxmin == 1:
                    if sp[j].p_particle_position < p_global_best_particle_position:
                        global_best_particle_position = list(sp[j].particle.position)
                        p_global_best_particle_position = float(sp[j].p_particle_position)
            for j in range(particle_size):
                sp[j].update_velocity(global_best_particle_position)
                sp[j].update_position(bounds)
                
            A.append(p_global_best_particle_position)
            print('Iteration #: ', i, ' value: ', p_global_best_particle_position)
            ax.plot(A, color='b')
            fig.canvas.draw()
            ax.set_xlim(left=max(0, i-iterations),right=i+3)
            time.sleep(0.01)
        print('Final Result: ')
        print('Optimized solution: ', global_best_particle_position)
        print('Objective function value: ', p_global_best_particle_position)

if maxmin == -1:
    initial_p = float("inf")
    
if maxmin == 1:
    initial_p = -float("inf")

PSO(objective_function, bounds, particle_size, iterations)
plt.show()