for i in range(1,8,2):                  # 拆成两步打印；range(1,8,2)表示从1到8，间隔2，不包含8
    print((i*'*').center(7))            # str.center(n,'$')长度为n的新字符串，其中str居中，第二个参数为填充字符，默认空格
for i in range(1,6,2):
    print(((6-i)*'*').center(7))
