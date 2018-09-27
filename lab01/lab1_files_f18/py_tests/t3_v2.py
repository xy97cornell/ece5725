#
# jfs9 2/13/17: modifications for exception check in python 2
#
prompt_text = "Enter a number: "

is_number = False

while not is_number:
    is_number = True
    try:
        user_num = int( raw_input (prompt_text) )
    except ValueError:
        print ("That is not a number.  Please enter a number")
        is_number = False
for i in range(1,10):
    print str(i) + " times " + str(user_num) + " is " + str(i*user_num)

even = (user_num % 2) == 0
print(" ")
if even:
    print str(user_num) + " is even"
else:
    print str(user_num) + " is odd"
