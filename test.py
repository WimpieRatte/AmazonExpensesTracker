import re
# def phone_verification():

#     x = True

#     while x == True: 
#         phone = input("Enter your national phone number with country code: ")

#         pattern = r"^+49|0049 [1-9]{1,4} [1-9]{1,12}$" 
#         print(re.match(pattern, phone))
#         #phone_check = bool(re.match(pattern, phone))
#         # if phone_check == True:
#         #     print ("Your phone number is correct")
#         #     break
#         # else:
#         #     print("your phone number is not valid")

# phone_verification()


import re
string_5 = "+265 0899654937ffff"
# Check for international code in front of telephone number:
pattern_5 = "^(\+|(00))[\s]*[^0][\s0-9\(\)]*"  
    # prefix either + or 00
    # followed by 0 or more whitespace
    # NOT allowed to be followed by a 0
    # followed by any number, white space or brackets
result_5 = re.sub(string=string_5, pattern=pattern_5, repl="")
print(result_5)
if len(result_5) > 0:
    print("invalid number")


result_5b = re.search(string=string_5b, pattern=pattern_5)
print(result_5)
print(result_5b)