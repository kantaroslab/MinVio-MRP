# -*- coding: utf-8 -*-

from task import Task
from buchi_parse import Buchi
from workspace import Workspace
from geodesic_path import Geodesic
import datetime
from collections import OrderedDict
import numpy as np
from biased_tree import BiasedTree
from construct_biased_tree import construction_biased_tree#, path_via_visibility
from draw_picture import path_plot, path_plot_moving_lm, path_print,\
    path_plot_moving_lm_multibot, path_plot_moving_lm_multibot_with_pkgs
from text_editor import export_to_txt, export_cov_to_txt, export_disc_to_txt
import matplotlib.pyplot as plt
import pyvisgraph as vg
from termcolor import colored
import networkx as nx



if __name__ == "__main__":
    # task
    np.random.seed(0)
    identity='run1'
    number_of_trials = 1
    save_waypoints = False
    save_covariances = False
    drone_height = 16.0     # altitude of drones
    waypoint_folder_location = "/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource"
    launch_folder_location = "/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/launch"
    
    
    time_array=[]   #stores time for each trial run
    cost_array=[]   #stores cost of each trial run
    
    
    for round_num in range(number_of_trials):
        print('Trial {}'.format(round_num+1))
        start = datetime.datetime.now()
        task = Task()
        buchi = Buchi(task)
        buchi.construct_buchi_graph()
        buchi.get_minimal_length()
        buchi.get_feasible_accepting_state()
        buchi_graph = buchi.buchi_graph
        NBA_time = (datetime.datetime.now() - start).total_seconds()
        print('Time for constructing the NBA: {0:.4f} s'.format(NBA_time))
        
        # workspace
        workspace = Workspace()
        geodesic = Geodesic(workspace, task.threshold)
        # parameters
        n_max = 100000
        para = dict()
        # lite version, excluding extending and rewiring
        para['is_lite'] = True
        # step_size used in function near
        para['step_size'] = 0.25 * buchi.number_of_robots
        # probability of choosing node q_p_closest
        para['p_closest'] = 0.99
        # probability used when deciding the target point
        para['y_rand'] = 0.99
        # probability used when deciding the target point when inside sensing range
        # more random actions to increase visibility of     
        # para['y_rand'] = 0.99
        # minimum distance between any pair of robots
        para['threshold'] = task.threshold
        # Updates landmark covariance when inside sensor range
        para['update_covariance'] = True
        # sensor range in meters
        para['sensor_range'] = 15
        # sensor measurement noise
        para['sensor_R'] = 0.5
        
        
        
        for b_init in buchi_graph.graph['init']:
            # initialization
            opt_cost = np.inf
            opt_path_pre = []
            opt_path_suf = []
        
            # ----------------------------------------------------------------#
            #                            Prefix Part                          #
            # ----------------------------------------------------------------#
        
            start = datetime.datetime.now()
            init_state = (task.init, b_init)
            init_label = task.init_label
            init_angle = task.init_angle
            tree_pre = BiasedTree(workspace, geodesic, buchi, task, init_state, init_label, init_angle, 'prefix', para)
            
            # print('------------------------------ prefix path --------------------------------')
            # construct the tree for the prefix part
            cost_path_pre, nodes, lm_cov, targets = construction_biased_tree(tree_pre, n_max)
            if len(tree_pre.goals):
                pre_time = ((datetime.datetime.now() - start).total_seconds())/60
                print('Time for the prefix path: {0:.4f} min'.format(pre_time))
                print('{0} accepting goals found'.format(len(tree_pre.goals)))
                print(len(cost_path_pre[0][1]))
            else:
                print('Couldn\'t find the path within predetermined number of iteration')
                break
            
                    
            for i in range(len(tree_pre.goals)):
                if cost_path_pre[i][0] < opt_cost:
                    opt_path_suf=[]
                    opt_path_pre = cost_path_pre[i][1]
                    opt_cost = cost_path_pre[i][0]
               
            # path_print((opt_path_pre, opt_path_suf), workspace, buchi.number_of_robots)
#case 1 comment start                
            # path_plot((opt_path_pre, opt_path_suf), workspace, tree_pre.biased_tree.nodes[cost_path_pre[0][1][-1]]['lm'], buchi.number_of_robots, round_num, identity)
            # plt.show()
#case 1 comment end
            path_plot_moving_lm_multibot((opt_path_pre, opt_path_suf), workspace, tree_pre, cost_path_pre, buchi.number_of_robots, round_num, identity)
            
            print('Time for the prefix path: {0:.4f} min'.format(pre_time))
            print('Cost of path: {}'.format(cost_path_pre[0][0]))
            print(' ')
            print(' ')
            print(len(cost_path_pre[0][1]))
            time_array.append(pre_time)
            cost_array.append(cost_path_pre[0][0])
    print(time_array)
    print(cost_array)
    if number_of_trials == 1 and  save_waypoints:
        robot_waypoints, robot_wp_satsify_AP = export_disc_to_txt(cost_path_pre, targets, buchi.number_of_robots, drone_height, waypoint_folder_location, launch_folder_location, 1)
    if number_of_trials == 1 and  save_covariances:
        export_cov_to_txt(lm_cov, waypoint_folder_location, launch_folder_location)

        
def generate_NBA(task, rob_team):
    start = datetime.datetime.now()
    buchi = Buchi(task, rob_team)
    buchi.construct_buchi_graph()
    buchi.get_minimal_length()
    buchi.get_feasible_accepting_state()
    buchi_graph = buchi.buchi_graph
    NBA_time = (datetime.datetime.now() - start).total_seconds()
    print('Time for constructing the NBA: {0:.4f} s'.format(NBA_time))
    return buchi, buchi_graph

def reassign_NBA(buchi,init_state):
    """
    Parameters
    ----------
    task : task object
    rob_team : rob_team object

    Returns
    -------
    Returns False if no reassignment is needed
    Returns true and updated NBA if reassignment is done
    """
    reassignment_flag,len_remaining_edges = buchi.reassign(init_state)
    buchi.get_minimal_length()
    return reassignment_flag,len_remaining_edges
    

def generate_path(task, buchi, buchi_graph, workspace, init_state, node_landmark = None, save_waypoints = True, 
                  edit_launch_file=True, save_covariances = False, animation = False,
                  prev_fail_loc_counter=0, skill_visualizer = None, old_penalty=0):
    identity='run1'
    round_num = 1
    number_of_trials = 1
    drone_height = 16.0     # altitude of drones
    waypoint_folder_location = "/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/resource"
    launch_folder_location = "/home/samarth/catkin_ws/src/rotors_simulator/rotors_gazebo/launch"
    
    time_array=[]   #stores time for each trial run
    cost_array=[]   #stores cost of each trial run
    
    geodesic = Geodesic(workspace, task.threshold)
    # geodesic = Geodesic(workspace, task.threshold,animation)
    # parameters
    n_max = 100000
    para = dict()
    # lite version, excluding extending and rewiring
    para['is_lite'] = True
    # step_size used in function near
    para['step_size'] = 0.25 * buchi.number_of_robots
    # probability of choosing node q_p_closest
    para['p_closest'] = 0.999
    # probability used when deciding the target point
    para['y_rand'] = 0.9999
    # probability used when deciding the target point when inside sensing range
    # more random actions to increase visibility of     
    # para['y_rand'] = 0.99
    # minimum distance between any pair of robots
    para['threshold'] = task.threshold
    # Updates landmark covariance when inside sensor range
    para['update_covariance'] = True
    # sensor range in meters
    para['sensor_range'] = 10
    # sensor measurement noise
    para['sensor_R'] = 0.5
    
    
    
    # initialization
    opt_cost = np.inf
    opt_path_pre = []
    opt_path_suf = []

    # ----------------------------------------------------------------#
    #                            Prefix Part                          #
    # ----------------------------------------------------------------#

    start = datetime.datetime.now()
    init_label = task.init_label
    init_angle = task.init_angle
    tree_pre = BiasedTree(workspace, geodesic, buchi, task, init_state, init_label, init_angle, 'prefix', para, node_landmark)
    
    # print('------------------------------ prefix path --------------------------------')
    # construct the tree for the prefix part
    cost_path_pre, nodes, lm_cov, targets = construction_biased_tree(tree_pre, n_max)
    if len(tree_pre.goals):
        pre_time = ((datetime.datetime.now() - start).total_seconds())/60
        print('Time for the prefix path: {0:.4f} min'.format(pre_time))
        print('{0} accepting goals found'.format(len(tree_pre.goals)))
        for i in range(len(tree_pre.goals)):
            if cost_path_pre[i][0] < opt_cost:
                opt_path_suf=[]
                opt_path_pre = cost_path_pre[i][1]
                opt_cost = cost_path_pre[i][0]
                    
        
        print('Time for the prefix path: {0:.4f} seconds'.format(pre_time*60))
        print('Cost of path: {}'.format(cost_path_pre[0][0]))
        print(' ')
        print(' ')
        print(len(cost_path_pre[0][1]))
        time_array.append(pre_time)
        cost_array.append(cost_path_pre[0][0])
        print(time_array)
        print(cost_array)
        if number_of_trials == 1 and  save_waypoints:
            robot_waypoints, robot_wp_satsify_AP = export_disc_to_txt(cost_path_pre, targets, buchi.number_of_robots, drone_height, waypoint_folder_location, launch_folder_location, 10, edit_launch_file)
        if number_of_trials == 1 and  save_covariances:
            export_cov_to_txt(lm_cov, waypoint_folder_location, launch_folder_location)
            
        
        """Calculate penalty"""
        total_penalty = old_penalty
        for i in range(len(robot_wp_satsify_AP[0])):
            if (robot_wp_satsify_AP[0][i][2],robot_wp_satsify_AP[0][i][3]) in buchi_graph.edges:
                edge_dict = buchi_graph.edges[robot_wp_satsify_AP[0][i][2],robot_wp_satsify_AP[0][i][3]]
                for key in edge_dict['task_assign']:
                    total_penalty += edge_dict['task_assign'][key][1]
        print("\n\n Penalty = ", total_penalty)
        
        ### path_print((opt_path_pre, opt_path_suf), workspace, buchi.number_of_robots)
        if animation:
            path_plot_moving_lm_multibot_with_pkgs((opt_path_pre, opt_path_suf), workspace, 
                                         tree_pre, cost_path_pre, buchi.number_of_robots, 
                                         round_num, identity, prev_fail_loc_counter,skill_visualizer,total_penalty)
        # else:
        #     path_plot((opt_path_pre, opt_path_suf), workspace, tree_pre.biased_tree.nodes[cost_path_pre[0][1][-1]]['lm'], buchi.number_of_robots, round_num, identity)
        #     plt.show()
    else:
        print('Couldn\'t find the path within predetermined number of iteration')
        
    return robot_waypoints, robot_wp_satsify_AP, tree_pre, cost_path_pre
            


