from z3 import * 




# rows in a matrix represents time slots
# colums in a matrix represent candidates
# '1' in matrix represents candidate available in particular time slot
# '0' in matrix represents candidate not available in particular time slot


slot_matric = []
num_rows = int(input("Enter the size of square matrix: "))
print("row values separated by spaces example as:1 0 0 .Values can be only 0 or 1")
for i in range(num_rows):
    row = input(f"Enter row-{i + 1} values : ").split()
    row = [int(value) for value in row]
    slot_matric.append(row)

def find_slots(slot_matric):
    pairs={}
    possible_pairs=[]
    for i in range(len(slot_matric)):
        temp=[]
        for j in range(len(slot_matric[0])):
            if(slot_matric[i][j]==1):
                pairs[(i,j)]=Bool(f"ts{i}_c{j}")
                temp.append((i,j))
            else:
                pairs[(i,j)]=False
        possible_pairs.append(temp)

    solver=Solver()
    keys_list=list(pairs.keys())
    value_list=list(pairs.values())


    #adding constraints for each candidate to schedule in atleast one timeslot and atmost one timeslot
    for candidate in range(len(slot_matric[0])):
        tlist=[pairs[slot,candidate] for slot in range(len(slot_matric))] 
        solver.add( AtMost(*tlist,1) )
        solver.add(Or([pairs[slot,candidate] for slot in range(len(slot_matric))]))

    #adding constriant for all given true entries to be either true or false
    solver.add(Or([p for p in value_list]))

    #adding constraint for each timeslot to be scheduled for atleast one candidate and atmost one candidate
    for i in range(len(possible_pairs)):
        zlist=[pairs[possible_pairs[i][j]] for j in range(len(possible_pairs[i]))]
        if(len(zlist)>0):
            solver.add(AtMost(*zlist,1))
            solver.add(Or([pairs[possible_pairs[i][j]] for j in range(len(possible_pairs[i]))]))
    #print(solver)
    #print(solver.check())
    #print(solver.model())
    solver.check()
    if(str(solver.check())=="sat"):
        print("\nts{x}-represents time slots and c{x} represents candidate\n")
        listofMaxes=[]
        results=[]
        while solver.check() == sat:
            model = solver.model()
            print(model)
            print("\n")
            results.append(model)
            solver.add( Not(    And([v() == model[v] for v in model])   )  )
    else:
        print("No satisfying assignments")

find_slots(slot_matric)