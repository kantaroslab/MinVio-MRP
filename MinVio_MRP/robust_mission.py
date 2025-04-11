#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 14:54:55 2022

@author: samarth
"""


from biased_TLRRT_star import generate_NBA, reassign_NBA, generate_path
from task import Robot, Teams
import datetime
from workspace import Workspace
from task import Task
import numpy as np
from collections import OrderedDict
from draw_picture import path_plot_moving_lm_multibot_with_pkgs_LOCAL

np.random.seed(10012111)


def get_curr_rob_waypoints(all_robot_waypoints, wp_id):
    """
    for given waypoint funtion return list of waypoints of all robots
    Parameters
    ----------
    all_robot_waypoints : 
    wp_id : int.
    Returns
    -------
    curr_pos : list of current positions of all robots
    state : curent buchi state
    """
    curr_pos = []
    for rob in range(len(all_robot_waypoints)):
        curr_pos.append(tuple(all_robot_waypoints[rob][wp_id][:2]))
    return curr_pos, all_robot_waypoints[0][wp_id][2]

def find_sub_idx(test_list, repl_list, start = 0):
    length = len(repl_list)
    for idx in range(start, len(test_list)):
        if test_list[idx : idx + length] == repl_list:
            return idx, idx + length
 
# helper function to perform final task
def replace_sub(test_list, repl_list, new_list):
    length = len(new_list)
    idx = 0
    for start, end in iter(lambda: find_sub_idx(test_list, repl_list, idx), None):
        test_list[start : end] = new_list
        idx = start + length
        
        
if __name__=="__main__":
    
    """ Case 1
        """
    # r1=Robot((18,20),1)
    # r2=Robot((18,45),2)
    # r3=Robot((100,78),3)
    # r4=Robot((18,70),4)
    # team_skills = {1: [1, 1, 0, 1, 0, 0, 0, 0],
    #                 2: [1, 0, 1, 0, 0, 0, 0, 0],
    #                 3: [1, 0, 1, 1, 0, 0, 0, 0],
    #                 4: [1, 0, 0, 0, 1, 0, 0, 0]}
    # skill_visualizer_pkg = [[[1,3],['b','r'],[]],
    #                         [[2],['g'],[]],
    #                         [[2,3],['g','r'],[]],
    #                         [[2,4],['g','y'],[]],
    #                         ] 
    # rob_team = Teams(team_skills)
    # rob_team.add_robots([r1,r2,r3,r4])
        
    
    
    """ Scalability Test"""
    r1=Robot((178.4, 116.6), 1)
    r2=Robot((178.7, 109.1), 1)
    r3=Robot((178.7, 104.0), 2)
    r4=Robot((178.8, 98.6), 2)
    r5=Robot((18.3, 91.7), 3)
    r6=Robot((18.3, 83.9), 3)
    r7=Robot((18.1, 76.0), 3)
    r8=Robot((18.3, 68.9), 3)
    r9=Robot((178.9, 92.3), 4)
    r10=Robot((186.4, 116.6), 4)
    r11=Robot((186.8, 110.0), 4)
    r12=Robot((186.6, 104.3), 4)
    r13=Robot((18.3, 63.0), 5)
    r14=Robot((11.9, 91.8), 5)
    r15=Robot((11.6, 84.4), 5)
    r16=Robot((12.0, 76.1), 5)
    r17=Robot((186.8, 98.5), 6)
    r18=Robot((187.4, 91.7), 6)
    r19=Robot((192.6, 110.0), 6)
    r20=Robot((192.8, 99.2), 6)
    r21=Robot((11.6, 69.5), 7)
    r22=Robot((11.5, 63.5), 7)
    r23=Robot((5.8, 87.8), 7)
    r24=Robot((6.5, 66.6), 7)
    team_skills = {1:  [1, 0, 0, 1, 1, 0],
                    2: [1, 0, 1, 0, 0, 1],
                    3: [1, 0, 0, 0, 1, 1],
                    4: [1, 1, 0, 1, 0, 0],
                    5: [1, 0, 1, 0, 0, 0],
                    6: [1, 1, 0, 0, 1, 0],
                    7: [1, 0, 1, 1, 0, 0]}
    
    skill_visualizer_pkg = [[[3, 4], ['purple', 'green'], []],
                              [[3, 4], ['purple', 'green'], []],
                              [[2, 5], ['red', 'orange'], []],
                              [[2, 5], ['red', 'orange'], []],
                              [[4, 5], ['green', 'orange'], []],
                              [[4, 5], ['green', 'orange'], []],
                              [[4, 5], ['green', 'orange'], []],
                              [[4, 5], ['green', 'orange'], []],
                              [[1, 3], ['blue', 'purple'], []],
                              [[1, 3], ['blue', 'purple'], []],
                              [[1, 3], ['blue', 'purple'], []],
                              [[1, 3], ['blue', 'purple'], []],
                              [[2], ['red'], []],
                              [[2], ['red'], []],
                              [[2], ['red'], []],
                              [[2], ['red'], []],
                              [[1, 4], ['blue', 'green'], []],
                              [[1, 4], ['blue', 'green'], []],
                              [[1, 4], ['blue', 'green'], []],
                              [[1, 4], ['blue', 'green'], []],
                              [[2, 3], ['red', 'purple'], []],
                              [[2, 3], ['red', 'purple'], []],
                              [[2, 3], ['red', 'purple'], []],
                              [[2, 3], ['red', 'purple'], []]] # for scalabitily example
    rob_team = Teams(team_skills)
    rob_team.add_robots([r1 ,r2 ,r3 ,r4 ,r5 ,r6 ,r7 ,r8 ,r9 ,r10 ,r11 ,r12 ,r13 ,r14 ,r15 ,r16 ,r17 ,r18 ,r19 ,r20 ,r21 ,r22 ,r23 ,r24])
    
    
    
    
    
    workspace = Workspace()
    task=Task(rob_team.get_all_rob_pos())
    all_robot_waypoints = []
    robot_wp_satsify_AP = []
    buchi, buchi_graph = generate_NBA(task, rob_team)
    
    init_state = (task.init, buchi_graph.graph['init'][0])
    all_robot_waypoints,robot_wp_satsify_AP, tree_pre, cost_path_pre = generate_path(task, buchi, buchi_graph, 
                                    workspace, init_state, save_waypoints = True, 
                                    edit_launch_file=False, save_covariances = False,
                                    animation = True, skill_visualizer = skill_visualizer_pkg)
    
    """
    Now re-run with failure
    """
    
    """ Case 1
        """
    # r2.skill_failure(2)
    # skill_visualizer_pkg = [[[1,3],['b','r'],[]],
    #                         [[2],['g'],[2]],
    #                         [[2,3],['g','r'],[]],
    #                         [[2,3],['g','y'],[]],
    #                         ]
    # Failure_waypoint = 2





    """ Scalability Test """ 
 
    
    """ 1 fail """
    r20.skill_failure(1)
    r20.skill_failure(4)
    
    
    """ 3 fail """
    
    r22.skill_failure(2)
    r22.skill_failure(3)
    
    r1.skill_failure(3)
    r1.skill_failure(4)
    
    """ 6 fail """
    
    r23.skill_failure(2)
    r23.skill_failure(3)
    
    r2.skill_failure(3)
    r2.skill_failure(4)
    
    r9.skill_failure(1)
    r9.skill_failure(3)
    
    
    """ 12 fail """
    
    r4.skill_failure(2)
    r4.skill_failure(5)
    
    r6.skill_failure(4)
    r6.skill_failure(5)
    
    r8.skill_failure(4)
    r8.skill_failure(5)
    
    r10.skill_failure(1)
    r10.skill_failure(3)
    
    """ 16 fail """
    
    r16.skill_failure(2)
    
    r24.skill_failure(2)
    r24.skill_failure(3)
    
    
    r13.skill_failure(2)
    
    r12.skill_failure(1)
    r12.skill_failure(3)
    
    """ 20 fail """
    
    r21.skill_failure(2)
    r21.skill_failure(3)
    
    r15.skill_failure(2)
    
    r18.skill_failure(1)
    r18.skill_failure(4)
    
    r14.skill_failure(2)
    
    
    r3.skill_failure(2)
    r3.skill_failure(5)
    
    r5.skill_failure(4)
    r5.skill_failure(5)
    
    
    """ 22 fail """
    r17.skill_failure(1)
    r17.skill_failure(4)
    r19.skill_failure(1)
    r19.skill_failure(4)
    
    
    
    skill_visualizer_pkg = [[[3, 4], ['purple', 'green'], [3,4]],    #1
                              [[3, 4], ['purple', 'green'], [3,4]],    #2
                              [[2, 5], ['red', 'orange'], [2,5]],    #3
                              [[2, 5], ['red', 'orange'], [2,5]],    #4
                              [[4, 5], ['green', 'orange'], [4,5]],    #5
                              [[4, 5], ['green', 'orange'], [4,5]],    #6
                              [[4, 5], ['green', 'orange'], []],    #7
                              [[4, 5], ['green', 'orange'], [4,5]],    #8
                              [[1, 3], ['blue', 'purple'], [1,3]],    #9
                              [[1, 3], ['blue', 'purple'], [1,3]],    #10
                              [[1, 3], ['blue', 'purple'], []],    #11
                              [[1, 3], ['blue', 'purple'], [1,3]],    #12
                              [[2], ['red'], [2]],                    #13
                              [[2], ['red'], [2]],                    #14
                              [[2], ['red'], [2]],                    #15
                              [[2], ['red'], [2]],                    #16
                              [[1, 4], ['blue', 'green'], []],    #17
                              [[1, 4], ['blue', 'green'], [1,4]],    #18
                              [[1, 4], ['blue', 'green'], [1,4]],    #19
                              [[1, 4], ['blue', 'green'], [1,4]],    #20
                              [[2, 3], ['red', 'purple'], [2,3]],    #21
                              [[2, 3], ['red', 'purple'], [2,3]],    #22
                              [[2, 3], ['red', 'purple'], []],    #23
                              [[2, 3], ['red', 'purple'], [2,3]]] # for scalabitily example
   
    
    # Failure_waypoint = 2 
    Failure_waypoint = 23 
    # Failure_waypoint = 34 
    
    
    curr_pos, state = get_curr_rob_waypoints(all_robot_waypoints, Failure_waypoint*10)
    rob_team.update_all_rob_pos(curr_pos)
    start_reas_time = datetime.datetime.now()
    recalculate_path_flag,len_remaining_edges = reassign_NBA(buchi,state)
    reas_time = (datetime.datetime.now() - start_reas_time).total_seconds()
    print('Time for reassigning the NBA: {0:.4f} s'.format(reas_time))
    # print('Time for reassigning the NBA: {0:.4f} s'.format(reas_time))
    print("after b: ",recalculate_path_flag)
    
    task=Task(rob_team.get_all_rob_pos())
    init_state = (task.init, state)
    lm = tree_pre.biased_tree.nodes[cost_path_pre[0][1][Failure_waypoint]]['lm']
    all_robot_waypoints,robot_wp_satsify_AP, tree_pre, cost_path_pre = generate_path(task, buchi, buchi_graph, 
                                    workspace, init_state, node_landmark = lm, save_waypoints = True, 
                                    edit_launch_file=False, save_covariances = False,
                                    animation = True, prev_fail_loc_counter = Failure_waypoint, 
                                    skill_visualizer = skill_visualizer_pkg)
    print('Time for reassigning the NBA: {0:.4f} s'.format(reas_time))
    print("after b: ",recalculate_path_flag)
    print("Length of remaining edges:",len_remaining_edges)
    
    
