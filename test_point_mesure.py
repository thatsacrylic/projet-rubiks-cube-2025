from modeleCube import Cube

ref_couleur = {'F': (255, 0, 0)}

class PointDeMesure:
    def __init__(self, pos, face_img, num_piece):
        self.position = pos
        self.face_img = face_img
        self.num_piece = num_piece
        
    def distance(self, point):
        #print(self.position, point.position)
        return ((self.position[0] - point.position[0])**2 + (self.position[1] - point.position[1])**2) ** 0.5

    def reconnaitre_couleur(self, image, ref):
        return 'F'

    def __repr__(self):
        return 'Point : ' + str(self.position) + 'piece ' + str(self.num_piece)
        
        
        
p1 = PointDeMesure((125, 45), 0, 1)
p2 = PointDeMesure((45, 44), 1, 3)
p3 = PointDeMesure((74, 325), 0, 7)
lst_P = [p1, p2, p3]

c = Cube()