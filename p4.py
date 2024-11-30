# 1) decreasing k in the optimistic utility calculation increases accuracy. 
# Consistent when decreased from 2 -> 1, 1 -> 0.001, 0.001 -> 0.0001.
# 2) increasing alpha increase the accuracy. 
# Consistent when increased from 0.5 -> 0.75, 0.75 -> 0.90 and 0.90 -> 1.
# 3) terminating based on the number of episodes is better than using the cumulative change in Q value.

from copy import deepcopy
import random
import time

def print_grid(grid):
    res = ""
    for row in grid:
        res += "|"
        for i, x in enumerate(row):
            if isinstance(x, str):
                res += "{:^27}".format("#"*25)
            elif isinstance(x, list):
                list_str = "[" + ", ".join("{:.2f}".format(float(val)) for val in x) + "]"
                res += "{:^8}".format(list_str)
            else:
                res += "{:28.2f}".format(float(x))
            if i < len(row) - 1:
                res += "||"
            else:
                res += "|"
        res += "\n"
    return res+"\n"

def print_policy(grid):
    res = ""
    for row in grid:
        res += "|"
        for i, x in enumerate(row):
            # print(x)
            res += "{:^3}".format(x)
            if i < len(row) - 1: res += "||"
            else: res += "|"
        res += "\n"
    return res

def q_value_td_learning(problem):
    grid, noise, livingReward, discount, start = problem
    return_value = ''
    choices = {'N':[(-1,0), (0,1), (0,-1)], 'E':[(0,1), (1,0), (-1,0)], 'S':[(1,0), (0,-1), (0,1)], 'W':[(0,-1), (-1,0), (1,0)]}
    # probs = (1-2*noise, noise, noise)
    grid_q_val = deepcopy(grid)
    grid_n = deepcopy(grid)
    policy = deepcopy(grid)
    t = 0

    ##Initialising hyperparameters
    k = 0.0001 #gives the strength for the optimistic utility 
    e = 0.01 #0.01
    delta_q_0 = .00000001  # total hange in delta_q per episode to break out of the outer while loop
    t_terminate = 2500

    alpha_0 = 1 #inital value for alpha 
    decay_rate = 0.999 #decay rate of alpha
    ##############################

    #intialising for k=0
    for i in range(len(grid_q_val)):
        for j in range(len(grid_q_val[i])):
            if grid[i][j] == "#":
                grid_q_val[i][j] = "#"
                policy[i][j] = "#"
                grid_n[i][j] = 0
            elif grid[i][j] not in ["#", "_", "S"]: 
                grid_q_val[i][j] = float(0)
                grid_n[i][j] = 0
                policy[i][j] = "x"
            else: 
                grid_q_val[i][j] = [float(0)]*4
                grid_n[i][j] = [0]*4
                policy[i][j] = "_"
    return_value += print_grid(grid_q_val)
    directions = ["N", "E", "S", "W"]

    delta_q = 100
    # while delta_q > delta_q_0:
    while t < t_terminate:
        return_value += f"\nEpisode {t+1}\n"
        alpha = alpha_0 * decay_rate**t
        # alpha = 1/t
        cur = start
        delta_q = 0

        cur_itr = 1
        while "ERROR 404 NOT FOUND":
            # print(print_grid(grid_q_val)
            #finding the indented action with highest Q-value
            cur_idx = grid_q_val[cur[0]][cur[1]].index(max(grid_q_val[cur[0]][cur[1]]))
            intended_action = directions[cur_idx]
            
            #finding the taken action due to noise
            taken_action = random.choices(population=choices[intended_action], weights=[1 - noise*2, noise, noise])[0]

            #updating cur
            next_pos = (cur[0]+taken_action[0], cur[1]+taken_action[1]) if (0<=(cur[0]+taken_action[0])<len(grid)) and (0<=(cur[1]+taken_action[1])<len(grid[0])) and grid[cur[0]+taken_action[0]][cur[1]+taken_action[1]] != "#" else cur
            
            #break out of loop if exit is reached (end episode)
            if policy[next_pos[0]][next_pos[1]] == "x": 
                grid_n[next_pos[0]][next_pos[1]] += 1
                grid_q_val[cur[0]][cur[1]][cur_idx] = (1-alpha)*grid_q_val[cur[0]][cur[1]][cur_idx] + alpha*(livingReward+discount*grid_q_val[next_pos[0]][next_pos[1]])
                
                #exit action
                cur = next_pos
                grid_q_val[cur[0]][cur[1]] = (1-alpha)*grid_q_val[cur[0]][cur[1]] + alpha*(livingReward+discount*grid[next_pos[0]][next_pos[1]])
                break
            
            # print(grid_q_val[next_pos[0]][next_pos[1]])
            #finding the argmax of optimistic utility
            f = [grid_q_val[next_pos[0]][next_pos[1]][i_1]+k/(grid_n[next_pos[0]][next_pos[1]][i_1]+e)  for i_1 in range(len(grid_q_val[next_pos[0]][next_pos[1]]))]
            next_action_q = max(f)
            next_action_idx = f.index(next_action_q)
            
            #updating N(s',a')
            grid_n[next_pos[0]][next_pos[1]][next_action_idx] += 1

            #updating Q(s,a)
            grid_q_val[cur[0]][cur[1]][cur_idx] = (1-alpha)*grid_q_val[cur[0]][cur[1]][cur_idx] + alpha*(livingReward+discount*next_action_q)
            # delta_q += alpha*(livingReward+discount*next_action_q)

            #updating cur
            cur = next_pos
            
            #printing updates
            return_value += f"Iteration: {cur_itr}\n" + "Q-values:\n" + print_grid(grid_q_val)

            cur_itr += 1
        
        #print the policy after every episode
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if policy[i][j] not in ["#", "x"]: policy[i][j] = directions[grid_q_val[i][j].index(max(grid_q_val[i][j]))]
        return_value += "Policy:\n" + print_policy(policy)
        
        t+=1
    
    #print the final policy
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if policy[i][j] not in ["#", "x"]: policy[i][j] = directions[grid_q_val[i][j].index(max(grid_q_val[i][j]))]
    
    return_value += "\n\nFinal Policy:\n" + print_policy(policy)
    return return_value[:-1], policy 

if __name__ == "__main__":
    start_time = time.time()
    grid = [["_", "_", "_", 1], ["_", "#", "_", -1], ["S", "_", "_", "_"]]    
    discount = 1
    noise = 0.1
    livingReward = -0.01
    start = (2,0)
    problem = (grid, noise, livingReward, discount, start)

    iterations = 10
    optimal_policy = [['E', 'E', 'E', 'x'], ['N', '#', 'W', 'x'], ['N', 'W', 'W', 'S']]
    num_optimal_policies = 0
    q_values, policy = q_value_td_learning(problem)
    print(q_values)
    # for i in range(iterations):
    #     q_values, policy = q_value_td_learning(problem) #print q_values to find q_value updates for every episode
    #     if optimal_policy == policy: num_optimal_policies += 1
    #     print(print_policy(policy))
    # print(f"{num_optimal_policies}/{iterations}")
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
