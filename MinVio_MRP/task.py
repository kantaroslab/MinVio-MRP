# -*- coding: utf-8 -*-

from workspace import Workspace, get_label
from random import uniform
import numpy as np
from sympy import Symbol
import copy
    
class Robot(object):
    def __init__(self,pos, team_num):
        self.pos = pos
        self.team_num = team_num
        self.skills = [] 
        """
        self.skills refers to current skillset of robot (includes failures)
        self.skills[0] is always for robot alive or dead, i.e., total failure
        """
    def skill_failure(self,skill_num):
        self.skills[skill_num] = 0
    
    def skill_activated(self,skill_num):
        self.skills[skill_num] = 1
    
    

class Teams(object):
    def __init__(self,team_skills):
        self.team_skills = team_skills #refers to skill set of teams(independent of failures)
        
        self.rob_list = []
        self.rob_pos = []
    
    def add_robots(self, rob_list):
        self.rob_list += rob_list
        for rob in rob_list:
            rob.skills = copy.copy(self.team_skills[rob.team_num])
        
    def get_all_rob_pos(self):
        self.rob_pos = []
        for rob in self.rob_list:
            self.rob_pos.append(rob.pos)
        return tuple(self.rob_pos)
    
    def update_all_rob_pos(self, new_pos_list):
        for i in range(len(new_pos_list)):
            self.rob_pos[i] = new_pos_list[i]
            self.rob_list[i].pos = new_pos_list[i]
        
    def get_able_robs(self, skill_num):
        able_robs=[]
        for i in range(len(self.rob_list)):
            if self.rob_list[i].skills[skill_num] == 1:
                able_robs.append(i+1)
        return able_robs
    
        
    
    
class Task(object):
    """
    define the task specified in LTL
    """
    def __init__(self, rob_pos, task_label_ref=None):
        """
        +----------------------------+
        |   Propositonal Symbols:    |
        |       true, false         |
        |	    any lowercase string |
        |                            |
        |   Boolean operators:       |
        |       !   (negation)       |
        |       ->  (implication)    |
        |       &&  (and)            |
        |       ||  (or)             |
        |                            |
        |   Temporal operators:      |
        |       []  (always)         |
        |       <>  (eventually)     |
        |       U   (until)          |
        +----------------------------+
        """
        workspace = Workspace()
        
        manual_initiation = True
        # robot_initial_pos = ((15,5),(55,5), (95,5))#,(35,5),(75,5),(15,145),(35,145), (55,145),(75,145),(95,145),(115,5),(135,5),(145,10),(145,30),(145,50))
        robot_initial_pos = copy.copy(rob_pos)
        robot_initial_angle = [np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708]), np.array([1.5708])]
        
        # For subformula it is necessary to have a space between landmark and logical operator 
        # task specification, e_i are subformulas, li_j means the j-th robot is at regions l_i
        '''
        subformula={ AP_id: [a,b,c,d,e]}
        a: condition for AP_id to be True
        b: if 0=> "AND". If "1"=> OR
        c: distance from landmark
        d: penalties
        e: if 0=> landmark . If "1"=> class
        '''
        
        """ Case 1
        """
        
        # self.formula = '<>e4 && !(e5) U e4  && <>(e6 && <>(e1 && e2 && e3))'
        # self.subformula = {1: ['(l1_1)',0,2,{"l1_1":[1,-30]}, 0], 
        #                     2: ['(l2_2)',0,2, {"l2_2":[2,-50]}, 0],
        #                     3: ['(l3_3)',0,2,{"l3_3":[3,-15]}, 0],
        #                     4: ['(l4_4)',0,2,{"l4_4":[4,-50]}, 0],
        #                     5: ['( l4_2 || l4_3)',0,7,{"l4_2":[2,-10],
        #                                                         "l4_3":[2,-10]}, 0],
        #                     6: ['(l1_1 && l4_2 && l4_3)',0,10,{"l1_1":[2,-0],"l4_2":[2,-0],
        #                                                         "l4_3":[2,-0]}, 0]
        #                     }
        # self.number_of_robots = len(rob_pos)
        
        
        
        """ Scalability Test """
        
        self.formula = '<> (e1 && <>(e2 && <>(e3))) && <> (e4 && <>(e5 && <>(e6)))' 
        self.subformula = {1: ['( l22_5 && l23_3 && l3_11 && l8_17 && l25_21 && l4_12 )',  0,  4,
                              {'l22_5': [5, -4],   'l23_3': [5, -6],   'l3_11': [1, -10],
                                'l8_17': [4, -13],   'l25_21': [3, -15],   'l4_12': [1, -17]},
                              0],
                              2: ['( l26_16 && l9_13 && l24_3 && l18_4 && l44_7 && l14_21 && l2_17 )',  0,  4,
                              {'l26_16': [2, -3],   'l9_13': [2, -5],   'l24_3': [2, -9],
                                'l18_4': [2, -12],   'l44_7': [4, -14],   'l14_21': [2, -16],   'l2_17': [1, -18]},
                              0],
                              3: ['( l13_16 && l8_8 && l30_1 && l1_18 && l27_12 && l20_5 && l41_19 && l27_24 )',  0,  4,
                              {'l13_16': [2, -8],   'l8_8': [5, -9],   'l30_1': [3, -10],   'l1_18': [1, -11],
                                'l27_12': [3, -11],   'l20_5': [4, -12],   'l41_19': [4, -13],   'l27_24': [3, -14]},
                              0],
                              4: ['( l19_7 && l21_13 && l34_14 && l40_15 && l39_18 && l5_19)',  0,  4,
                              {'l19_7': [5, -16],   'l21_13': [2, -18],   'l34_14': [2, -10],
                                'l40_15': [2, -11],   'l39_18': [4, -13],   'l5_19': [1, -10]},
                              0],
                              5: ['( l11_15 && l12_5 && l31_6 && l42_8 && l28_24 && l29_11 && l37_18 && l6_10 )',  0,  4,
                              {'l11_15': [2, -14],   'l12_5': [5, -13],   'l31_6': [5, -12],   'l42_8': [4, -11],
                                'l28_24': [3, -11],   'l29_11': [3, -13],   'l37_18': [4, -15],   'l6_10': [1, -17]},
                              0],
                              6: ['( l39_9 && l20_14 && l41_2 && l16_3 && l24_4 && l32_6 && l38_20 && l34_23 && l26_22)',  0,  4,
                              {'l39_9': [1, -4],   'l20_14': [2, -6],   'l41_2': [4, -8],   'l16_3': [2, -10],
                                'l24_4': [2, -11],   'l32_6': [4, -13],   'l38_20': [4, -15],   'l34_23': [3, -10],   'l26_22': [3, -10]},
                              0]}
        self.number_of_robots = len(rob_pos)
        
        
        
        if not manual_initiation:
            self.init = []  # initial locations
            self.init_label = []  # labels of initial locations
            for i in range(self.number_of_robots):
                while True:
                    ini = [round(uniform(0, workspace.workspace[k]), 3) for k in range(len(workspace.workspace))]
                    ap = get_label(ini, workspace)
                    if 'o' not in ap:
                        break
                self.init.append(tuple(ini))
                self.init_angle.append(np.arctan2(workspace.workspace[1]/2-ini[1],workspace.workspace[1]/2-ini[0]))
                # ap = ap + '_' + str(i + 1) if 'l' in ap else ''
                # self.init_label.append(ap)
            self.init = tuple(self.init)          # in the form of ((x, y), (x, y), ...)
            self.init_label = self.get_label_landmark(self.init, workspace, task_label_ref)
        else:
            self.init = robot_initial_pos
            self.init_angle = robot_initial_angle
            self.init_label = self.get_label_landmark(self.init, workspace, task_label_ref)
            
        self.threshold = 1                # minimum distance between any pair of robots
        
        
    
    def get_label_landmark(self, x, workspace, task_label_ref=None):
        '''
        inputParameters
        ----------
        x : state of all robots
        workspace: object or Workspace class or Landmark class
        
        get labels of robot position satisfied in each AP
        returns {2:['','l6_2']
                 3:[''}]}   --> 
        '''
        AP_labels = {}
        
        for key in self.subformula.keys():
            AP = self.subformula[key][0]
            logic = self.subformula[key][1]     #not needed
            # desired_prob = self.subformula[key][2]
            distance = self.subformula[key][2]
            if self.subformula[key][4] == 0:
                # dict storing robot as key and its respective landmark
                robot_index, AP = self.parse_AP(AP, task_label_ref)     
                label=[]
                AP_satisfied = False
                count = 0
                for robot_id in range(1, self.number_of_robots+1):
                    if robot_id in robot_index.keys():
                        #check probability and set flag (x[robot_id]), probability, distance workspace, robot_id, landmark)
                        landmark_id = robot_index[robot_id]
                        if self.robot_proximity_check(x[robot_id - 1], distance, workspace, robot_id, landmark_id):
                            label.append('l'+ str(landmark_id) + '_' + str(robot_id))
                            count+=1
                            if logic == 1:
                                AP_satisfied = True
                        else:
                            label.append('')
                    else:
                        label.append('')
                if logic == 0 and count != 0: #If AP is partially satisfied count wont be equal to length of AP
                    AP_satisfied = True
                if AP_satisfied:
                    AP_labels[key]=label
            else:
                robot_index = self.parse_AP(AP) 
                label=[]
                AP_satisfied = False
                count = 0
                for robot_id in range(1, self.number_of_robots+1):
                    if robot_id in robot_index.keys():
                        #check probability and set flag (x[robot_id]), probability, distance workspace, robot_id, landmark)
                        class_id = robot_index[robot_id] 
                        landmark_id = np.argmax(workspace.classes[:,(class_id-1)]) + 1
                        
                        lm_id = []
                        for index in range(workspace.classes.shape[0]):
                            if np.argmax(workspace.classes[index,:]) == class_id-1:
                                lm_id.append(index+1)
                        label_flag=False
                        for landmark_id in lm_id:
                            if self.robot_proximity_check(x[robot_id - 1], distance, workspace, robot_id, landmark_id):
                                label.append('c'+ str(class_id) + '_' + str(robot_id))
                                count+=1
                                label_flag=True
                                if logic == 1:
                                    AP_satisfied = True
                        if not label_flag:
                            label.append('')
                    else:
                        label.append('')
                if logic == 0 and count != 0: #If AP is partially satisfied count wont be equal to length of AP
                    AP_satisfied = True
                if AP_satisfied:
                    AP_labels[key]=label
                
        return AP_labels
                
            
                
    def robot_proximity_check(self, x, distance, workspace, robot_id, landmark_id):
        
        
        lm_id = "l"+str(landmark_id)
        xx1 = workspace.landmark[lm_id][0][0]-x[0]
        yy1 = workspace.landmark[lm_id][0][1]-x[1]
        dist = np.sqrt(xx1**2+yy1**2)
        if dist < distance:
            return True
        else:
            return False
        
            
    def parse_AP(self, AP, task_label_ref = None):
        """
        Parameters
        ----------
        AP : Atomic proposition text
        task_label_ref: If reassignment is done then this tells what are new tasks
        Returns
        -------
        robot_index : TYPE
            DESCRIPTION.

        """
        # returns list of landmarks and respective robot indices for a given AP (subformula)
        robot_index={}
        i=0
        if task_label_ref:
            AP = self.reassignAP(AP,task_label_ref)
        while i < len(AP):
            if AP[i]=='l' or AP[i]=='c':
                j=i+1
                while AP[j]!='_':
                    j=j+1
                k=j+1
                while AP[k]!=' ' and AP[k]!=')':
                    k=k+1
                robot_index[int(AP[j+1:k])] = int(AP[i+1:j])
                i=k
            else:
                i+=1
        return robot_index, AP
    
    def reassignAP(self, AP, task_label_ref):
        """
        Parses AP and replaces tasks in AP with new reassigned tasks
        Parameters
        ----------
        AP : Atomic proposition text
        task_label_ref: If reassignment is done then this tells what are new tasks
        Returns
        -------
        None.
        """
        for key in task_label_ref:
            if key in AP:
                AP = AP.replace(key, task_label_ref[key])
        return AP
    
    
    def Replanning_check(self, rob_waypoint, next_rob_waypoint, workspace, robot_wp_satsify_AP, robot_id, buchi_graph):
        rob_x = rob_waypoint[0]
        rob_y = rob_waypoint[1]
        rob_state = rob_waypoint[2]
        rob_target_state = rob_waypoint[3]
        
        needs_replanning = False
# case 1 ... check if end point of robot_id (referrred from robot_wp_satsify_AP) still satisfy AP for that robot_id
        # find the truth value to reach the next buchi state
        truth = buchi_graph.edges[(rob_state, rob_target_state)]['truth']
        if truth != '1': 
            #find the target for robot_id
            target_lm=""
            for key in truth.keys():
                pair = key.split('_')
                if int(pair[1])==robot_id and truth[key]:
                    target_lm=key
            if target_lm!="":
                pair = target_lm.split('_')
                is_class=False
                if pair[0][0]=='c':
                    lm_id = np.argmax(workspace.classes[:,(int(pair[0][1:])-1)]) + 1
                    target_lm_='l'+str(lm_id)+'_'+pair[1]
                    pair = target_lm_.split('_')
                    is_class = True
                # if target_lm covariance is large then dont replan
                if (workspace.landmark[pair[0]][1][0][0] <=0.3 and workspace.landmark[pair[0]][1][1][1] <= 0.3) or is_class:
                    b_state_count=0
                    for i in range(len(robot_wp_satsify_AP[robot_id-1])):
                        if robot_wp_satsify_AP[robot_id-1][i][2] == rob_state:
                            b_state_count=i+1                
                    satisfying_x = []
                    for i in range(self.number_of_robots):
                        satisfying_x.append(robot_wp_satsify_AP[i][b_state_count][:2])        
                    label = self.get_label_landmark(satisfying_x, workspace)
                    mod_truth={target_lm:True}
                    needs_replanning = not(self.check_transition_b(label, mod_truth))
        if needs_replanning:
            return needs_replanning

# case 2 ... check if next waypoints of robot_id enter avoid region     
        avoid = buchi_graph.edges[(rob_state, rob_target_state)]['avoid_self_loop']   
        avoid_truth = {}
        if truth !='1':
            for key in truth.keys():
                if truth[key]==False:
                    avoid_truth[key]=False
        for key in avoid.keys():
            for i in range(len(avoid[key])):
                lmid=avoid[key][i][0]+'_'+str(key+1)
                avoid_truth[lmid]=False
        for j in range(len(next_rob_waypoint[0])):           
            next_state=[]
            for i in range(self.number_of_robots):
                next_state.append(next_rob_waypoint[i][j][:2])
            needs_replanning = not(self.check_transition_b(self.get_label_landmark(next_state, workspace), avoid_truth))
            if needs_replanning:
                return needs_replanning
        return needs_replanning 
        
        
    def check_transition_b(self, x_label, truth):
        """
        check whether transition enabled with current generated label
        :param x_label: label of the current position
        :param truth: symbol enabling the transition
        :return: true or false
        """
        if truth == '1':
            return True
        # all true propositions should be satisdied
        true_label = [true_label for true_label in truth.keys() if truth[true_label]]
        for label in true_label:
            found = False
            for key in x_label.keys():
                if label in x_label[key]:
                    found =True
            if found==False:
                return False

        #  all fasle propositions should not be satisfied
        false_label = [false_label for false_label in truth.keys() if not truth[false_label]]
        for label in false_label:
            found = False
            for key in x_label.keys():
                if label in x_label[key]:
                    found =True
            if found==True:
                return False
        return True
    
    
    # def reassign(self, rob_team):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        