n1=int(input(""))
n2=int(input(""))
total=0
for i in range(n1,n2):
    total+=i
avg=total/(n2-n1)
print("avg",avg)