# opcode for different instruction
opcode_dict = {"add": "00000", "sub": "00001", "movImm": "00010", "mov": "00011", "ld": "00100", "st": "00101", "mul": "00110", "div": "00111", "rs": "01000", "ls": "01001",
               "xor": "01010", "or": "01011", "and": "01100", "not": "01101", "cmp": "01110", "jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111", "hlt": "11010"}
# variable names as defined in given instruction
variables = []
# dictionary : key ->variable || value-> memory address of variable that assign at last
variables_dict = {}
# bit used in register
register_add = {"R0": "000", "R1": "001", "R2": "010", "R3": "011",
                "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
#  these are some operation that help in  to define address of insruction after so that we can allocate memory to variables
address = "0000000"
ser_no = 0
# dictionary key->instruction like(ld,st) and value->list of address,corrospend terms for all different types
main_dict = {}
#  this function help in finding address and immediate value
# to solve problem of label
# list of label declaration
label_ls = []
label_dict = {}


def binary_add(address, val):
    summ = int(address)
    a = bin(summ + val)
    a = str(a[2:])
    b = a  # decide what to do when this value is more than 7.
    while (len(b) != 7):
        b = "0"+b
    return b


def Doer(line):
    global ser_no
    global hlt_check
    global hlt_check_last
    global error_check
    if ":" not in line:
        if not line.isspace() and line != '':
            # i = line.split(" ")
            i = [s for s in line.split() if s]
            if (i[0] in opcode_dict.keys()):
                flag = False
                if (len(i) > 4):
                    # syntax error
                    error_check = True
                    print(f"(line no. {line_no})Invalid Instruction format.")
                # type A
                elif (len(i) == 4):
                    i[3] = i[3].strip()
                    if (i[1] in register_add.keys() and i[2] in register_add.keys() and i[3] in register_add.keys()):
                        if (i[1] != "FLAGS" and i[2] != "FLAGS" and i[3] != "FLAGS"):
                            if (i[0] == "add"):
                                main_dict[binary_add(address, ser_no)] = ["add", binary_add(
                                    address, ser_no), opcode_dict["add"]+"00"+register_add[i[1]] + register_add[i[2]]+register_add[i[3]]]
                                ser_no += 1
                            elif (i[0] == "sub"):
                                main_dict[binary_add(address, ser_no)] = ["sub", binary_add(
                                    address, ser_no), opcode_dict["sub"]+"00"+register_add[i[1]] + register_add[i[2]]+register_add[i[3]]]
                                ser_no += 1
                            elif (i[0] == "mul"):
                                main_dict[binary_add(address, ser_no)] = ["mul", binary_add(
                                    address, ser_no), opcode_dict["mul"]+"00"+register_add[i[1]] + register_add[i[2]]+register_add[i[3]]]
                                ser_no += 1
                            elif (i[0] == "xor"):
                                main_dict[binary_add(address, ser_no)] = ["xor", binary_add(
                                    address, ser_no), opcode_dict["xor"]+"00"+register_add[i[1]] + register_add[i[2]]+register_add[i[3]]]
                                ser_no += 1
                            elif (i[0] == "or"):
                                main_dict[binary_add(address, ser_no)] = ["or", binary_add(
                                    address, ser_no), opcode_dict["or"]+"00"+register_add[i[1]] + register_add[i[2]]+register_add[i[3]]]
                                ser_no += 1
                            elif (i[0] == "and"):
                                main_dict[binary_add(address, ser_no)] = ["and", binary_add(
                                    address, ser_no), opcode_dict["and"]+"00"+register_add[i[1]] + register_add[i[2]]+register_add[i[3]]]
                                ser_no += 1
                            else:
                                # syntax error
                                error_check = True
                                print(
                                    f"(line no. {line_no})Invalid instruction format.")
                        else:
                            # error
                            error_check = True
                            print(
                                f"(line no. {line_no})Invalid use of FLAGS registor.")
                    else:
                        # syntax error
                        error_check = True
                        print(
                            f"(line no. {line_no})Invalid registor name given.")

                # type B and type C and type D
                if (len(i) == 3):
                    i[2] = i[2].strip()
                    if (i[1] in register_add.keys()):
                        if (i[1] != 'FLAGS'):
                            if ('$' in i[2]):
                                if (i[2][1:].isdigit() and int(i[2][1:]) <= 127 and int(i[2][1:]) >= 0):
                                    if (i[0] == "mov"):
                                        main_dict[binary_add(address, ser_no)] = ["movImm", binary_add(
                                            address, ser_no), opcode_dict["movImm"]+"0"+register_add[i[1]] + binary_add("0", int(i[2][1:]))]
                                        # We stored this instruction as "movImm", but the input instruction is just "mov".
                                        ser_no += 1
                                        flag = True
                                    elif (i[0] == "rs"):
                                        main_dict[binary_add(address, ser_no)] = ["rs", binary_add(
                                            address, ser_no), opcode_dict["rs"]+"0"+register_add[i[1]] + binary_add("0", int(i[2][1:]))]
                                        ser_no += 1
                                        flag = True
                                    elif (i[0] == "ls"):
                                        main_dict[binary_add(address, ser_no)] = ["ls", binary_add(
                                            address, ser_no), opcode_dict["ls"]+"0"+register_add[i[1]] + binary_add("0", int(i[2][1:]))]
                                        ser_no += 1
                                        flag = True
                                else:
                                    # error
                                    error_check = True
                                    print(
                                        f"(line no. {line_no})Invalid Immediate value given.")
                                    flag = True

                            else:
                                if (i[0] == "mov"):
                                    if (i[2] in register_add.keys()):
                                        if (i[2] != 'FLAGS'):
                                            main_dict[binary_add(address, ser_no)] = ["mov", binary_add(
                                                address, ser_no), opcode_dict["mov"]+"00000"+register_add[i[1]] + register_add[i[2]]]
                                            ser_no += 1
                                            flag = True
                                        else:
                                            # error
                                            error_check = True
                                            print(
                                                f"(line no. {line_no})Invalid use of FLAGS registor.")
                                            flag = True
                                    else:
                                        # error
                                        error_check = True
                                        print(
                                            f"(line no. {line_no})Invalid Registor name.")
                                        flag = True

                                elif (i[0] == "div"):
                                    if (i[2] in register_add.keys()):
                                        if (i[2] != 'FLAGS'):
                                            main_dict[binary_add(address, ser_no)] = ["div", binary_add(
                                                address, ser_no), opcode_dict["div"]+"00000"+register_add[i[1]] + register_add[i[2]]]
                                            ser_no += 1
                                            flag = True
                                        else:
                                            # error
                                            error_check = True
                                            print(
                                                f"(line no. {line_no})Invalid use of FLAGS registor.")
                                            flag = True
                                    else:
                                        # error
                                        error_check = True
                                        print(
                                            f"(line no. {line_no})Invalid Registor name.")
                                        flag = True

                                elif (i[0] == "not"):
                                    if (i[2] in register_add.keys()):
                                        if (i[2] != 'FLAGS'):
                                            main_dict[binary_add(address, ser_no)] = ["not", binary_add(
                                                address, ser_no), opcode_dict["not"]+"00000"+register_add[i[1]] + register_add[i[2]]]
                                            ser_no += 1
                                            flag = True
                                        else:
                                            # error
                                            error_check = True
                                            print(
                                                f"(line no. {line_no})Invalid use of FLAGS registor.")
                                            flag = True
                                    else:
                                        # error
                                        error_check = True
                                        print(
                                            f"(line no. {line_no})Invalid Registor name.")
                                        flag = True

                                elif (i[0] == "cmp"):
                                    if (i[2] in register_add.keys()):
                                        if (i[2] != 'FLAGS'):
                                            main_dict[binary_add(address, ser_no)] = ["cmp", binary_add(
                                                address, ser_no), opcode_dict["cmp"]+"00000"+register_add[i[1]] + register_add[i[2]]]
                                            ser_no += 1
                                            flag = True
                                        else:
                                            # error
                                            error_check = True
                                            print(
                                                f"(line no. {line_no})Invalid use of FLAGS registor.")
                                            flag = True
                                    else:
                                        # error
                                        error_check = True
                                        print(
                                            f"(line no. {line_no})Invalid Registor name.")
                                        flag = True

                                elif (i[0] == "ld"):
                                    main_dict[binary_add(address, ser_no)] = ["ld", binary_add(
                                        address, ser_no), opcode_dict["ld"]+"0"+register_add[i[1]], i[2]]
                                    ser_no += 1
                                    flag = True
                                elif (i[0] == "st"):
                                    main_dict[binary_add(address, ser_no)] = ["st", binary_add(
                                        address, ser_no), opcode_dict["st"]+"0"+register_add[i[1]], i[2]]
                                    ser_no += 1
                                    flag = True
                        else:
                            # error
                            error_check = True
                            print(
                                f"(line no. {line_no})Invalid use of FLAGS registor.")
                            flag = True
                    else:
                        # error
                        error_check = True
                        print(f"(line no. {line_no})Invalid Registor name.")
                        flag = True

                    if (flag == False):
                        # syntax error
                        error_check = True
                        print(
                            f"(line no. {line_no})Invalid Instruction Format.")
                # Type E
                if (len(i) == 2):
                    i[1] = i[1].strip()
                    if (i[0] == "jmp"):
                        main_dict[binary_add(address, ser_no)] = ["jmp", binary_add(
                            address, ser_no), opcode_dict["jmp"] + "0000", i[1]]
                        label_ls.append(i[1])
                        ser_no += 1
                    elif (i[0] == "jlt"):
                        main_dict[binary_add(address, ser_no)] = ["jlt", binary_add(
                            address, ser_no), opcode_dict["jlt"] + "0000", i[1]]
                        label_ls.append(i[1])
                        ser_no += 1
                    elif (i[0] == "jgt"):
                        main_dict[binary_add(address, ser_no)] = ["jgt", binary_add(
                            address, ser_no), opcode_dict["jgt"] + "0000", i[1]]
                        label_ls.append(i[1])
                        ser_no += 1
                    elif (i[0] == "je"):
                        main_dict[binary_add(address, ser_no)] = ["je", binary_add(
                            address, ser_no), opcode_dict["je"] + "0000", i[1]]
                        label_ls.append(i[1])
                        ser_no += 1
                    else:
                        # syntax error
                        error_check = True
                        print(
                            f"(line no. {line_no})Invalid Instruction Format.")
                # Type F
                if (len(i) == 1):
                    if (i[0] == "hlt"):
                        main_dict[binary_add(address, ser_no)] = ["hlt", binary_add(
                            address, ser_no), opcode_dict["hlt"]+"00000000000"]
                        ser_no += 1
                        hlt_check = True
                        hlt_check_last = True
                    else:
                        # syntax error
                        error_check = True
                        print(
                            f"(line no. {line_no})Invalid Instruction Format.")

            else:
                # error
                error_check = True
                print(
                    f"(line no. {line_no})Check Instruction name, not found in ISA.")
    else:  # Define this properly
        label_line = line.split(":")
        label_line[0] = label_line[0].lstrip()
        if label_line[0][-1] == ' ':
            # error
            error_check = True
            print(
                f"(line no. {line_no})Space between Label name and ':' not allowed.")
        else:
            label_line[1] = label_line[1].strip()
            label_dict[label_line[0]] = binary_add(address, ser_no)
            Doer(label_line[1])
        # function call!!!
        # Put entire label_line[1] in the function. next two lines are not required as we called the function.
        # main_dict[binary_add(address,ser_no)] = [label_line[1],binary_add(address,ser_no),opcode_dict["hlt"]+"00000000000"]
        # ser_no +=1


# print(register_add)
hlt_check = False
hlt_check_last = False
var_check = False
error_check = False
line_no = 0
with open("inputfile.txt", "r+") as f:
    for line in f.readlines():
        line_no += 1
        line = line.strip()
        if line[:3] == 'var':
            if (var_check == False):
                i = line.split()
                i[1] = i[1].strip()
                variables.append(i[1])
            else:
                i = line.split()
                i[1] = i[1].strip()
                print(
                    f"(line no. {line_no})Varibale {i[1]} declared in between instructions. Wont be included in the code varibales.")
        elif line != '':
            if var_check == False:
                line2_no = line_no+1
            var_check = True
            hlt_check_last = False
            Doer(line)

if (hlt_check == False):
    # error
    error_check = True
    print(f"(line no. {line_no})No hlt instruction found in the input file.")
elif (hlt_check_last == False):
    # error
    error_check = True
    print(f"(line no. {line_no})No hlt instruction at the end found.")

for i in variables:
    variables_dict[i] = binary_add(address, ser_no)
    ser_no += 1
# print(register_add)
# print(main_dict)
# print(label_ls)
# print(label_dict)
# print(variables_dict)

with open('output.txt', 'w') as ff:
    if (error_check == True):
        ff.write(
            "Errors have been found in the Assembler. Refer to Terminal for Errors.")
        ff.write("\n")
    for inst in main_dict.keys():
        line2_no += 1
        if (main_dict[inst][0] == 'ld' or main_dict[inst][0] == "st"):
            # print(main_dict[inst][2] +variables_dict[main_dict[inst][3]])
            # print("\n")
            if (main_dict[inst][3] in variables_dict.keys()):
                ff.write(main_dict[inst][2] +
                         variables_dict[main_dict[inst][3]])
                ff.write("\n")
            elif (main_dict[inst][3] in label_dict.keys()):
                print(
                    f"(line no. {line2_no})Label name '{main_dict[inst][3]}' used as a varibale.")
                ff.write(
                    "Errors have been found in the Assembler. Refer to Terminal for Errors.")
                ff.write("\n")
            else:
                # syntax error
                print(
                    f"(line no. {line2_no})Undeclared variable '{main_dict[inst][3]}' used.")
                ff.write(
                    "Errors have been found in the Assembler. Refer to Terminal for Errors.")
                ff.write("\n")
        elif (main_dict[inst][0] == "jmp" or main_dict[inst][0] == 'jlt' or main_dict[inst][0] == 'jgt' or main_dict[inst][0] == "je"):
            # print(main_dict[inst][2] + main_dict[x][1])
            # print("\n")
            if (main_dict[inst][3] in label_dict.keys()):
                ff.write(main_dict[inst][2] + label_dict[main_dict[inst][3]])
                ff.write("\n")
            elif (main_dict[inst][3] in variables_dict.keys()):
                print(
                    f"(line no. {line2_no})Variable name '{main_dict[inst][3]}' used as a Label.")
                ff.write(
                    "Errors have been found in the Assembler. Refer to Terminal for Errors.")
                ff.write("\n")
            else:
                # syntax error
                print(
                    f"(line no. {line2_no})Undefined Label '{main_dict[inst][3]}' used.")
                ff.write(
                    "Errors have been found in the Assembler. Refer to Terminal for Errors.")
                ff.write("\n")

        else:
            # print(main_dict[inst][2])
            # print("\n")
            ff.write(main_dict[inst][2])
            ff.write("\n")
