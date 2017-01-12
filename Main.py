import numpy as np
import HopfieldNetwork
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.font_manager
font = {'size'   : 7}
matplotlib.rc('font', **font)
fig = plt.figure(figsize = (6,5))


#Initial set of parameters
n = 9
weight_value = 0.5
b = [0.]*n
strictly = 0
# Initial points to test the network
init=[[1, 1, 1, 0, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 0, 0, 1],
[1, 1, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 1, 0, 1, 0, 1, 1],
[1, 0, 0, 1, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 0, 1, 1, 1],
[0, 0, 1, 0, 0, 0, 1, 1, 1], [1, 1, 0, 1, 0, 0, 0, 1, 0],
[0, 1, 0, 1, 0, 1, 0, 0, 0], [0, 1, 0, 1, 1, 0, 1, 0, 0],
[0, 0, 1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 1, 1, 1, 0, 1, 1],
[1, 0, 1, 1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 0, 1, 0, 0],
[1, 0, 0, 1, 0, 1, 0, 0, 0], [1, 0, 0, 1, 1, 0, 0, 0, 1],
[0, 0, 1, 0, 0, 0, 1, 0, 1], [1, 0, 0, 1, 1, 0, 1, 0, 1],
[0, 0, 0, 0, 1, 0, 1, 1, 1], [1, 0, 0, 1, 1, 0, 0, 1, 0]]

#The inhibition constant w = 0.5 or 1
initial_weight = input('Enter inhibition constant: ')

#Define the inital weight matrix using the negative inhibition constant. 
weight = -initial_weight*np.ones([n,n])
for i in range(n):
    for j in range(n):
        # Different cases in which I have to modify the matrix element
        if i == j: weight[i,j] = 0
        elif (i==1 and (j==4 or j==7)): weight[i,j] = 1
        elif (i==3 and (j==4 or j==5)): weight[i,j] = 1
        elif (i==4 and (j==1 or j==7)): weight[i,j] = 1
        elif (i==4 and (j==3 or j==5)): weight[i,j] = 1
        elif (i==5 and (j==3 or j==4)): weight[i,j] = 1
        elif (i==7 and (j==1 or j==4)): weight[i,j] = 1

print 'For inhibition constant:', initial_weight
print ' '
print 'Weight Matrix'
print weight
print ' '

hop = HopfieldNetwork.HopfieldNetwork(n, weight, b)

# 1) Determine fixed points
steady_points = hop.retrieve_steady_points('scan', weight)
print 'Fixed points:'
print steady_points
print ' '

# 2) Compute minimum points based on energy levels of the neighbouring points
#being greater than or equal to the energy levels of the fixed points
minimum_points = hop.retrieve_minimum_points(steady_points, weight, strictly)
print ' '
print 'Therefore the the minimum points are:'
print minimum_points
print ' '
# 3) Run the network aysnchronously both in scan and random order,
# however the scan order is the result which I print out
save_list = [[1, 1, 1, 0, 0, 1, 1, 0, 1],[0, 1, 0, 1, 1, 1, 0, 1, 1]]
#In order to make comparisons regarding a number of iterations I run the next code
#5 times. This way the graph produces lines of energy against time for each iteration
for x in range(5):
    # I begin the cycle
    print 'Initial State:', '               ' 'Final State:'
    print ' '
    for state in init: 
        
        print  state, ':',
        
        # I evolve the network for the selected number of times, also
        # providing the weight matrix and the selected state and the
        # desired updating rule
        # After having run the hopfield function, it returns the list
        # containing all the states which was hit
        evolution_states_scan = hop.hopfield('scan', weight, state, 5)
        # I record the scan energy of all the states
        energy_scan = [hop.energy(weight, x) for x in evolution_states_scan]
        
        # The same as before using the random asynchronous rule instead
        evolution_states_async = hop.hopfield('async', weight, state, 50)
        energy_async = [hop.energy(weight, x) for x in evolution_states_async]
        
        print evolution_states_scan[-1]
        
        # I save the energy plots
        if state in save_list:
            plt.plot(energy_async)
            plt.title('Hopfield energy against iteration (Random asynchronous rule)')
            plt.ylabel('Energy')
            plt.xlabel('Time')
            plt.grid(True)
            # I save the plot obtained in a file in order to be able to reuse it
            plt.savefig("energy_async__%s_%s.png" % (str(weight_value).replace('.',''),''.join(str(x) for x in state)), bbox_inches='tight', transparent = True, dpi = 600)

            plt.plot(energy_scan)
            plt.title('Hopfield energy against iteration (Scan asynchronous rule)')
            plt.ylabel('Energy')
            plt.xlabel('Time')
            plt.grid(True)
            # I save the plot obtained in a file in order to be able to reuse it
            plt.savefig("energy_scan__%s_%s.png" % (str(weight_value).replace('.',''),''.join(str(x) for x in state)), bbox_inches='tight', transparent = True, dpi = 600)
