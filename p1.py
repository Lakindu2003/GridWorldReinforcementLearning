import sys, grader, parse
import random

def print_grid(grid):
    res = ""
    for row in grid:
        res+=" "    
        res+=" ".join(f"{str(x):>4}" for x in row)
        res+="\n"
    return res

def play_episode(problem):
    seed, noise, livingReward, grid, policy, start = problem
    experience = ''
    cum_reward = 0.0
    end_line = "-------------------------------------------- \n"
    
    if seed!=-1: random.seed(seed, version=1) 
    choices = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
    
    #initialising the grid
    pos = start
    temp = grid[pos[0]][pos[1]] 
    grid[pos[0]][pos[1]] = "P"
    experience += "Start state:\n" + print_grid(grid) + "Cumulative reward sum: 0.0\n" + end_line

    while 1:
        # print(print_grid(grid))
        #selecting next action
        intended_action = policy[pos[0]][pos[1]]
        taken_action = random.choices(population=choices[intended_action], weights=[1 - noise*2, noise, noise])[0]
        experience += f"Taking action: {taken_action} (intended: {intended_action})\n"

        #processing next action
        if taken_action == "N": next_pos = (pos[0]-1, pos[1])
        elif taken_action == "E": next_pos = (pos[0], pos[1]+1)
        elif taken_action == "W": next_pos = (pos[0], pos[1]-1)
        else: next_pos = (pos[0]+1, pos[1])
        if next_pos[0]<0 or next_pos[1]<0 or next_pos[0]>=len(grid) or next_pos[1]>=len(grid[0]) or grid[next_pos[0]][next_pos[1]] == "#": #check if unable to move
            next_pos = pos
            cum_reward += livingReward
            cum_reward = round(cum_reward, 2)
            experience += f"Reward received: {livingReward}\n" + "New state:\n" + print_grid(grid) + f"Cumulative reward sum: {cum_reward}\n" + end_line
        else:
            # if pos == start: grid[start[0]][start[1]] = "S"
            cum_reward += livingReward
            cum_reward = round(cum_reward, 2)
            grid[pos[0]][pos[1]] = temp
            temp = grid[next_pos[0]][next_pos[1]]
            if grid[next_pos[0]][next_pos[1]] != "_" and grid[next_pos[0]][next_pos[1]] != "S": 
                final_reward = float(temp)
                break
            grid[next_pos[0]][next_pos[1]] = "P"
            experience += f"Reward received: {livingReward}\n" + "New state:\n" + print_grid(grid) + f"Cumulative reward sum: {cum_reward}\n" + end_line
               
            pos = next_pos
    
    #finish processing the action prior to the exit action
    grid[next_pos[0]][next_pos[1]] = "P"
    experience += f"Reward received: {livingReward}\n" + "New state:\n" + print_grid(grid) + f"Cumulative reward sum: {cum_reward}\n" + end_line
    #processing exit action
    cum_reward += final_reward
    grid[next_pos[0]][next_pos[1]] = temp
    experience += "Taking action: exit (intended: exit)\n" + f"Reward received: {final_reward}\n" + "New state:\n" + print_grid(grid) + f"Cumulative reward sum: {cum_reward}"
        
    return experience

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)