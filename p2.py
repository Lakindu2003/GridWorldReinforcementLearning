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

def policy_evaluation(problem):
    iterations, noise, livingReward, grid, policy, discount = problem
    return_value = ''
    choices = {'N':[(-1,0), (0,1), (0,-1)], 'E':[(0,1), (1,0), (-1,0)], 'S':[(1,0), (0,-1), (0,1)], 'W':[(0,-1), (-1,0), (1,0)]}
    probs = (1-2*noise, noise, noise)
    grid_eval_cur = deepcopy(grid)

    #intialising for k=0
    for i in range(len(grid_eval_cur)):
        for j in range(len(grid_eval_cur[i])):
            grid_eval_cur[i][j] = float(0) if grid[i][j] != "#" else "#####"
    return_value += "V^pi_k=0\n" + print_grid(grid_eval_cur)
    
    #policy evaluation when k=1
    if iterations == 0: return return_value
    for i in range(len(grid_eval_cur)):
        for j in range(len(grid_eval_cur[i])):
            if policy[i][j] == "exit": grid_eval_cur[i][j] = float(grid[i][j])
            elif grid_eval_cur[i][j] == "#####": pass
            else: grid_eval_cur[i][j] = livingReward
    return_value += "V^pi_k=1\n" + print_grid(grid_eval_cur)
    grid_eval_prev = deepcopy(grid_eval_cur)

    #policy evaluation for k>=2
    for k in range(2, iterations):
        for i in range(len(grid_eval_cur)):
            for j in range(len(grid_eval_cur[i])):
                if policy[i][j] in ['#', "exit"]: pass
                else:
                    choice = choices[policy[i][j]]
                    choice0 = (i+choice[0][0], j+choice[0][1])
                    choice0 = probs[0]*(livingReward+discount*grid_eval_prev[i][j]) if  choice0[0]<0 or choice0[1]<0 or choice0[0]>=len(grid) or choice0[1]>=len(grid[0]) or grid[choice0[0]][choice0[1]] == "#" else probs[0]*(livingReward+discount*grid_eval_prev[choice0[0]][choice0[1]]) 
                    choice1 = (i+choice[1][0], j+choice[1][1])
                    choice1 = probs[1]*(livingReward+discount*grid_eval_prev[i][j]) if  choice1[0]<0 or choice1[1]<0 or choice1[0]>=len(grid) or choice1[1]>=len(grid[0]) or grid[choice1[0]][choice1[1]] == "#" else probs[1]*(livingReward+discount*grid_eval_prev[choice1[0]][choice1[1]]) 
                    choice2 = (i+choice[2][0], j+choice[2][1])
                    choice2 = probs[2]*(livingReward+discount*grid_eval_prev[i][j]) if  choice2[0]<0 or choice2[1]<0 or choice2[0]>=len(grid) or choice2[1]>=len(grid[0]) or grid[choice2[0]][choice2[1]] == "#" else probs[2]*(livingReward+discount*grid_eval_prev[choice2[0]][choice2[1]]) 
                    grid_eval_cur[i][j] = choice0+choice1+choice2
        return_value += f"V^pi_k={k}\n" + print_grid(grid_eval_cur)
        grid_eval_prev = deepcopy(grid_eval_cur)
    return return_value[:-1]

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)