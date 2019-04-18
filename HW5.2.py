"""
def findNextOpr(txt):
    if not isinstance(txt,str) or len(txt)<=0:
        return "error: findNextOpr"

    # --- YOU CODE STARTS HERE
    txtlist = []
    count = 0
    count2 = 0
    breaker = 0
    while count < len(txt):
        txtlist.append(txt[count])
        count = count + 1
    try:
        while breaker != 1:
             if txtlist[count2] == '+' or txtlist[count2] == '-' or txtlist[count2] == '*' or txtlist[count2] == '/' or txtlist[count2] == '^':
                 breaker = 1
                 position = count2
             count2 = count2 + 1
    except IndexError:
        position = -1
    if breaker == 0:
        position = -1
    return(position)



def isNumber(txt):
    if not isinstance(txt, str) or len(txt)==0:
        return "error: isNumber"
    # --- YOU CODE STARTS HERE
    try:
        thenumber = float(txt)
        return(True)
    except ValueError:
        return(False)


def getNextNumber(expr, pos):
    if not isinstance(expr, str) or not isinstance(pos, int) or len(expr)==0 or pos<0 or pos>=len(expr):
        return None, None, "error: getNextNumber"
    # --- YOU CODE STARTS HERE

    ################################
    subexpression = expr[pos:].strip()
    if subexpression[0] == '-':
        posofminus = expr.find('-',0)
        oprPos = findNextOpr(expr[posofminus+1:])
        if oprPos != -1:
            oprPos = oprPos + posofminus + 1 - pos
    else:
        oprPos = findNextOpr(expr[pos:])

    if oprPos != -1:
        oprPos = oprPos + pos
        nextOpr = expr[oprPos]
        newNumber = expr[pos:oprPos]
    else:
        nextOpr = None
        oprPos = None
        newNumber = expr[pos:]
    if isNumber(newNumber) is True:
        return float(newNumber), nextOpr, oprPos
    else:
        return None, nextOpr, oprPos
"""
"""
class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "{}".format(self.value) 

    __repr__ = __str__
                          

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__

    def isEmpty(self):
        return(self.top is None)

    def __len__(self):
        return(self.count)
    
    def peek(self):
        if self.top == None:
            return None
        else:
            return(self.top)
   
    def push(self,value):
        new = Node(value)
        self.top = new.next
        self.top = new
        self.count = self.count + 1
        return


    def pop(self):
        if self.top is None:
            return None
        else:
            topval = self.top
            self.top = self.top.next
            self.count = self.count - 1
            return(topval.value)
"""
"""
def postfix(expr):
    number, opr, oprPos = getNextNumber(expr, 0)
    if number is None:
        return "invalid"
    elif opr is None:
        return number
    pos = oprPos + 1
    S = Stack()
    postfix = []
    postfix = [str(number)]
    S.push(opr)
    precedence={'+':1,'-':1,'*':2,'/':2,'^':3}
    while True:
        number, opr, oprPos = getNextNumber(expr, pos)
        if opr is None and number is None:
            return postfix
        postfix.append(str(number))
        if opr is not None:
            while S is not S.isEmpty():
                if precedence[str(opr)] > precedence[str(S.peek())]:
                    break
                else:
                    postfix.append(S.pop())
            S.push(opr)
        else:
            while S is not S.isEmpty():
                postfix.append(S.pop())
                return ' '.join(postfix)
        pos = oprPos+1
"""
def postfix(expr):
    openP = expr.count('(')
    closeP = expr.count(')')
    if openP != closeP:
        return "error, invalid expression parenthesis"

    if not isinstance(expr, str) or len(expr) == 0:
        return "error, invalid expression length"

    precedence={'+':1,'-':1,'*':2,'/':2,'^':3,'(':0,')':0}
    printable = ''
    pos = 0

    opStack = Stack()

    while True:
        #print("1")
        try:
            validation = getNextNumber(expr, pos)
            #print("3")
            currNum, currOp, opPos = getNextNumber(expr, pos)
            print("fuck", currNum, currOp, opPos)
        except:
            return "error, invalid expression 1"

        if currNum == None:
            print(currNum, currOp, opPos)
            return "error, invalid expression 2"

        else:
            if currOp == None:
                if currNum != None:
                    printable += str(currNum) + " "

                    while opStack.isEmpty() == False:
                        if opStack.peek() != "(":
                            printable += opStack.pop() + " "
                        else:
                            opStack.pop()
                break
            else:
                operators = ['+','-','*','/','^']
                if expr[-1] in operators:
                    return "error, invalid expression 3"
                currNum = validation[0]
                currOp = validation[1]
                initPos = pos
                pos = validation[2] + 1
                
        if currNum != None:
            if len(printable) == 0:
                printable = str(currNum) + " "
            else:
                printable += str(currNum) + " "
        if '(' in expr[initPos:opPos]:
            numParenthesis = expr[initPos:opPos].count("(")
            for paren in range(numParenthesis):
                opStack.push('(')
        if ')' in expr[initPos:opPos]:
            numclosed = expr[initPos:opPos].count(")")
            for count in range(numclosed):
                while opStack.peek() != '(':
                    printable = printable + str(opStack.pop()) + " "
                opStack.pop()

        if currOp != None:
            if opStack.isEmpty():
                opStack.push(currOp)
            else:
                
                while (precedence[str(currOp)] <= precedence[str(opStack.peek())]):
                    #print(currNum, currOp, opStack.peek())
                    printable = printable + str(opStack.pop()) + " "

                    if opStack.peek() == None:
                        break
                opStack.push(currOp)
    printable = printable.strip()

    return printable
                
    




def calculator(expr):
    if not isinstance(expr, str) or len(expr) <= 0:
        return 'input error in calculation'

    expr = expr.strip()
    s = Stack()

    pos = expr.find('(')
    while True:
        if pos == -1:
            if expr.find(')') == -1:
                if s.isEmpty():
                    return evaluate(expr)
                else:
                    return 'error 1'
            else:
                if s.isEmpty():
                    return 'error 2'
                else:
                    x = s.pop()
                    y = expr.find(')')
                    expr = expr[:x] + str(evaluate(expr[x+1:y])) + expr[y+1:]
        else:
            if expr[pos:].find(')') == -1:
                return 'error 4'
            else:
                if expr[pos+1].find('(') == -1:
                    expr = expr[:pos] + str(evaluate(expr[pos+1:expr[pos+1].find(")")+pos+1]))+expr[expr[pos+1:].find(")")+pos+2:]

                    if s.isEmpty():
                        pos-=1
                    else:
                        pos = s.pop()
                else:
                    if expr[pos+1].find(')')>expr[pos+1:].find('('):
                        s.push(pos)
                        pos = pos + 1 + expr[pos+1:].find('(')
                    else:
                        expr = expr[:pos] + str(evaluate(expr[pos+1:expr[pos+1].find(")")+pos+1]))+expr[expr[pos+1:].find(")")+pos+2:] 
                        if s.isEmpty():
                            pos = pos + 1 + expr[pos+1:].find('(')
                        else:
                            pos = s.pop()
#"""

def evaluate(expr):
    if len(expr) <= 0 or not isinstance(expr,str):
        return "input error A"
    expr = expr.strip()
    if expr[0] == "-":
        expr = "0 " + expr
    newNumber, newOpr, oprPos = getNextNumber(expr, 0)

    if newNumber is None:
        return "Input error B"
    elif newOpr is None:
        return newNumber
    elif newOpr == "+" or newOpr == "-":
        mode = "add"
        addResult = newNumber
    elif newOpr == "*" or newOpr == "/":
        mode = "mul"
        addResult = 0
        mulResult = newNumber
        addLastOpr = "+"
    elif newOpr == "^":
        mode = "exp"
        addResult = 0
        mulResult = 1
        addLastOpr = "+"
        mulLastOpr = "*"
        expResult = newNumber
        LastOpr = None
    pos = oprPos + 1
    opr = newOpr
    
    while True:
        newNumber, newOpr, oprPos = getNextNumber(expr,pos)
        if newNumber is None:
            return "error message"
        elif mode == "add":
            if newOpr is None:
                return exeOpr(addResult, opr, newNumber)
            elif newOpr == "+" or newOpr == "-":
                addResult = exeOpr(addResult, opr, newNumber)
            elif newOpr == "*" or newOpr == "/":
                mode = "mul"
                mulResult = newNumber
                addLastOpr = opr
                LastOpr = opr
            elif newOpr == "^":
                mode = "exp"
                expResult = newNumber
                addLastOpr = opr
                LastOpr = opr
        elif mode == "mul":
            if newOpr is None:
                mulResult = exeOpr(mulResult, opr, newNumber)
                return exeOpr(addResult, addLastOpr, mulResult)
            elif newOpr == "+" or newOpr == "-":
                mode = "add"
                mulResult = exeOpr(mulResult, opr, newNumber)
                addResult = exeOpr(addResult, addLastOpr, mulResult)
            elif newOpr == "*" or newOpr == "/":
                mulResult = exeOpr(mulResult, opr, newNumber)
            elif newOpr == "^":
                mode = "exp"
                expResult = newNumber
                mulLastOpr = opr
                LastOpr = opr
        elif mode == "exp":
            expResult = exeOpr(expResult, opr, newNumber)
            if newOpr is None:
                if LastOpr == "*" or LastOpr == "/" or LastOpr == None:
                    mulResult = exeOpr(mulResult, mulLastOpr, expResult)
                    return exeOpr(addResult, addLastOpr, mulResult)
                if LastOpr == "+" or LastOpr == "-":
                    return exeOpr(addResult, addLastOpr, expResult)
            elif newOpr == "*" or newOpr == "/":
                mode = "mul"
                if LastOpr == "*" or LastOpr == "/":
                    mulResult = exeOpr(mulResult, mulLastOpr, expResult)
                else:
                    mulResult = expResult
            elif newOpr == "+" or newOpr == "-":
                mode = "add"
                if LastOpr == "*" or LastOpr == "/":
                    addResult = exeOpr(mulResult, mulLastOpr, expResult)
                elif LastOpr == "+" or LastOpr == "-":
                    addResult = exeOpr(addResult, addLastOpr, expResult)
                else:
                    addResult = expResult
        opr = newOpr
        pos = oprPos + 1


def exeOpr(num1, opr, num2):
    if opr == "+":
        return num1 + num2
    elif opr == "-":
        return num1 - num2
    elif opr == "*":
        return num1 * num2
    elif opr == "/":
        if num2 == 0:
            return "error"
        else:
            return num1 / num2
    elif opr == "^":
        return num1 ** num2
    else:
        return "error"
    
def findNextOpr(txt):

    if not isinstance(txt,str) or len(txt)<=0:
        return "error: findNextOpr"

    # --- YOU CODE STARTS HERE
    operator = ['+', '-', '^', '/', '*']
    for n in range(len(txt)):

        if txt[n] in operator:

            #if txt[n] == '-':

                #if txt[n+1] != " ":
                    #continue
            return n
    return -1

def isNumber(txt):

    if not isinstance(txt, str) or len(txt)==0:
        return "error: isNumber"
    # --- YOU CODE STARTS HERE
    StripTxt = txt.strip()
    try:
        test = float(StripTxt)
        return True
    except:
        return False

def getNextNumber(expr, pos):

    if not isinstance(expr, str) or not isinstance(pos, int) or len(expr)==0 or pos<0 or pos>=len(expr):
        return None, None, "error: getNextNumber"
    # --- YOU CODE STARTS HERE
    expr.strip('(')
    expr.strip(')')
    newExpr = expr[pos:]
    operPos = findNextOpr(newExpr)
    subExpr = newExpr.strip()


    if subExpr[0] == '-':
        minus_pos = findNextOpr(newExpr) + pos
        operPos = findNextOpr(expr[(minus_pos+1):])


        if operPos != -1:
            operPos = operPos + minus_pos + 1 - pos

    else:
        operPos = findNextOpr(expr[pos:])

    if operPos != -1:
        operPos = operPos + pos
        newOper = expr[operPos]
        newNumber = expr[pos:operPos]

    else:
        operPos = None
        newOper = None
        newNumber = expr[pos:]


    if isNumber(newNumber):
        return float(newNumber), newOper, operPos
    else:
        return None, newOper, operPos


def calculator2(expr):
    L = []
    L = expr.split(" ")
    print(expr)
    S = Stack()
    for a in L:
        if isNumber(a) is True:
            a = float(a)
            S.push(a)
            print(S)
        
        
        #op1, op2 = S.pop(), S.pop()

        if a == '+':
            print("+")
            op1, op2 = S.pop(), S.pop()
            S.push(op2 + op1)
        elif a == '-':
            print("-")
            op1, op2 = S.pop(), S.pop()
            S.push(op2 - op1)
        elif a == '*':
            print("*")
            op1, op2 = S.pop(), S.pop()
            S.push(op2 * op1)
        elif a == '/':
            print("/")
            op1, op2 = S.pop(), S.pop()
            if op1 == 0:
                return "error division by zero"
            else:
                S.push(op2 / op1)
        elif a == '^':
            print("^")
            op1, op2 = S.pop(), S.pop()
            S.push(op2 ** op1)

    return S.pop()

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return "Node({})".format(self.value)

    __repr__ = __str__


class Stack:

    def __init__(self):
        self.top = None
        self.count = 0

    def __str__(self):
        temp = self.top
        out = []
        while temp:
            out.append(str(temp.value))
            temp = temp.next
        out = '\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top, out))

    __repr__ = __str__

    def isEmpty(self):
        # write your code here
        if not self.top:
            return True
        else:
            return False

    def __len__(self):
        # write your code here
        curr = self.top

        while curr:
            self.count += 1
            curr = curr.next

    def peek(self):
        # write your code here
        if self.isEmpty():
            return None
        else:
            return self.top.value

    def push(self, value):
        # write your code here
        new_node = Node(value)
        self.count += 1

        if self.isEmpty():
            self.top = new_node
            return
        else:
            curr = self.top
            last = None

            while curr.value > new_node.value:
                last = curr
                curr = curr.next

                if not curr: break

            if not last:
                new_node.next = self.top
                self.top = new_node
                return

            if curr:
                last.next = new_node
                new_node.next = curr
            return

    def pop(self):
        # write your code here
        if self.isEmpty():
            return None

        else:
            curr = self.top.value
            self.top = self.top.next
            return curr
