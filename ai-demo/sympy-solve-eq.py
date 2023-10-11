from sympy import *

# 定义符号变量
x, y, z = symbols('x y z')

# 定义方程组
print("0, 原始方程组")
eq1 = Eq(4*x -2*y -6*z, 6)
eq2 = Eq(2*x -7*y +3*z, -3)
eq3 = Eq(-1*x +3*y -1*z, 1)
print(eq1.lhs , " = " , eq1.rhs)
print(eq2.lhs , " = " , eq2.rhs)
print(eq3.lhs , " = " , eq3.rhs)
print("")

# 化简方程组expr1, expr2, expr3
print("1 移项")
expr1 = eq1.lhs - eq1.rhs
expr2 = eq2.lhs - eq2.rhs
expr3 = eq3.lhs - eq3.rhs
print("[expr1] ", expr1, " = 0")
print("[expr2] ", expr2, " = 0")
print("[expr3] ", expr3, " = 0")
print("")

# # 通过消元过程得到化简后的方程组，并输出消元过程
print("2 消元")

print("2.1, expr1 和 expr2 消 x 得到 expr4")
expr4 = expr2 - expr1*expr2.coeff(x)/expr1.coeff(x)
print("[expr4] ", expr4, " = 0")
print("")

print("2.2, expr1 和 expr3 消 x 得到 expr5")
expr5 = expr3 - expr1*expr3.coeff(x)/expr1.coeff(x)
print("[expr5] ", expr5, " = 0")
print("")

print("2.3, expr4 和 expr5 消 y 得到 expr6")
expr6 = expr5 - expr4*expr5.coeff(y)/expr4.coeff(y)
print("[expr6] ", expr6, " = 0")
print("")


# 解方程组
sol = solve((eq1, eq2, eq3), (x, y, z))

# 输出解向量
print("3 求解")
print(sol)

if len(sol) == 3:
    print("该方程组有唯一解，解为：", sol)
elif len(sol) == 0:
    print("该方程组无解")
else:
    print("该方程组有无数解")





# import numpy as np
# np.set_printoptions(precision=4)
# # 系数矩阵
# A = np.array([[2, -7, 5], [-1, -3, 1], [3, -4, 4]])

# # 常数矩阵
# B = np.array([-4, -4, -1])

# # 解方程组
# # X = np.linalg.solve(A, B)
# # LU分解
# P, L, U = scipy.linalg.lu(A)

# # 解方程组
# Y = np.dot(np.linalg.inv(P@L), B)
# X = np.dot(np.linalg.inv(U), Y)

# # 判断解的情况
# detA = np.linalg.det(A)
# print("det A", detA)
# if int(detA) == 0:
#     value = B.dot(np.linalg.inv(A))
#     print("B/A", value)
#     # if value.all() == np.zeros(value.shape):
#     #     print("该方程组有无数解")
#     # else:
#     #     print("该方程组无解")
# else:
#     print("该方程组有唯一解，解为：", X)