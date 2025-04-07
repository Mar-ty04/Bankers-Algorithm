#Marisol Morales ID: 029984979
#Project 3: Banker's Algorithm
#Due by 3/30/2025

#importing numpy as we will be using this library due to its array features
# also more comfortable with this library due to Math 323  
import numpy as np  

#starting our class for bankers algorithm
class BankersAlgorithm:
    def __init__(self, available, maximum, allocated):
        self.available = np.array(available)
        self.maximum = np.array(maximum)
        self.allocated = np.array(allocated)
        self.need = self.maximum - self.allocated #doing this right here so that we dont have to make a new function to calculate this for us
        self.num_processes = len(self.need)
        self.num_resources = len(self.need[0])

    #now lets make our function for determining of the sequence is safe or not
    def is_Safe(self):
        work = self.available.copy() #this allows us to copy our available resources
        finish = [False] * self.num_processes #lets us track our completed processes
        safe_sequence = []

        #while loop to implement the proccess of checking if it safe to allocate or not
        #if safe then allocate the resources 
        while len(safe_sequence) < self.num_processes:
            allocat = False 
            for i in range(self.num_processes):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(self.num_resources)):
                    #lets allocate our resources now 
                    work = [work[j] + self.allocated[i][j] for j in range(self.num_resources)]
                    finish[i] = True
                    safe_sequence.append(i)
                    allocat = True
                    break
            if not allocat:
                return False, [] #when this is returned that means there was no safe sequence found
        return True, safe_sequence
    
    #now lets make our function that allows us to request resources 
    def request_resource(self, process_id, request):
        request = np.array(request)
        for j in range(self.num_resources):
            if request[j] > self.need[process_id][j]:
                print("Error: Not enough resources available.")
                return False
            if request[j] > self.available[j]:
                print("Error: Not enough resources available.")
                return False
        
        #lets temporarily allocate our resources (we will check if this is safe to do later!)
        self.available -= request
        self.allocated[process_id] += request
        self.need[process_id] -= request

        #now lets check if the resources we allocated is safe!
        safe, sequence = self.is_Safe()
        if not safe:
            #let roll back the resources since not safe to allocate them
            #basically reversing the math we did previously!
            self.available += request
            self.allocated[process_id] -= request
            self.need[process_id] += request
            print("Error: Request will lead to an unsafe state.")

        print("System is in a safe state.")
        print(f"Safe sequence: {sequence}")
        print(f"Resources allocated to process {process_id}.")
        return True
    
#now lets do our main function to be able to run this code
def main():
    #lets initialize our vectos based on how the pdf has initialized it for us 
    available = [3, 3, 2]
    maximum = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]

    bankersAlgor = BankersAlgorithm(available, maximum, allocation)

    #lets check in our main if it is safe
    safe, sequence = bankersAlgor.is_Safe()
    if safe:
        print("System is in a safe state.")
        print(f"Safe sequence: {sequence}")
    else:
        print("System is not in a safe state.")

    #lets allow for user input to occur now we will allow them to pick the process and
    #we will also allow them to request resources for that processes selected
    while True:
        #let our user specify which process id
        process_id = int(input("Enter Process ID: "))
        if process_id < 0 or process_id >= len(maximum):
            print("Invalid Process ID. Try again.")
            continue

        #now lets allow for them to input the resource request
        try:
            request = eval(input(f"Enter resource request. For example: [1, 0, 2]: "))
            if not isinstance(request, list) or len(request) != len(available):
                print("Error: Request does not match the number of resource types. Please try again.") #lets do this so that we dont worry so much about our code breaking!
                continue
        except:
            print("Invalid input format. Enter them as requested. For example: [0, 2, 2].") #lets do this so that we dont worry so much about our code breaking!
            continue
        
        #begin the request process
        #here we will also check if it is safe to the request and allocate those resources or not!
        bankersAlgor.request_resource(process_id, request)

main()