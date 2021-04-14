clc;
clear;
close all;

%% Problem Definition
CostFunction = @(x) MyCost(x);  %Cost Function
nVar = 10;                       %Number of unknown (Decision) Variables
VarSize = [1 nVar];             %Matrix Size of Decision Variables
VarMin = -5;                   %Lower Bound of Decision Variables
VarMax = 10;                    %Upper Bound of Decision Variables

%We're looking for variable that minimizes MyCost(x)

%% Parameters of PSO --> Iterative algrorithm

kap = 1;
phi1 = 2.05;
phi2 = 2.05;
phi = phi1 + phi2;
chi = 2*kap/abs(2-phi-sqrt(phi^2-4*phi));

MaxIt = 1000; % Max number of iteration
nPop = 50;   %Population Size (Swarm Size)
%Define w, c1, c2
w = chi;      %Inertial Coefficient
wdamp =0.99 %Damping rate of intertia coeff
c1 = chi*phi1;     %Personal Acceleration Coefficient
c2 = chi*phi2;     %Social Accelreation Coefficient


MaxV = (VarMax - VarMin)*0.2;
MinV = -MaxV;

%% Initialization

%Particle Template
empty_particle.Position = [];           %Position of Particle
empty_particle.Velocity = [];           %Velocity of Particle
empty_particle.Cost = [];               %Cost Function Value evaluated at particle pos
empty_particle.Best.Position = [];      %Personal best position
empty_particle.Best.Cost = [];          %Personal best cost

%Iterate above whatever population manyt times
%Repeat matrix
particle = repmat(empty_particle, nPop, 1);

%Initialize Global best
GlobalBest.Cost = inf;      %Initialized to Global best before iteration (WORST)
%GlobalBest.Position = 0;

%Initialize Population Members
for i = 1:nPop
    %Generate Random Solutions
    particle(i).Position = unifrnd(VarMin, VarMax, VarSize);    %Random positions
    
    %Initialize Velocity
    particle(i).Velocity = zeros(VarSize);
    
    %Evaluation
    particle(i).Cost = CostFunction(particle(i).Position);
    
    %Update the Personal Best
    particle(i).Best.Position = particle(i).Position;
    particle(i).Best.Cost = particle(i).Cost;
    
    %Update Global Best
    %Compare Global best to Particle Best
    a = particle(i).Best.Cost;
    b = GlobalBest.Cost;
    if a < b
        GlobalBest = particle(i).Best;
    end
end

%array to hold best cost value on each iteration
BestCosts = zeros(MaxIt, 1);


%% Main Loop of PSO

for it=1:MaxIt
    for i=1:nPop
        %update particle velocity
        particle(i).Velocity = w*particle(i).Velocity ...
            + rand(VarSize)*c1.*(particle(i).Best.Position - particle(i).Position) ...
            + rand(VarSize)*c2.*(GlobalBest.Position - particle(i).Position);
       
        %Apply Lower+Upper bound limit
        particle(i).Velocity = max(particle(i).Velocity, MinV);
        particle(i).Velocity = min(particle(i).Velocity, MaxV);
        
        %Update particle position
        particle(i).Position = particle(i).Position + particle(i).Velocity;

        %Apply Lower+Upper bound limit
        particle(i).Position = max(particle(i).Position, VarMin);
        particle(i).Position = min(particle(i).Position, VarMax);
        
        %Evaluate Current position to Personal Best
        particle(i).Cost = CostFunction(particle(i).Position);
        
        %Compare best position of particle, and update if need be
        if particle(i).Cost < particle(i).Best.Cost
            
            particle(i).Best.Position = particle(i).Position;
            particle(i).Best.Cost = particle(i).Cost;
            
             %Compare Global best to Particle Best
            e = particle(i).Best.Cost;
            f = GlobalBest.Cost;
            if e < f
                GlobalBest = particle(i).Best;
            end
        end
    end
    
    %Store best cost value
    BestCosts(it) = GlobalBest.Cost;
    
    %Display Iteration Information
    disp(['Iteration ' num2str(it) ': Best Cost = ' num2str(BestCosts(it))])

    %Damping Inertia Coefficient
    w = w * wdamp;
end

%% Results

figure;
plot(BestCosts, 'LineWidth', 2);
semilogy(BestCosts, 'LineWidth', 2);
xlabel('Iterations');
ylabel('Best Cost');
grid on;


