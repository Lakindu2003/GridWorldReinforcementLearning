import sys, grader, parse
from copy import deepcopy

def print_grid(grid):
    res = ""
    for row in grid:
        res += "|"
        for i, x in enumerate(row):
            if isinstance(x, str): res += "{:^7}".format(x)
            else: res += "{:7.2f}".format(float(x))
            if i < len(row) - 1: res += "||"
            else: res += "|"
        res += "\n"
    return res

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

def value_iteration(problem):
    iterations, noise, livingReward, grid, discount = problem
    return_value = ''
    choices = {'N':[(-1,0), (0,1), (0,-1)], 'E':[(0,1), (1,0), (-1,0)], 'S':[(1,0), (0,-1), (0,1)], 'W':[(0,-1), (-1,0), (1,0)]}
    probs = (1-2*noise, noise, noise)
    grid_eval_cur = deepcopy(grid)
    policy = deepcopy(grid)

    #intialising for k=0
    for i in range(len(grid_eval_cur)):
        for j in range(len(grid_eval_cur[i])):
            if grid[i][j] == "#":
                grid_eval_cur[i][j] = "#####"
                policy[i][j] = "#"
            elif grid[i][j] not in ["#", "_", "S"]: 
                grid_eval_cur[i][j] = float(0)
                policy[i][j] = "x"
            else: 
                grid_eval_cur[i][j] = float(0)
                policy[i][j] = "_"
    return_value += "V_k=0\n" + print_grid(grid_eval_cur)
    
    #policy evaluation when k=1
    if iterations == 0: return return_value
    for i in range(len(grid_eval_cur)):
        for j in range(len(grid_eval_cur[i])):
            if grid[i][j] not in ["#", "_", "S"]: grid_eval_cur[i][j] = float(grid[i][j])
            elif grid_eval_cur[i][j] == "#####": pass
            else: 
                grid_eval_cur[i][j] = livingReward
                policy[i][j] = "N"
    return_value += "V_k=1\n" + print_grid(grid_eval_cur) + "pi_k=1\n" + print_policy(policy)
    grid_eval_prev = deepcopy(grid_eval_cur)

    #policy evaluation for k>=2
    for k in range(2, iterations):
        for i in range(len(grid_eval_cur)):
            for j in range(len(grid_eval_cur[i])):
                if policy[i][j] in ['#', "x"]: pass
                else:
                    max_v = float("-inf")
                    for dir in ["N", "E", "S", "W"]:
                        choice = choices[dir]
                        choice0 = (i+choice[0][0], j+choice[0][1])
                        choice0 = probs[0]*(livingReward+discount*grid_eval_prev[i][j]) if  choice0[0]<0 or choice0[1]<0 or choice0[0]>=len(grid) or choice0[1]>=len(grid[0]) or grid[choice0[0]][choice0[1]] == "#" else probs[0]*(livingReward+discount*grid_eval_prev[choice0[0]][choice0[1]]) 
                        choice1 = (i+choice[1][0], j+choice[1][1])
                        choice1 = probs[1]*(livingReward+discount*grid_eval_prev[i][j]) if  choice1[0]<0 or choice1[1]<0 or choice1[0]>=len(grid) or choice1[1]>=len(grid[0]) or grid[choice1[0]][choice1[1]] == "#" else probs[1]*(livingReward+discount*grid_eval_prev[choice1[0]][choice1[1]]) 
                        choice2 = (i+choice[2][0], j+choice[2][1])
                        choice2 = probs[2]*(livingReward+discount*grid_eval_prev[i][j]) if  choice2[0]<0 or choice2[1]<0 or choice2[0]>=len(grid) or choice2[1]>=len(grid[0]) or grid[choice2[0]][choice2[1]] == "#" else probs[2]*(livingReward+discount*grid_eval_prev[choice2[0]][choice2[1]]) 
                        v = choice0+choice1+choice2
                        if v > max_v:
                            max_v = v
                            max_dir = dir
                    grid_eval_cur[i][j] = max_v
                    policy[i][j] = max_dir
        return_value += f"V_k={k}\n" + print_grid(grid_eval_cur) + f"pi_k={k}\n" + print_policy(policy)
        grid_eval_prev = deepcopy(grid_eval_cur)
    return return_value[:-1]

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)