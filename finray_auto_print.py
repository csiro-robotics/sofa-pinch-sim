import numpy as np
import json
from finray_design_auto import fin_design

init_points = 11  # number of initial points   10->30

# parameters = [ 120, 40, 30, 30, 1, 3, 1, 3, 10, 30]
#       l_w = input[1]
#     l_h = input[0]
#     l_tip=input[3]
#     l_hh=l_h-l_tip
#     l_t=input[2]
#     t_back = input[4]
#     t_flex = input[5]
#     t_rib = input[6]
#     n= np.rint(input[7]).astype(int)
#     d_agl = input[8]

def main():

    lower_bound = np.array([90, 28, 18, 20, 1, 1, 1, 1, -40])  # setting lower bound of solution
    upper_bound = np.array([100, 40, 30, 30, 3, 3, 3, 10, 40])

    # Randomly generate the initial trgx matrix
    trgx = lower_bound + np.random.rand(init_points, 9) * (upper_bound - lower_bound)
    trgx[:, 7] = np.rint(trgx[:, 7]).astype(int)

    

    # Save variable to a JSON file
    
         
    trgx_list = trgx.tolist()
    
    
    # with open('data/fingers/designs.json', 'w', newline='\n') as file:
        
    designs_dict = {}

    for i in range (0, init_points):
            design_name = i
            parameters = trgx[i,:]
            parameters_list = parameters.tolist()
            designs = {"B01G"+str(design_name): parameters_list}
            design_key = "B01G" + str(design_name)
            designs_dict[design_key] = parameters_list
            fin_design(parameters, design_name)

    with open('data/fingers/designs.json', 'w', newline='\n') as file:
        json.dump(designs_dict, file, indent=4)
       


    return 

# trgx_list = trgx.tolist()

# designs_dict = {}

# for i in range(init_points):
#     design_name = i
#     parameters = trgx[i,:]
#     parameters_list = parameters.tolist()
#     design_key = "B01G" + str(design_name)
#     designs_dict[design_key] = parameters_list
#     fin_design(parameters, design_name)

# with open('data/fingers/designs.json', 'w', newline='\n') as file:
#     json.dump(designs_dict, file)




if __name__ == "__main__":
    main()