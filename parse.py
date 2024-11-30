def read_grid_mdp_problem_p1(file_path):
    #Your p1 code here
    with open(file_path, 'r') as file:
        line_number = -1
        grid = []
        policy = []
        for line in file:
            lst_line = line.split()
            # print(lst_line)
            if not lst_line: pass
            elif lst_line[0] == "seed:": seed = int(lst_line[1])
            elif lst_line[0] == "noise:": noise = float(lst_line[1])
            elif lst_line[0] == "livingReward:": livingReward = float(lst_line[1])
            else: grid.append(lst_line)
            line_number+=1
        policy = grid[len(grid)//2+1:]
        grid = grid[1:len(grid)//2]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == "S": start = (i,j)
    problem = (seed, noise, livingReward, grid, policy, start)
    return problem

def read_grid_mdp_problem_p2(file_path):
    with open(file_path, 'r') as file:
        line_number = -1
        grid = []
        policy = []
        for line in file:
            lst_line = line.split()
            # print(lst_line)
            if not lst_line: pass
            elif lst_line[0] == "discount:": discount = float(lst_line[1])
            elif lst_line[0] == "noise:": noise = float(lst_line[1])
            elif lst_line[0] == "livingReward:": livingReward = float(lst_line[1])
            elif lst_line[0] == "iterations:": iterations = int(lst_line[1])
            else: grid.append(lst_line)
            line_number+=1
        policy = grid[len(grid)//2+1:]
        grid = grid[1:len(grid)//2]
        # for i in range(len(grid)):
        #     for j in range(len(grid[i])):
        #         if grid[i][j] == "S": start = (i,j)
    problem = (iterations, noise, livingReward, grid, policy, discount)
    return problem

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here
    with open(file_path, 'r') as file:
        line_number = -1
        grid = []
        for line in file:
            lst_line = line.split()
            # print(lst_line)
            if not lst_line: pass
            elif lst_line[0] == "discount:": discount = float(lst_line[1])
            elif lst_line[0] == "noise:": noise = float(lst_line[1])
            elif lst_line[0] == "livingReward:": livingReward = float(lst_line[1])
            elif lst_line[0] == "iterations:": iterations = int(lst_line[1])
            else: grid.append(lst_line)
            line_number+=1
        grid = grid[1:]
        # for i in range(len(grid)):
        #     for j in range(len(grid[i])):
        #         if grid[i][j] == "S": start = (i,j)
    problem = (iterations, noise, livingReward, grid, discount)
    return problem