###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    res = {}
    with open(filename, 'rb') as f:
        for line in f.readlines():
            line = line.strip()
            val = line.split(',')
            res[val[0]] = val[1] 
    return res

def greedy_trip(cows_list, limit):
    trip = []
    remaining_cows = []
    for k, v in cows_list:
        if int(v) > limit:
            continue
        else:
            trip.append((k,v))
            limit = limit - int(v)  
    for each in cows_list:
        if each not in trip:
            remaining_cows.append(each)

    return trip, remaining_cows

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cows_list = cows.copy()
    from operator import itemgetter
    cows_list = sorted(cows_list.items(), key = itemgetter(1), reverse = True)
    trips = [] 
    
    while len(cows_list) > 0:
        trip, cows_list = greedy_trip(cows_list, limit) 
        trips.append(trip)
 
    return trips


def brute_force_min_trips(cows_list, minimum_len, limit):
    for each in get_partitions(cows_list):
        if len(each) == minimum_len:
            is_found = 1
            for route in each:
                sum_wt = 0
                for each_trip in route:
                    sum_wt += int(each_trip[1])
                if sum_wt > limit:
                    is_found = 2  
                    break
            if is_found == 1:
                return each
    return None


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of   name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cows_list = cows.copy()
    from operator import itemgetter
    cows_list = sorted(cows_list.items(), key = itemgetter(1), reverse = True)

    minimum_len = 1
    while minimum_len<= len(cows_list):
        path = brute_force_min_trips(cows_list, minimum_len, limit)  
        if path: 
            return path
        minimum_len+=1
    return None

# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    
    cows = load_cows('ps1_cow_data.txt')
    
    start = time.time()
    path_greedy = greedy_cow_transport(cows)
    end = time.time()
    print 'Greedy algo path is {}'.format(path_greedy)
    print 'Time taken by greedy algo is ', str(end - start)

    start = time.time()
    path_brute_force = brute_force_cow_transport(cows)
    end = time.time()
    print 'Brute force path is {}'.format(path_brute_force)
    print 'Time taken by brute force algo is {} seconds'.format(end - start)

if __name__ == '__main__':  
    compare_cow_transport_algorithms()