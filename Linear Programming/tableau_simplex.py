import sys

def tableau_simplex(num_of_decision_variables, num_of_constraints, cj, LHS, RHS):
    """
    Perform the Simplex algorithm using the tableau method to solve a linear programming problem.

    Parameters:
    num_of_decision_variables (int): The number of decision variables in the problem.
    num_of_constraints (int): The number of constraints in the problem.
    cj (list of float): The objective function coefficients.
    LHS (list of list of float): The left hand side matrix of the constraints.
    RHS (list of float): The right hand side vector of the constraints.

    Returns:
    decision_variables (list of float): The optimal values of the decision variables.
    objective_value (float): The optimal value of the objective function.
    """

    objective_value = 0

    # list to store basic variables (starting with slack variables)
    basic_variables = []

    # initialise basic variables as the slack variable
    for i in range(num_of_constraints):
        basic_variables.append(i + num_of_decision_variables)

    while True:
        net_evaluation = calculate_cj_zj(LHS, basic_variables, cj)

        # if all values in the net evaluation are <= 0, we have an optimal solution
        if max(net_evaluation) <= 0:
            break

        # determine the entering variable (the one with the largest positive net evaluation)
        entering_variable = net_evaluation.index(max(net_evaluation))

        # calculate theta (RHS / LHS) for all rows to determine the leaving variable
        theta = []
        for i in range(num_of_constraints):
            LHS_value = LHS[i][entering_variable]
            if LHS_value > 0:
                theta.append(RHS[i] / LHS_value)
            else:
                # infeasible direction
                theta.append(float("inf"))

        # determine the leaving variable (row with the smallest theta)
        leaving_variable = theta.index(min(theta))

        # update the basic variables: replace the leaving variable with the entering variable
        basic_variables[leaving_variable] = entering_variable

        # update the table with the new basic variables
        LHS, RHS = update_table(LHS, RHS, leaving_variable, entering_variable)

        # update the objective value using the new basic variables
        row_sum = 0
        for i in range(num_of_constraints):
            row_sum += cj[basic_variables[i]] * RHS[i]

        objective_value = row_sum

    # extract the values of the decision variables from the final table
    decision_variables = [0] * num_of_decision_variables

    # loop over constraints to update decision variable values
    for i in range(num_of_constraints):
        if basic_variables[i] < num_of_decision_variables:
            decision_variables[basic_variables[i]] = RHS[i]

    return decision_variables, objective_value

def calculate_cj_zj(LHS, basic_variables, cj):
    """
    Calculate the net evaluation row (Cj - Zj) for the Simplex tableau.

    Parameters:
    LHS (list of list of float): The left hand side matrix of the constraints.
    basic_variables (list of int): The indices of the current basic variables.
    cj (list of float): The coefficients of the objective function for each variable.

    Returns:
    list of float: The net evaluation row (Cj - Zj), used to determine the entering variable.
    """

    net_evaluation = [0] * len(cj)

    # loop through each variable to calculate cj - zj
    for j in range(len(cj)):
        zj = 0

        # dot product between the coefficients of the basic variables (cj[basic_variables[i]])
        # and the corresponding column of LHS (LHS[i][j])
        for i in range(len(basic_variables)):
            zj += cj[basic_variables[i]] * LHS[i][j]

        # calculate the net evaluation cj - zj for the current variable
        net_evaluation[j] = cj[j] - zj

    return net_evaluation

def update_table(LHS, RHS, leaving_variable, entering_variable):
    """
    Update the Simplex tableau after selecting the entering and leaving variables.

    This function performs the pivot operation in the Simplex algorithm. It updates the 
    LHS matrix and RHS vector by making the rest of the column corresponding to the entering 
    variable zero, except for the pivot row.

    Parameters:
    LHS (list of list of float): The left hand side matrix of the constraints.
    RHS (list of float): The righ -hand side vector of the constraints.
    leaving_variable (int): The index of the leaving variable (row).
    entering_variable (int): The index of the entering variable (column).

    Returns:
    tuple: Updated LHS and RHS after performing row operations.
    """

    # get the coefficient from the leaving variable's row and entering variable's column
    divide_coefficient = LHS[leaving_variable][entering_variable]

    # divide the entire row by the coefficient  
    for i in range(len(LHS[leaving_variable])):
        LHS[leaving_variable][i] = LHS[leaving_variable][i] / divide_coefficient

    # adjust RHS for the leaving variable's row
    RHS[leaving_variable] = RHS[leaving_variable] / divide_coefficient

    # perform row operations to make the rest of the entering column zero
    for i in range(len(LHS)):
        # skip the row of the leaving variable
        if i == leaving_variable:
            continue

        # get the coefficient for the row operation
        row_coefficient = LHS[i][entering_variable]

        # update each element in the row by subtracting the scaled values from the active row
        for j in range(len(LHS[i])):
            LHS_value = LHS[i][j]
            pivot_row_value = LHS[leaving_variable][j]
            
            LHS[i][j] = LHS_value - row_coefficient * pivot_row_value

        # update RHS 
        RHS[i] -= row_coefficient * RHS[leaving_variable]

    return LHS, RHS

def read_file(file_path: str):
    """
    Read the input file for a linear programming problem and extract the number of decision variables, 
    number of constraints, objective function coefficients, left hand side matrix (LHS) and 
    right hand side vector (RHS).

    Parameters:
    file_path (str): Path to the input file.

    Returns:
    tuple: A tuple containing the number of decision variables, number of constraints, 
           the list of objective function coefficients (cj), LHS, and RHS.
    """

    f = open(file_path, "r")
    
    # number of decision variables
    f.readline()
    num_of_decision_variables = int(f.readline().strip())

    # number of constraints
    f.readline()
    num_of_constraints = int(f.readline().strip())

    # objective function
    f.readline()
    cj = f.readline().strip()
    cj_list = cj.split(", ")

    # convert to float
    for i in range(len(cj_list)):
        cj_list[i] = float(cj_list[i])

    # add zeros to the objective function coefficients list for the slack variables
    cj_list += num_of_constraints * [0.0]

    # LHS
    f.readline()

    LHS = []
    for i in range(num_of_constraints):
        row = []

        line = f.readline().strip()
        split_values = line.split(", ")

        # convert to float
        for value in split_values:
            row.append(float(value))

        # add slack variables (zeros for all other rows, 1 for the current row)
        row += num_of_constraints * [0.0]
        
        # add 1.0 for the slack variable
        row[i + num_of_decision_variables] = 1.0
        
        LHS.append(row)

    # RHS
    f.readline()

    RHS = []
    for i in range(num_of_constraints):
        line = f.readline().strip()

        # convert to float
        RHS.append(float(line))

    return num_of_decision_variables, num_of_constraints, cj_list, LHS, RHS

def write_file(file_name, decision_variables, objective_value):
    """
    Write the optimal decision variables and the optimal objective function value to a file.

    Parameters:
    file_name (str): The name of the output file.
    decision_variables (list of float): The optimal values of the decision variables.
    objective_value (float): The optimal value of the objective function.
    """

    with open(file_name, "w") as f:
        f.write(f"# Optimal_Values_of_Decision_Variables\n{decision_variables}\n")
        f.write(f"# Optimal_Value_of_Objective_Function\n{objective_value}\n")

if __name__ == "__main__":
    # run --> python tableau_simplex.py [FILENAME.txt]

    LP = sys.argv[1]
    num_of_decision_variables, num_of_constraints, cj_list, LHS, RHS = read_file(LP)
    decision_variables, objective_value = tableau_simplex(num_of_decision_variables, num_of_constraints, cj_list, LHS, RHS)
    write_file("output q2.txt", decision_variables, objective_value)