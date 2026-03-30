stack = []
capacity = 5
def isFull():
    if len(stack) == capacity:
        return True
    else:
        return False
def push(data):
    if isFull():
        print("stack is full")
    else:
        stack.append(data)
print(f'[[정수형 스택 연산 실습(용량:{capacity})]]')
def isEmpty():
    if not stack:
        return True
    else:
        return False
def pop():
    if isEmpty():
        print()
    else:
        return stack.pop()
def peak():
    return stack[-1]
while True:
    menu = int(input())
    if menu == 0:
        break
    elif menu == 1:
        data = int(input())
        push(data)
    elif menu ==2:
        data = pop()
        print(data)
    elif menu == 3:
        data=peak()
        print(data)
print("[[정수형 스택 연산 실습 종료]]")