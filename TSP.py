import random
import turtle
import math
import copy

def student_details():
    
    # add variables to store student ID and username to be returned
    student_id = 18016995
    student_username = "ak18afd"

    return student_id, student_username

def generate_map(x_range, y_range, locations):

    # add code to create a list then use a for loop to create a random population for this list
    generated_map = [] #Empty List that contains the generated map
    for coordinate in range(locations): #For Loop to iterate through the number of locations provided
        generated_map.append([random.randint(-x_range,x_range),random.randint(-y_range,y_range)])#Appends the x,y coordinate to the empty list

    return generated_map

def print_map(speed, color, thickness, selected_map):

    # add code to use the turtle to draw the path between all destinations
    # the turtle should make use of the parameters provided: speed. color, etc...
    # you will need to use a loop in order to draw the path to all locations
    
    turtle.up()#prevents the intialisation from drawing on the screen
    turtle.speed(speed)#Sets the speed of the turtle
    turtle.color(color)#Sets the color of the turtle
    turtle.pensize(thickness)#Sets the pensize
    
    for q in selected_map:#For Loop iterating through the selected_map to draw the points
        turtle.goto(q)#Draws the point onto the screen
        turtle.down()#Places the turlte down after intialization to begin drawing
    
def calculate_distance(starting_x, starting_y, destination_x, destination_y):
    distance = math.hypot(destination_x - starting_x, destination_y - starting_y)  # calculates Euclidean distance (straight-line) distance between two points
    return distance

def calculate_path(selected_map):

    # you will need to setup a variable to store the total path distance
    # you will need to use a loop in order to calculate the distance of the locations individually
    # it would be wise to use make use of the calculate_distance function as you can reuse this
    # remember your need to calculate the path of all locations returning to the original location
    
    l = len(selected_map)
    distance = 0
    for y in range(l-1):
        distance += calculate_distance(selected_map[y][0],selected_map[y][1],selected_map[y+1][0],selected_map[y+1][1])

    distance += calculate_distance(selected_map[-1][0],selected_map[-1][1],selected_map[0][0],selected_map[0][1])
    
    return distance

#################################################################################################

def nearest_neighbour_algorithm(selected_map):

    temp_map = copy.deepcopy(selected_map)
    
    # you need to create an empty list for your optimised map
    
    optermised_map = []
    optermised_map.append(temp_map.pop())
    
    for nearest in range(len(temp_map)):

        # you need to add some variables to store establish the closest location
        nearest_value = 1000
        nearest_index = 0
        
        for NearestX in range(len(temp_map)):
            #temp = i # NOTE: you can remove this line once function is implemented
            # you need to calculate the distance between the current path and the next potential location
            # it would be wise to use make use of the calculate_distance function
            current_value = abs(calculate_distance(optermised_map[nearest][0],optermised_map[nearest][1],temp_map[NearestX][0],temp_map[NearestX][1]))

            if current_value < nearest_value:
                nearest_value = current_value
                nearest_index = NearestX

                # you will need to write an if statement to establish if the current distance is lower than the stored
                # best distance, and if so set the best distance to the current location

        # the final step is to add the closest location to the optermised_map and remove from the temp_map

        optermised_map.append(temp_map[nearest_index])
        del temp_map[nearest_index]
   
    return optermised_map

#################################################################################################

def genetic_algorithm(selected_map, population, iterations, mutation_rate, elite_threshold):

    # this is the main genetic algorithm function and should make use of the inputs and call the sub functions in order to run
    # you will need to call the create_population function and store this in a list
    # you will then need to use the iterator function and store the returned solution to best_solution
    
    Create_Pool = create_population(population,selected_map)
    best_solution = iterator(Create_Pool,iterations,mutation_rate,elite_threshold)
    
    return best_solution

def create_population(population, selected_map):

    # you need to create an empty list called gene_pool for the population
    # use a for loop and the provided inputs to create the population
    # you will also need to randomise the individuals within the population
    
    gene_pool = []
    for p in range(population):
        gene_pool.append(copy.deepcopy(selected_map))
        random.shuffle(gene_pool[p])
        
    return gene_pool

def fitness_function(gene_pool, best_solution):

    # you need to find a way to rank the fitness of your population. one way you may consider doing this is with a ranked list
    # you will need to have correctly implemented the calculate_path function in order to rank the fitness of the population
    # you may consider using a loop to achieve this
    # your function must return a sorted gene pool that is sorted by fittest (shortest path to longest path)
    # your function should also return the fittest individual in best_solution

    best_arrangement_score = calculate_path(best_solution)
    best_solution = copy.deepcopy(gene_pool[0])
    sorted_gene_pool = []
    ranking = []
    
    for idx,x in enumerate(gene_pool):
        score = 0
        score += abs(calculate_path(x))
        
        ranking.append(score)
        
        if score < best_arrangement_score:
            best_solution = x
            best_arrangement_score = score
    
    sorted_gene_pool = copy.deepcopy([x for _,x in sorted(zip(ranking,gene_pool))])
    
    return sorted_gene_pool, best_solution

def iterator(gene_pool, iterations, mutation_rate, elite_threshold):

    # you need to use the provided inputs to iterate (run) the algorithm for the specified iterations
    # you will need to use a for loop in order to achieve this
    # in order for this function to work all over parts of the algorithm must be complete
    # the function must return the best individual (best_solution) in the population
    
    sorted_gene_pool = []
    new_gene_pool = gene_pool
    current_best_solution = copy.deepcopy(gene_pool[0])
    new_best_solution = copy.deepcopy(gene_pool[0])
    BestSolution = []

    for i in range(iterations):
        sorted_gene_pool, new_best_solution = fitness_function(new_gene_pool,current_best_solution)
        BestSolution.append(new_best_solution)
        new_gene_pool = mating_function(sorted_gene_pool, new_best_solution, mutation_rate, elite_threshold)

    LowestScore = []
    for idscore, score in enumerate(BestSolution):
        LowestScore.append(calculate_path(score))
        
    Sorted_Score = [y for _,y in sorted(zip(LowestScore,BestSolution))]
    best_solution = Sorted_Score[0]
    
    return best_solution

def mating_function(gene_pool, best_solution, mutation_rate, elite_threshold):

    # you need to create a new list called new_gene_pool to store the newly created individuals from this function
    # you will need to use a loop in order to perform the genetic crossover and mutations for each individual
    # in order for this function to work correctly you need to select the parent genes based to create the child
    # one of the top individuals based on the elite_threshold should be selected as one of the parents
    # once both parents have been chosen the breed function should be called using both of these parents
    # this means the breed function must be working and returning a child
    # once the breed function has returned a new individual this individual needs to be mutated
    # this means you need to implement the mutate function and it must return the mutated child
    # the function must return a new generation of individuals in new_gene_pool

    new_gene_pool = []
    for m in gene_pool:
        p_1 = copy.deepcopy(gene_pool[random.randint(0,int(len(gene_pool)*elite_threshold))])
        p_2 = copy.deepcopy(m)
        new_gene_pool.append(mutate(breed(p_1,p_2),mutation_rate))

    new_gene_pool[len(gene_pool)-1] = copy.deepcopy(best_solution)
    
    return new_gene_pool

def breed(parent_1, parent_2):

    # you need to select random points in which to cut the genes of the parents and put them into the child
    # because the individual must contain all of the locations (this is a unique issue to the TSP) the gene selection is slightly more difficult
    # one suggested way is to selected portions of genetic data from one parent then fill in the remainder of locations from the other parent
    # the portion of genes selected should be random and you may want to use some for loops to achieve this
    # the function must return a child of the 2 parents containing all the locations in the original map
    
    cut_points = []
    cut_points.extend([random.randint(0,len(parent_1)),random.randint(0,len(parent_1))])
    cut_points.sort()

    child = []
    dna_1 = []
    dna_2 = []
    
    for g in range(cut_points[0],cut_points[1]):
        dna_1.append(parent_1[g])
        
    dna_2 = [item for item in parent_2 if item not in dna_1]#Anything that isnt from parent comes from parent 2
    child = (dna_1 + dna_2)
    
    return child

def mutate(child, mutation_rate):

    # this function must mutate the genes of the child based on the mutation rate provided
    # to achieve this you may want to use a for loop to go through the child
    # then use a random number with an if statement according the mutation rate
    # selected genes will then need to be swapped
    # the function must return a child containing all the locations in the original map but not as it originally arrived
    
    mutated_child = []
    for switch  in range(len(child)):
        if(random.random() < mutation_rate):
            switchwith = random.randint(0,len(child)-1)
            gene_1 = child[switch]
            gene_2 = child[switchwith]
            child[switch] = gene_2
            child[switchwith] = gene_1
            
    mutated_child = child

    return mutated_child
