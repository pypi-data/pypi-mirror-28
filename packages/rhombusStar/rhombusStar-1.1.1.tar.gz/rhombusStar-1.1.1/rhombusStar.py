# 打印菱形
def printRhombus():
   count = 1    # 每行星星数
   num=4        # 星星个数
   total=0      # 星星打印行数     
   while total<7:
        print(' ' * num + '*' * count)  #打印星星与空格    
        total+=1
        # 根据行数判断打印星星与空格
        if(total<4):
            count+=2
            num-=1
        else:
            count-=2
            num+=1

printRhombus()