import MapReduce
import sys

"""
Matrix Multiplication Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):

    #as recommended in the course, dimensions are hardcoded 
    #(two passes can't be done in the toy example)
    k = [0,1,2,3,4]

    if record[0] == "a":
        for N  in k:
            key = tuple((record[1], N))
            value = record
            print key, value
            mr.emit_intermediate(key, value)
            
    if record[0] == "b":
        for L in k:
            for N in k:
                if record[2] == L:
                    key = tuple((N, L))
                    value = record
                    print key, value
                    mr.emit_intermediate(key, value)
                    

def reducer(key, list_of_values):

    total = 0
    for i in list_of_values:
        for j in list_of_values:
            print i, j
            if i[0] == "a" and j[0] == "b":
                if i[2] == j[1]:
                    total+= i[3]*j[3]

    mr.emit((key[0], key[1], total))


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open('matrix.json')
  mr.execute(inputdata, mapper, reducer)
