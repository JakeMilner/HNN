#import numpy files
import numpy as np
import random
import itertools
import copy

# Hopfield class
class HopfieldNetwork:

    # Constructor method
    def __init__(self, n, weight, b):

        # used to store the dimension
        self.n = n  
        #b vector stores activation function
        self.b = b
        #empty list to store states
        self.evolution = []
        #empty list to store steady points
        self.steady_points = []
        #empty to list to store minimum points
        self.minimum_points = []
                
        
                
        #decides if the unit of the network is to be activated
    def activate(self, element, i):
        
        # np.rint allows to round to the nearest integer
        # np.sign returns the sign of the vector
        # The activation function works as it follows:
        # if element > 0  output = 1
        # if element = 0 output = 0
        # if element > 0 output = 0
        return np.rint(.5 + .5 * np.sign(element + self.b[i]))
    
        #random asynchronous 
    def async(self, weight, state):
        
        #array equal to state variable
        new_state = copy.deepcopy(state)
        a = random.randint(0,self.n-1)
        c = self.activate(np.dot(weight, state), a)
        new_state[a] = c[a]

        return new_state
    
        #scan asynchronous
    def scan(self, weight, state): 
        
        #array equal to state variable
        new_state = copy.deepcopy(state)
        
        for i in range(self.n):
            a = np.dot(weight,new_state)
            new_state[i] = self.activate(a[i], i)

        return new_state  
    
        #main function to evolve the system
    def hopfield(self, update_name, weight, state, n_iterations):
        
        #choose updating rule
        if update_name == 'scan': 
            update = self.scan
        elif update_name == 'async':
            update = self.async
        else:
            print 'No update rules having that name. Try [scan, async]'
            return -1
        
        #array equal to state variable
        new_state = copy.deepcopy(state)
        
        #Reset the evolution list
        self.evolution = []
        
        #Append the initial state to the list
        self.evolution.append(state)
        
        i = 0
        while i < n_iterations:
            
            #Retrieve the next state of the network
            new_state = update(weight, new_state)
            self.evolution.append(new_state)
            
            # Increment i
            i += 1
            
        # Return the last state
        return self.evolution
    
    
    
    # Function which computes the energy of the system
    # The energy of one state can be defined in a vector 
    # notation as: H(u) = -1/2u^{T}*W*u - u^{T}b
    def energy(self, weight, state):
        
        #array equal to state variable
        state = np.array(state)

        # Definition of the energy of the system
        return -0.5 * np.dot(state, np.dot(weight, state)) - np.dot(state, self.b)
    
    
    
    #Test each of the 2^9 = 512 possible states of the network
    # in order to detect the steady states. A state is steady if 
    # it remains constant over the time
    def retrieve_steady_points(self, update_name, weight):

        #choose updating rule      
        if update_name == 'scan': 
            update = self.scan
        elif update_name == 'sync':
            update = self.sync
        else:
            print 'It is not possible retrieve the steady state with that rule. Try [scan]'
            return -1
        
        for state in [list(x) for x in itertools.product(range(2), repeat=self.n)]:
        
            # If I apply the update function to the state and I obtain
            # exactly the same state, it is a steady point
            if update(weight, state) == state:
                self.steady_points.append(state)
            
            
        #Return the steady points
        return self.steady_points
    
    
    
    # It retrieves the positions for which the energy function is lowest
    def retrieve_minimum_points(self, steady_points, weight, strictly):
        
        # Quick check on the strictly values
        if not (strictly == 1 or strictly == 0):
            print 'The value of the strictly parameter is not allowed. Try [0,1]'
        
        #Cycle over each steady state
        for state in steady_points:
            # If the comparison returns 1, then the state is stable
            # Otherwise it is not stable
            if self.comparing_neighbour_energies(state, weight, strictly):
                self.minimum_points.append(state)
                
        #Return the stable points
        return self.minimum_points
            
    
    
    
    # It compares the energy of the provided state
    # with those of its neighbours
    def comparing_neighbour_energies(self, state, weight, strictly):  
        # I compute the energy associated to the state
        energy_state = self.energy(weight, state)
        print ' '
        print 'Energy of fixed point',state, ' : ', energy_state
        print ' '
        #compare energy levels to energy levels of neighbour states
        for i in range(len(state)):
            
            if state[i] == 1: 
                neighbour = state[:i] + [0] + state[i+1:]
            else: 
                neighbour = state[:i] + [1] + state[i+1:]

            print 'Energy of neighbour',neighbour, ' : ', self.energy(weight, neighbour)
            if strictly == 1:
                if self.energy(weight, neighbour) <= energy_state:
                    return 0
            else:
                if self.energy(weight, neighbour) < energy_state:
                    return 0                
            
        # If the test passes then the point is a stable point
        return 1