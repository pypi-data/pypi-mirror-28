while 1:
    print ('输入black变黑色')
    print ('输入red变红色')
    print ('输入green变绿色')
    print ('输入yellow变黄色')
    print ('输入blue变蓝色')
    print ('输入fuchsia变紫红色')
    print ('输入cyan变青蓝色')
    print ('输入white变白色')
    print ('输入ret变回默认设置')
    print ('输入exit退出')
    color = input('您想让文字变成什么颜色? ')
    print ('')
    if color == 'black':
        print ('\033[1;30;40m')
        print ('修改成功！')
        print ('')
    elif color == 'red':
        print ('\033[1;31;40m')
        print ('修改成功！')
        print ('')
    elif color == 'green':
        print ('\033[1;32;40m')
        print ('修改成功！')
        print ('')
    elif color == 'yellow':
        print ('\033[1;33;40m')
        print ('修改成功！')
        print ('')
    elif color == 'blue':
        print ('\033[1;34;40m')
        print ('修改成功！')
        print ('')
    elif color == 'fuchsia':
        print ('\033[1;35;40m')
        print ('修改成功！')
        print ('')
    elif color == 'cyan':
        print ('\033[1;36;40m')
        print ('修改成功！')
        print ('')
    elif color == 'white':
        print ('\033[1;37;40m')
        print ('修改成功！')
        print ('')
    elif color == 'ret':
        print ('\033[0m')
        print ('还原成功！')
        print ('')
    elif color == 'exit':
        exit()
    else:
        print ('您的输入有误，请重新输入')
        print ('')