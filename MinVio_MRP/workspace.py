# -*- coding: utf-8 -*-

from shapely.geometry import Polygon, Point
import numpy as np
import matplotlib.pyplot as plt

import datetime
from landmark_motion import lm_motion

def get_label(x, workspace):
    """
    generating the label of position component
    """
    point = Point(x)
    # whether x lies within obstacle
    for (obs, boundary) in iter(workspace.obs.items()):
        if point.within(boundary):
            return obs

    # whether x lies within regions
    # for (region, boundary) in iter(workspace.regions.items()):
    #     if point.within(boundary):
    #         return region
    # x lies within unlabeled region
    return ''




class Workspace(object):
    """
    define the workspace where robots reside
    """
    def __init__(self):
        # dimension of the workspace
        self.length = 150
        self.width = 150
        self.workspace = (self.length, self.width)
        
        
        """ Case 1 """
        
        # self.length = 120
        # self.width = 85
        # self.workspace = (self.length, self.width)
        # self.obs = {'o1': Polygon([(60, 3), (60, 55), (62, 55), (62, 3)]),
        #                 'o2': Polygon([(70, 60), (70, 62), (115, 62), (115, 60)])
        #                 } 
        # self.padded_obs={}
        # self.pad_obstacle(3)
        # center = [(50, 30), (90, 20), (110,40), (62,57),(60,60)]
        
        
        # l1_obj = lm_motion([center[0][0], center[0][1]], func=2, vel = 0, direction =  np.pi/2, dist = 20)
        # l2_obj = lm_motion([center[1][0], center[1][1]], func=2, vel = 0, direction =  -np.pi/2, dist = 25)
        # l3_obj = lm_motion([center[2][0], center[2][1]], func=2, vel = 0, direction =  np.pi/2, dist = 21)
        # l4_obj = lm_motion([center[3][0], center[3][1]], func=2, vel = 0, direction =  -np.pi/2, dist = 20)
                                 
        
        # self.landmark= {'l1': [[center[0][0], center[0][1]],  [[6, 0], [0, 4]], l1_obj],
        #                 'l2': [[center[1][0], center[1][1]],  [[7, 0], [0, 7]], l2_obj],
        #                 'l3': [[center[2][0], center[2][1]],  [[3, 0], [0, 3]], l3_obj],
        #                 'l4': [[center[3][0], center[3][1]],  [[3, 0], [0, 3]], l4_obj]
        #                 }
        
        
        """ Scalability test"""
        self.length = 200
        self.width = 200
        self.workspace = (self.length, self.width)
        self.obs = {'o1': Polygon([(25, 80), (25, 81), (70, 81), (70, 80)]),
                        'o2': Polygon([(100, 15), (100, 80), (101, 80), (101, 15)]),
                        'o3': Polygon([(130, 80), (130, 81), (180, 81), (180, 80)]),
                        'o4': Polygon([(100, 160), (100, 185), (101, 185), (101, 160)]),
                        'o5': Polygon([(40, 145), (40, 146), (140, 146), (140, 145)]),
                        # 'o6': Polygon([(50, 25), (50, 55), (51, 55), (51, 25)]),
                        # 'o7': Polygon([(30, 170), (30, 171), (70, 171), (70, 170)]),
                        # 'o8': Polygon([(110, 160), (110, 161), (180, 161), (180, 160)]),
                        # 'o9': Polygon([(160, 20), (160, 60), (161, 60), (161, 20)]),
                        # 'o10': Polygon([(145, 90), (145, 120), (146, 120), (146, 90)]),
                        # 'o11': Polygon([(55, 90), (55, 120), (56, 120), (56, 90)]),
                        # 'o12': Polygon([(100, 90), (100, 120), (101, 120), (101, 90)])
                        } 
        
        self.padded_obs={}
        self.pad_obstacle(3)
        center = [(10.9, 19.9), (9.9, 49.8), (112.2, 42.9), (153.0, 15.7), (99.9, 136.2), (51.2, 190.7), (156.7, 190.7), (183.9, 176.9), (22.2, 181.9), (79.2, 181.5), (29.0, 127.2), (62.1, 127.7), (46.1, 108.6), (66.6, 17.2), (159.7, 74.9), (184.3, 75.8), (173.0, 60.3), (184.8, 45.5), (75.5, 105.8), (20.0, 105.6), (51.3, 173.9), (93.1, 27.5), (150.5, 60.1), (169.9, 39.4), (41.4, 67.3), (76.6, 68.2), (138.7, 36.0), (89.7, 91.4), (131.3, 124.2), (174.8, 126.1), (166.3, 174.2), (127.4, 176.9), (79.1, 155.3), (23.1, 155.3), (23.6, 13.5), (22.4, 45.7), (61.0, 56.7), (125.8, 88.4), (155.8, 114.5), (88.6, 125.7), (181.4, 148.6), (145.0, 167.9), (61.1, 186.2), (19.8, 139.2)]
        l1_obj = lm_motion([center[0][0], center[0][1]], func=2, vel=0, direction=0, dist=0)
        l2_obj = lm_motion([center[1][0], center[1][1]], func=2, vel=0, direction=0, dist=0)
        l3_obj = lm_motion([center[2][0], center[2][1]], func=2, vel=0, direction=0, dist=0)
        l4_obj = lm_motion([center[3][0], center[3][1]], func=2, vel=0, direction=0, dist=0)
        l5_obj = lm_motion([center[4][0], center[4][1]], func=2, vel=0, direction=0, dist=0)
        l6_obj = lm_motion([center[5][0], center[5][1]], func=2, vel=0, direction=0, dist=0)
        l7_obj = lm_motion([center[6][0], center[6][1]], func=2, vel=0, direction=0, dist=0)
        l8_obj = lm_motion([center[7][0], center[7][1]], func=2, vel=0, direction=0, dist=0)
        l9_obj = lm_motion([center[8][0], center[8][1]], func=2, vel=0, direction=0, dist=0)
        l10_obj = lm_motion([center[9][0], center[9][1]], func=2, vel=0, direction=0, dist=0)
        l11_obj = lm_motion([center[10][0], center[10][1]], func=2, vel=0, direction=0, dist=0)
        l12_obj = lm_motion([center[11][0], center[11][1]], func=2, vel=0, direction=0, dist=0)
        l13_obj = lm_motion([center[12][0], center[12][1]], func=2, vel=0, direction=0, dist=0)
        l14_obj = lm_motion([center[13][0], center[13][1]], func=2, vel=0, direction=0, dist=0)
        l15_obj = lm_motion([center[14][0], center[14][1]], func=2, vel=0, direction=0, dist=0)
        l16_obj = lm_motion([center[15][0], center[15][1]], func=2, vel=0, direction=0, dist=0)
        l17_obj = lm_motion([center[16][0], center[16][1]], func=2, vel=0, direction=0, dist=0)
        l18_obj = lm_motion([center[17][0], center[17][1]], func=2, vel=0, direction=0, dist=0)
        l19_obj = lm_motion([center[18][0], center[18][1]], func=2, vel=0, direction=0, dist=0)
        l20_obj = lm_motion([center[19][0], center[19][1]], func=2, vel=0, direction=0, dist=0)
        l21_obj = lm_motion([center[20][0], center[20][1]], func=2, vel=0, direction=0, dist=0)
        l22_obj = lm_motion([center[21][0], center[21][1]], func=2, vel=0, direction=0, dist=0)
        l23_obj = lm_motion([center[22][0], center[22][1]], func=2, vel=0, direction=0, dist=0)
        l24_obj = lm_motion([center[23][0], center[23][1]], func=2, vel=0, direction=0, dist=0)
        l25_obj = lm_motion([center[24][0], center[24][1]], func=2, vel=0, direction=0, dist=0)
        l26_obj = lm_motion([center[25][0], center[25][1]], func=2, vel=0, direction=0, dist=0)
        l27_obj = lm_motion([center[26][0], center[26][1]], func=2, vel=0, direction=0, dist=0)
        l28_obj = lm_motion([center[27][0], center[27][1]], func=2, vel=0, direction=0, dist=0)
        l29_obj = lm_motion([center[28][0], center[28][1]], func=2, vel=0, direction=0, dist=0)
        l30_obj = lm_motion([center[29][0], center[29][1]], func=2, vel=0, direction=0, dist=0)
        l31_obj = lm_motion([center[30][0], center[30][1]], func=2, vel=0, direction=0, dist=0)
        l32_obj = lm_motion([center[31][0], center[31][1]], func=2, vel=0, direction=0, dist=0)
        l33_obj = lm_motion([center[32][0], center[32][1]], func=2, vel=0, direction=0, dist=0)
        l34_obj = lm_motion([center[33][0], center[33][1]], func=2, vel=0, direction=0, dist=0)
        l35_obj = lm_motion([center[34][0], center[34][1]], func=2, vel=0, direction=0, dist=0)
        l36_obj = lm_motion([center[35][0], center[35][1]], func=2, vel=0, direction=0, dist=0)
        l37_obj = lm_motion([center[36][0], center[36][1]], func=2, vel=0, direction=0, dist=0)
        l38_obj = lm_motion([center[37][0], center[37][1]], func=2, vel=0, direction=0, dist=0)
        l39_obj = lm_motion([center[38][0], center[38][1]], func=2, vel=0, direction=0, dist=0)
        l40_obj = lm_motion([center[39][0], center[39][1]], func=2, vel=0, direction=0, dist=0)
        l41_obj = lm_motion([center[40][0], center[40][1]], func=2, vel=0, direction=0, dist=0)
        l42_obj = lm_motion([center[41][0], center[41][1]], func=2, vel=0, direction=0, dist=0)
        l43_obj = lm_motion([center[42][0], center[42][1]], func=2, vel=0, direction=0, dist=0)
        l44_obj = lm_motion([center[43][0], center[43][1]], func=2, vel=0, direction=0, dist=0)
        self.landmark= {'l1': [[center[0][0], center[0][1]],  [[6, 0], [0, 4]], l1_obj],
                        'l2': [[center[1][0], center[1][1]],  [[3, 0], [0, 3]], l2_obj],
                        'l3': [[center[2][0], center[2][1]],  [[3, 0], [0, 3]], l3_obj],
                        'l4': [[center[3][0], center[3][1]],  [[3, 0], [0, 3]], l4_obj],
                        'l5': [[center[4][0], center[4][1]],  [[3, 0], [0, 3]], l5_obj],
                        'l6': [[center[5][0], center[5][1]],  [[3, 0], [0, 3]], l6_obj],
                        'l7': [[center[6][0], center[6][1]],  [[3, 0], [0, 3]], l7_obj],
                        'l8': [[center[7][0], center[7][1]],  [[3, 0], [0, 3]], l8_obj],
                        'l9': [[center[8][0], center[8][1]],  [[3, 0], [0, 3]], l9_obj],
                        'l10': [[center[9][0], center[9][1]],  [[3, 0], [0, 3]], l10_obj],
                        'l11': [[center[10][0], center[10][1]],  [[3, 0], [0, 3]], l11_obj],
                        'l12': [[center[11][0], center[11][1]],  [[3, 0], [0, 3]], l12_obj],
                        'l13': [[center[12][0], center[12][1]],  [[3, 0], [0, 3]], l13_obj],
                        'l14': [[center[13][0], center[13][1]],  [[3, 0], [0, 3]], l14_obj],
                        'l15': [[center[14][0], center[14][1]],  [[3, 0], [0, 3]], l15_obj],
                        'l16': [[center[15][0], center[15][1]],  [[3, 0], [0, 3]], l16_obj],
                        'l17': [[center[16][0], center[16][1]],  [[3, 0], [0, 3]], l17_obj],
                        'l18': [[center[17][0], center[17][1]],  [[3, 0], [0, 3]], l18_obj],
                        'l19': [[center[18][0], center[18][1]],  [[3, 0], [0, 3]], l19_obj],
                        'l20': [[center[19][0], center[19][1]],  [[3, 0], [0, 3]], l20_obj],
                        'l21': [[center[20][0], center[20][1]],  [[3, 0], [0, 3]], l21_obj],
                        'l22': [[center[21][0], center[21][1]],  [[3, 0], [0, 3]], l22_obj],
                        'l23': [[center[22][0], center[22][1]],  [[3, 0], [0, 3]], l23_obj],
                        'l24': [[center[23][0], center[23][1]],  [[3, 0], [0, 3]], l24_obj],
                        'l25': [[center[24][0], center[24][1]],  [[3, 0], [0, 3]], l25_obj],
                        'l26': [[center[25][0], center[25][1]],  [[3, 0], [0, 3]], l26_obj],
                        'l27': [[center[26][0], center[26][1]],  [[3, 0], [0, 3]], l27_obj],
                        'l28': [[center[27][0], center[27][1]],  [[3, 0], [0, 3]], l28_obj],
                        'l29': [[center[28][0], center[28][1]],  [[3, 0], [0, 3]], l29_obj],
                        'l30': [[center[29][0], center[29][1]],  [[3, 0], [0, 3]], l30_obj],
                        'l31': [[center[30][0], center[30][1]],  [[3, 0], [0, 3]], l31_obj],
                        'l32': [[center[31][0], center[31][1]],  [[3, 0], [0, 3]], l32_obj],
                        'l33': [[center[32][0], center[32][1]],  [[3, 0], [0, 3]], l33_obj],
                        'l34': [[center[33][0], center[33][1]],  [[3, 0], [0, 3]], l34_obj],
                        'l35': [[center[34][0], center[34][1]],  [[3, 0], [0, 3]], l35_obj],
                        'l36': [[center[35][0], center[35][1]],  [[3, 0], [0, 3]], l36_obj],
                        'l37': [[center[36][0], center[36][1]],  [[3, 0], [0, 3]], l37_obj],
                        'l38': [[center[37][0], center[37][1]],  [[3, 0], [0, 3]], l38_obj],
                        'l39': [[center[38][0], center[38][1]],  [[3, 0], [0, 3]], l39_obj],
                        'l40': [[center[39][0], center[39][1]],  [[3, 0], [0, 3]], l40_obj],
                        'l41': [[center[40][0], center[40][1]],  [[3, 0], [0, 3]], l41_obj],
                        'l42': [[center[41][0], center[41][1]],  [[3, 0], [0, 3]], l42_obj],
                        'l43': [[center[42][0], center[42][1]],  [[3, 0], [0, 3]], l43_obj],
                        'l44': [[center[43][0], center[43][1]],  [[3, 0], [0, 3]], l44_obj]
                        }
        
        
        self.no_of_classes = 3
        self.classes = np.array([[0.7, 0.25, 0.05],
                                  [0.65, 0.3, 0.05],
                                  [0.6, 0.35, 0.05],
                                  [0.7, 0.25, 0.05],
                                  [0.35, 0.6, 0.05],
                                  [0.05, 0.35, 0.6]])

        self.num_sample_points = 200
    
    def pad_obstacle(self, padding):
        for (obs, boundary) in iter(self.obs.items()):
            obs_x,obs_y = boundary.exterior.coords.xy
            new_poly=[]
            centroid_x = 0
            centroid_y = 0            
            for i in range(len(obs_x)-1):
                centroid_x = centroid_x + obs_x[i]
                centroid_y = centroid_y + obs_y[i]
            centroid_x=centroid_x/(len(obs_x)-1)
            centroid_y=centroid_y/(len(obs_x)-1)
            for i in range(len(obs_x)-1):
                v=np.array([obs_x[i]-centroid_x,obs_y[i]-centroid_y])
                v1=v/np.linalg.norm(v)
                new_poly.append((obs_x[i]+v1[0]*padding,obs_y[i]+v1[1]*padding))
            self.padded_obs[obs]=Polygon(new_poly)
    

class Landmark(object):
    """
    define the workspace where robots reside
    """
    def __init__(self):
        # dimension of the workspace
        
        self.landmark= {}
        self.classes = {}
        self.no_of_classes = 3
        self.num_sample_points = 200
        self.packages = []
        self.package_locations = {}
        self.packages_picked = []
        self.packages_picked_robots = []
        self.package_pick_skills = []
        self.package_drop_skills = []

            
    def update_from_landmark(self,landmark_obj):
        self.landmark = landmark_obj.landmark.copy()
        start = datetime.datetime.now()   
        # self.landmark_x = landmark_obj.landmark_x.copy()
        # self.landmark_y = landmark_obj.landmark_y.copy()
        # self.generate_samples()
        NBA_time = (datetime.datetime.now() - start).total_seconds()
        print('Time for constructing the NBA: {0:.4f} s'.format(NBA_time))
        
        
    def update_from_workspace(self,workspace_obj):
        self.landmark = workspace_obj.landmark.copy()
        
        """ Case 1
        """
        p1 = Package('l1', self.landmark, [5], [6], size=2, color ="blue")
        p2 = Package('l2', self.landmark, [5], [6], size=2, color ="green")
        p3 = Package('l3', self.landmark, [5], [6], size=2, color ="red")
        p4 = Package('l4', self.landmark, [5], [6], size=2, color ="yellow")
        self.package_pick_skills = [5]
        self.package_drop_skills = [6]
        self.packages = [p1,p2,p3,p4]
        
        
        
        
        """ Scalability dISASTER factory """
        # p1 = Package('l1', self.landmark, [1], [12], size=4, color='blue')
        # p2 = Package('l2', self.landmark, [1], [12], size=4, color='blue')
        # p3 = Package('l3', self.landmark, [1], [12], size=4, color='blue')
        # p4 = Package('l4', self.landmark, [1], [12], size=4, color='blue')
        # p5 = Package('l5', self.landmark, [1], [12], size=4, color='blue')
        # p6 = Package('l6', self.landmark, [1], [12], size=4, color='blue')
        # p7 = Package('l7', self.landmark, [1], [12], size=4, color='blue')
        # p8 = Package('l8', self.landmark, [1], [12], size=4, color='blue')
        # p9 = Package('l9', self.landmark, [2], [12], size=4, color='red')
        # p10 = Package('l10', self.landmark, [2], [12], size=4, color='red')
        # p11 = Package('l11', self.landmark, [2], [12], size=4, color='red')
        # p12 = Package('l12', self.landmark, [2], [12], size=4, color='red')
        # p13 = Package('l13', self.landmark, [2], [12], size=4, color='red')
        # p14 = Package('l14', self.landmark, [2], [12], size=4, color='red')
        # p15 = Package('l15', self.landmark, [2], [12], size=4, color='red')
        # p16 = Package('l16', self.landmark, [2], [12], size=4, color='red')
        # p17 = Package('l17', self.landmark, [2], [12], size=4, color='red')
        # p18 = Package('l18', self.landmark, [2], [12], size=4, color='red')
        # p19 = Package('l19', self.landmark, [5], [12], size=4, color='orange')
        # p20 = Package('l20', self.landmark, [5], [12], size=4, color='orange')
        # p21 = Package('l21', self.landmark, [5], [12], size=4, color='orange')
        # p22 = Package('l22', self.landmark, [5], [12], size=4, color='orange')
        # p23 = Package('l23', self.landmark, [5], [12], size=4, color='orange')
        # p24 = Package('l24', self.landmark, [5], [12], size=4, color='orange')
        # p25 = Package('l25', self.landmark, [3], [12], size=4, color='purple')
        # p26 = Package('l26', self.landmark, [3], [12], size=4, color='purple')
        # p27 = Package('l27', self.landmark, [3], [12], size=4, color='purple')
        # p28 = Package('l28', self.landmark, [3], [12], size=4, color='purple')
        # p29 = Package('l29', self.landmark, [3], [12], size=4, color='purple')
        # p30 = Package('l30', self.landmark, [3], [12], size=4, color='purple')
        # p31 = Package('l31', self.landmark, [3], [12], size=4, color='purple')
        # p32 = Package('l32', self.landmark, [3], [12], size=4, color='purple')
        # p33 = Package('l33', self.landmark, [3], [12], size=4, color='purple')
        # p34 = Package('l34', self.landmark, [3], [12], size=4, color='purple')
        # p35 = Package('l35', self.landmark, [4], [12], size=4, color='green')
        # p36 = Package('l36', self.landmark, [4], [12], size=4, color='green')
        # p37 = Package('l37', self.landmark, [4], [12], size=4, color='green')
        # p38 = Package('l38', self.landmark, [4], [12], size=4, color='green')
        # p39 = Package('l39', self.landmark, [4], [12], size=4, color='green')
        # p40 = Package('l40', self.landmark, [4], [12], size=4, color='green')
        # p41 = Package('l41', self.landmark, [4], [12], size=4, color='green')
        # p42 = Package('l42', self.landmark, [4], [12], size=4, color='green')
        # p43 = Package('l43', self.landmark, [4], [12], size=4, color='green')
        # p44 = Package('l44', self.landmark, [4], [12], size=4, color='green')
        # self.package_pick_skills = [1,2,3,4,5]
        # self.package_drop_skills = [12]
        # self.packages = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13,
        #                   p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24,
        #                   p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35,
        #                   p36, p37, p38, p39, p40, p41, p42, p43, p44]
        
        
    def update_package_locations(self):
        self.packages_picked = []
        self.packages_picked_robots = []
        for lm_key in self.landmark:
            self.package_locations[lm_key]=[]
        for pkg in self.packages:
            if not pkg.picked:
                self.package_locations[pkg.landmark_id].append(pkg)
            else:
                self.packages_picked.append(pkg)
                self.packages_picked_robots.append(pkg.picked_by_robot)

            
class Package(object):
    """
    define the workspace where robots reside
    """
    def __init__(self, landmark_id,landmarks, pick_skill, drop_skill, disp=0, size = 5, color = "brown"):
        # dimension of the workspace
        self.landmark_id = landmark_id
        self.position = landmarks[self.landmark_id][0]
        self.pick_skill = pick_skill
        self.drop_skill = drop_skill
        self.picked = False
        self.color = color
        self.size = size
        self.picked_by_robot = None
        self.displacement = disp

