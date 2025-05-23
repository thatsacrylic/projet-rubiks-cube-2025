from modeleCube import Cube
#from reconnaissance_video_V1_8 import Reference_color

ref = (255, 0, 0)
#print(Reference_color)
class PointDeMesure:
    def __init__(self, pos, face_img, num_piece):
        self.position = pos
        self.face_img = face_img
        self.num_piece = num_piece
        
    def distance(self, point):
        #print(self.position, point.position)
        return ((self.position[0] - point.position[0])**2 + (self.position[1] - point.position[1])**2) ** 0.5

    def reconnaitre_couleur(self, ref):
        if co[0] < co[1] and co[0] < co[2] and co[0] < co[3] and co[0] < co[4] and co[0] < co[5]:
            result_co = co[0],"F"
        elif co[1] < co[0] and co[1] < co[2] and co[1] < co[3] and co[1] < co[4] and co[1] < co[5]:
            result_co = co[1],"R"
        elif co[2] < co[1] and co[2] < co[0] and co[2] < co[3] and co[2] < co[4] and co[2] < co[5]:
            result_co = co[2],"U"
        elif co[3] < co[1] and co[3] < co[2] and co[3] < co[0] and co[3] < co[4] and co[3] < co[5]:
            result_co = co[3],"B"
        elif co[4] < co[1] and co[4] < co[2] and co[4] < co[3] and co[4] < co[0] and co[4] < co[5]:
            result_co = co[4],"L"
        else:
            result_co = co[5],"D"
     
        return result_co

    def __repr__(self):
        return str(self.position)# + str(self.num_piece)
        
    def calc_dist_couleur(new_click):
        face = 'FRUBLD'
        co = []
    
        x, y = new_click  # Convertit les coordonnées en entiers
        r, v, b = 0, 0, 0
        px = image[x, y]
        R2 = int(px[0])
        G2 = int(px[1])
        B2 = int(px[2])
    
        for loop in range(6):
            couleurs = face[loop]
            #R1 = color.get(couleurs)[0]
            #G1 = color.get(couleurs)[1]
            #B1 = color.get(couleurs)[2]
            R1 = ref[0]
            G1 = ref[1]
            B1 = ref[2]
        
            if loop == 0:
                dist_F = sqrt((R2-R1)**2+(G2-G1)**2+(B2-B1)**2)
                co.append(dist_F)
            elif loop == 1:
                dist_R = sqrt((R2-R1)**2+(G2-G1)**2+(B2-B1)**2)
                co.append(dist_R)
            elif loop == 2:
                dist_U = sqrt((R2-R1)**2+(G2-G1)**2+(B2-B1)**2)
                co.append(dist_U)
            elif loop == 3:
                dist_B = sqrt((R2-R1)**2+(G2-G1)**2+(B2-B1)**2)
                co.append(dist_B)
            elif loop == 4:
                dist_L = sqrt((R2-R1)**2+(G2-G1)**2+(B2-B1)**2)
                co.append(dist_L)
            else:
                dist_D = sqrt((R2-R1)**2+(G2-G1)**2+(B2-B1)**2)
                co.append(dist_D)
        return co

        
p0u = PointDeMesure((195, 80), 0, 0)
p3u = PointDeMesure((220, 140), 0, 3)
p6u = PointDeMesure((270, 221), 0, 6)
p7u = PointDeMesure((400, 170), 0, 7)
p8u = PointDeMesure((500, 150), 0, 8)
p5u = PointDeMesure((435, 70), 0, 5)
p2u = PointDeMesure((390, 35), 0, 2)
p1u = PointDeMesure((280, 50), 0, 1)

p0f = PointDeMesure((300, 280), 1, 0)
p3f = PointDeMesure((310, 370), 1, 3)
p6f = PointDeMesure((310, 435), 1, 6)
p7f = PointDeMesure((400, 410), 1, 7)
p8f = PointDeMesure((500, 355), 1, 8)
p5f = PointDeMesure((500, 300), 1, 5)
p2f = PointDeMesure((520, 220), 1, 2)
p1f = PointDeMesure((420, 250), 1, 1)
lst_P = [p0u, p3u, p6u, p7u, p8u, p5u, p2u, p1u, p0f, p3f, p6f, p7f, p8f, p5f, p2f, p1f]

c = Cube()

c.cube['F'].setPiece(0, 'F')
