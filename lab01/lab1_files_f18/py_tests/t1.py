#
#   t1.py, jfs9, 9/2/16:  simple python code to use some cpu time 
#

#prompt_text = "Enter a number: "
#user_in = input(prompt_text)
#user_num = int( user_in )
final_i = 700
final_j = 1000
k = 0

for i in range(1,final_i):
   for j in range(1,final_j):
       k = k + (i*j)

print("k = " + str(k) )
print("done....")
