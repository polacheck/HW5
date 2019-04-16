


def eval_postfix(vartree, iterator):
    stack = linkedList()
    for token in iterator:
        if token.isalnum():
            stack.push(token)
        elif token == "=":
            right = stack.pop()
            left = stack.pop()
            if right[0].isalpha():
                right = vartree.lookup(right)
            vartree.assign(right, left)
            stack.push(right)
        else:
            right = stack.pop()
            left = stack.pop()
            if not right[0].isdigit():
                right = vartree.lookup(right)
            if not left[0].isdigit():
                left = vartree.lookup(left)
            stack.push(str(eval(str(left) + token + str(right))))
    value = str(stack.pop())
    if value[0].isalpha():
        return vartree.lookup(value)
    else:
        return value

def postfix_sum(iterator):
	yield from postfix_product(iterator)
	while peek(iterator) == '+' or peek(iterator) == '-':
		op = next(iterator)
		yield from postfix_product(iterator)
		yield op

def postfix_product(iterator):
	yield from postfix_factor(iterator)
	while peek(iterator) == '*' or peek(iterator) == '/' or peek(iterator) == '%':
		oper = next(iterator)
		yield from postfix_product(iterator)
		yield oper
       

def postfix_factor(iterator):
	if peek(iterator) == '(':
		next(iterator)
		yield from postfix_sum(iterator)
		next(iterator)
	else:
		yield next(iterator)

def to_postfix(expr):
	yield from postfix_sum(Peekable(new_split_iter(expr)))

class linkedList:
    """A simple singly linked list"""
    class Node:
        """A simple singly linked list node"""
        __slots__ = "_value","_next"
        def __init__(self, v, n):
            self._value = v
            self._next = n
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0
    def push(self,value):
        """Place a value at the front of the list"""
        self._head = linkedList.Node( value, self._head )
        if self._tail is None:      # empty list
            self._tail = self._head
        self._size += 1 
    def pop(self):
        """Retrieve a value from front of the list
        This implemenation assumes the list is not empty"""
        result = self._head._value
        self._head = self._head._next
        if self._head is None:      # now empty list
            self._tail = None
        self._size -= 1
        return result
    def __iter__(self):
        current = self._head
        while current is not None:
            yield current._value
            current = current._next
    def top(self):
        return self._head._value
    def is_empty(self):
        return self._head is None
    def __len__(self):
        return self._size
    def __str__(self):
        return ' '.join( iter(self) )

class Peekable():
    """An iterator with the ability to examine a value without advancement"""

    def __init__(self, iterator):
        """Take an existing iterator and add peek functionality
        iterator    -- the previous 'ordinary iterator
    """
        self._iterator = iterator;
        self._peeked = None

    #   the following two methods meet the protocol for iterators

    def __iter__(self):
        return self

    def __next__(self):
        """return the next element of the data (as would be expected)
    no advancement occurs if that element has already been peeked at
    """
        if self._peeked is None:
            self._peeked = next(self._iterator)
        ans = self._peeked
        self._peeked = None     # we don't yet see what comes next
        return ans

    def peek(self):
        """peek at the next element of the data
    only advancing if that next item has not yet been peeked at
    """
        if self._peeked is None:
            try:
                self._peeked = next(self._iterator)
            except StopIteration:
                self._peeked = None
        return self._peeked


# this function is defined just to allow similarity to next()
def peek(x):
    return x.peek()

def new_split_iter( expr ):   
   """divide a character string into individual tokens, which need not be separated by spaces (but can be!)
   also, the results are returned in a manner similar to iterator instead of a new data structure
   """
   expr = expr + ";"                # append new symbol to mark end of data, for simplicity
   pos = 0
   operatorLst = ["+", "-", "*", "/", "%", "(", ")", "=", ">", "<", "!", ":", "?"] # begin at first character position in the list

   while expr[pos] != ";": # repeat until the end of the input is found
      alnum = ""
      if expr[pos].isalnum():
         while expr[pos].isalnum():
            alnum += expr[pos]
            pos += 1
         yield alnum
      elif(expr[pos] in operatorLst) and (expr[pos+1] == "="):
         yield expr[pos] + expr[pos+1]
         pos += 2
      elif expr[pos] in operatorLst:
         yield expr[pos]
         pos += 1
      else:
         pos += 1

################################################ Here Down is Ours #####################
def findNextOpr(txt):
    """
        >>> findNextOpr('  3*   4 - 5')
        3
        >>> findNextOpr('8   4 - 5')
        6
        >>> findNextOpr('89 4 5')
        -1
    """
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
    """
        >>> isNumber('1   2 3')
        False
        >>> isNumber('-  156.3')
        False
        >>> isNumber('     29.99999999    ')
        True
        >>> isNumber('    5.9999x ')
        False
    """
    if not isinstance(txt, str) or len(txt)==0:
        return "error: isNumber"
    # --- YOU CODE STARTS HERE
    try:
        thenumber = float(txt)
        return(True)
    except ValueError:
        return(False)


def getNextNumber(expr, pos):
    """
        >>> getNextNumber('8  +    5    -2',0)
        (8.0, '+', 3)
        >>> getNextNumber('8  +    5    -2',4)
        (5.0, '-', 13)
        >>> getNextNumber('4.5 + 3.15         /  -5',20)
        (-5.0, None, None)
        >>> getNextNumber('4.5 + 3.15         /   5',10)
        (None, '/', 19)
    """

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
            while S is not empty:
                if precedence[opr] > precedence[S.peek()]:
                    break
                else:
                    postfix1.append(S.pop())
            S.push(opr)
        else:
            while S is not S.isEmpty():
                postfix.append(S.pop())
                return ' '.join(postfix)
        pos = oprPos+1




