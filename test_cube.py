from modeleCube import Cube
from robotCube import Robot


c = Cube()

'''
suite: cube totalement résolut
'''

c.cube['F'].setPiece(0, 'F')
c.cube['F'].setPiece(1, 'F')
c.cube['F'].setPiece(2, 'F')
c.cube['F'].setPiece(3, 'F')
c.cube['F'].setPiece(5, 'F')
c.cube['F'].setPiece(6, 'F')
c.cube['F'].setPiece(7, 'F')
c.cube['F'].setPiece(8, 'F')
c.cube['U'].setPiece(0, 'U')
c.cube['U'].setPiece(1, 'U')
c.cube['U'].setPiece(2, 'U')
c.cube['U'].setPiece(3, 'U')
c.cube['U'].setPiece(5, 'U')
c.cube['U'].setPiece(6, 'U')
c.cube['U'].setPiece(7, 'U')
c.cube['U'].setPiece(8, 'U')
print(c)
c.rotations("R L' D U' F B' R L'")
print(c)
c.cube['F'].setPiece(0, 'D')
c.cube['F'].setPiece(1, 'D')
c.cube['F'].setPiece(2, 'D')
c.cube['F'].setPiece(3, 'D')
c.cube['F'].setPiece(5, 'D')
c.cube['F'].setPiece(6, 'D')
c.cube['F'].setPiece(7, 'D')
c.cube['F'].setPiece(8, 'D')
c.cube['U'].setPiece(0, 'L')
c.cube['U'].setPiece(1, 'L')
c.cube['U'].setPiece(2, 'L')
c.cube['U'].setPiece(3, 'L')
c.cube['U'].setPiece(5, 'L')
c.cube['U'].setPiece(6, 'L')
c.cube['U'].setPiece(7, 'L')
c.cube['U'].setPiece(8, 'L')
print(c)
c.rotations("R L' D U' F B' R L'")
print(c)
c.cube['F'].setPiece(0, 'R')
c.cube['F'].setPiece(1, 'R')
c.cube['F'].setPiece(2, 'R')
c.cube['F'].setPiece(3, 'R')
c.cube['F'].setPiece(5, 'R')
c.cube['F'].setPiece(6, 'R')
c.cube['F'].setPiece(7, 'R')
c.cube['F'].setPiece(8, 'R')
c.cube['U'].setPiece(0, 'B')
c.cube['U'].setPiece(1, 'B')
c.cube['U'].setPiece(2, 'B')
c.cube['U'].setPiece(3, 'B')
c.cube['U'].setPiece(5, 'B')
c.cube['U'].setPiece(6, 'B')
c.cube['U'].setPiece(7, 'B')
c.cube['U'].setPiece(8, 'B')
print(c)
c.rotations("R L' D U' F B' R L'")
print(c)

'''
suite: cube résolut avec une pièce sur deux d'inversée
'''
'''
c.cube['F'].setPiece(0, 'F')
c.cube['F'].setPiece(1, 'F')
c.cube['F'].setPiece(2, 'F')
c.cube['F'].setPiece(3, 'F')
c.cube['F'].setPiece(5, 'F')
c.cube['F'].setPiece(6, 'F')
c.cube['F'].setPiece(7, 'F')
c.cube['F'].setPiece(8, 'F')
c.cube['U'].setPiece(0, 'U')
c.cube['U'].setPiece(1, 'U')
c.cube['U'].setPiece(2, 'U')
c.cube['U'].setPiece(3, 'U')
c.cube['U'].setPiece(5, 'U')
c.cube['U'].setPiece(6, 'U')
c.cube['U'].setPiece(7, 'U')
c.cube['U'].setPiece(8, 'U')
print(c)
c.rotations("R2 L2 D2 U2 F2 B2")
print(c)
c.cube['F'].setPiece(0, 'F')
c.cube['F'].setPiece(1, 'B')
c.cube['F'].setPiece(2, 'F')
c.cube['F'].setPiece(3, 'B')
c.cube['F'].setPiece(5, 'B')
c.cube['F'].setPiece(6, 'F')
c.cube['F'].setPiece(7, 'B')
c.cube['F'].setPiece(8, 'F')
c.cube['U'].setPiece(0, 'U')
c.cube['U'].setPiece(1, 'D')
c.cube['U'].setPiece(2, 'U')
c.cube['U'].setPiece(3, 'D')
c.cube['U'].setPiece(5, 'D')
c.cube['U'].setPiece(6, 'U')
c.cube['U'].setPiece(7, 'D')
c.cube['U'].setPiece(8, 'U')
print(c)
c.rotations("R L' D U' F B' R L'")
print(c)
c.cube['F'].setPiece(0, 'D')
c.cube['F'].setPiece(1, 'U')
c.cube['F'].setPiece(2, 'D')
c.cube['F'].setPiece(3, 'U')
c.cube['F'].setPiece(5, 'U')
c.cube['F'].setPiece(6, 'D')
c.cube['F'].setPiece(7, 'U')
c.cube['F'].setPiece(8, 'D')
c.cube['U'].setPiece(0, 'L')
c.cube['U'].setPiece(1, 'R')
c.cube['U'].setPiece(2, 'L')
c.cube['U'].setPiece(3, 'R')
c.cube['U'].setPiece(5, 'R')
c.cube['U'].setPiece(6, 'L')
c.cube['U'].setPiece(7, 'R')
c.cube['U'].setPiece(8, 'L')
print(c)
c.rotations("R L' D U' F B' R L'")
print(c)
c.cube['F'].setPiece(0, 'R')
c.cube['F'].setPiece(1, 'L')
c.cube['F'].setPiece(2, 'R')
c.cube['F'].setPiece(3, 'L')
c.cube['F'].setPiece(5, 'L')
c.cube['F'].setPiece(6, 'R')
c.cube['F'].setPiece(7, 'L')
c.cube['F'].setPiece(8, 'R')
c.cube['U'].setPiece(0, 'B')
c.cube['U'].setPiece(1, 'F')
c.cube['U'].setPiece(2, 'B')
c.cube['U'].setPiece(3, 'F')
c.cube['U'].setPiece(5, 'F')
c.cube['U'].setPiece(6, 'B')
c.cube['U'].setPiece(7, 'F')
c.cube['U'].setPiece(8, 'B')
print(c)
c.rotations("R L' D U' F B' R L'")
print(c)
'''
