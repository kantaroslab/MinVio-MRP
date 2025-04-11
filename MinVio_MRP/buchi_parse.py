    # -*- coding: utf-8 -*-

import subprocess
import os.path
import re
import networkx as nx
import numpy as np
from networkx.classes.digraph import DiGraph
from sympy import satisfiable
from sympy.parsing.sympy_parser import parse_expr    #samarth change

from itertools import combinations




class Buchi(object):
    """
    construct buchi automaton graph
    """

    def __init__(self, task, rob_team):
        """
        initialization
        :param task: task specified in LTL
        """
        # task specified in LTL
        self.formula = task.formula
        self.subformula = task.subformula
        self.number_of_robots = task.number_of_robots
        # graph of buchi automaton
        self.buchi_graph = DiGraph(type='buchi', init=[], accept=[])
        #robots in the mission
        self.rob_team = rob_team

        # minimal length (in terms of number of transitions) between a pair of nodes
        self.min_length = dict()
        self.min_length_target = dict()

    """ original"""                
    # def construct_buchi_graph(self):
    #     """
    #     parse the output of the program ltl2ba and build the buchi automaton
    #     """
    #     # directory of the program ltl2ba
    #     dirname = os.path.dirname(__file__)
    #     # output of the program ltl2ba
    #     output = subprocess.check_output(dirname + "/./ltl2ba -f \"" + self.formula + "\"", shell=True).decode(
    #         "utf-8")
        
    #     # find all states/nodes in the buchi automaton
    #     state_re = re.compile(r'\n(\w+):\n\t')
    #     state_group = re.findall(state_re, output)

    #     # find initial and accepting states
    #     init = [s for s in state_group if 'init' in s]
    #     ''' accept to accept_al and vice versa loc 1/3'''
    #     # accept = [s for s in state_group if 'accept' in s]  
    #     accept = [s for s in state_group if 'accept_all' in s]  
    #     # finish the inilization of the graph of the buchi automaton
    #     self.buchi_graph.graph['init'] = init
    #     self.buchi_graph.graph['accept'] = accept
        
    #     order_key = list(self.subformula.keys())
    #     order_key.sort(reverse=True)
    #     # for each state/node, find it transition relations
    #     for state in state_group:
    #         # add node
    #         self.buchi_graph.add_node(state)
    #         # loop over all transitions starting from current state
    #         state_if_fi = re.findall(state + r':\n\tif(.*?)fi', output, re.DOTALL)
    #         if state_if_fi:
    #             relation_group = re.findall(r':: (\(.*?\)) -> goto (\w+)\n\t', state_if_fi[0])
    #             for symbol, next_state in relation_group: # symbol that enables state to next_state
    #                 # delete edges with multiple subformulas
    #                 # if ' && ' in symbol: continue
    #                 # whether the edge is feasible in terms of atomic propositions
    #                 symbol_copy = symbol
    #                 for k in order_key:
    #                     symbol = symbol.replace('e{0}'.format(k), self.subformula[k][0])
    #                 # get the truth assignment
    #                 truth_table = self.get_truth_assignment(symbol)
                    
    #                 # infeasible transition
    #                 if not truth_table: continue
                    
    #                 symbol_keys = re.findall(r'[0-9]+', symbol_copy)
    #                 avoid_regions={}
    #                 for i in range(self.number_of_robots):
    #                     avoid_regions[i]=[]
    #                 for key in truth_table:
    #                     if key!='1':
    #                         if truth_table[key]==False:
    #                             pair = key.split('_')  # region-robot pair
    #                             robot_index = int(pair[1]) - 1
    #                             distance=0
    #                             for sub_f in symbol_keys:
    #                                 if key in self.subformula[int(sub_f)][0]:
    #                                     distance = self.subformula[int(sub_f)][2]
    #                                     # prob = self.subformula[int(sub_f)][2]
                                
    #                             avoid_regions[robot_index].append((pair[0],distance))
                    
    #                 edge_skill={}
    #                 current_assignment={} #task: [rob_num, curr_score, fail_score]
    #                 task_ref = {}
    #                 if truth_table!="1":
    #                     for sub_f in symbol_keys:
    #                         for key in self.subformula[int(sub_f)][3]:
    #                             edge_skill[key] = self.subformula[int(sub_f)][3][key][0]
    #                             pair = key.split('_')  # region-robot pair
    #                             rob_num = int(pair[1])
    #                             current_assignment[key]=[rob_num,0,self.subformula[int(sub_f)][3][key][1]]
    #                             task_ref[key]=key
                        
                        
                    
                    
    #                 # add edge
    #                 avoid_current_state={}
    #                 for i in range(self.number_of_robots):
    #                     avoid_current_state[i]=[]
    #                 if state!=next_state and self.buchi_graph.has_edge(state,state):
    #                     avoid_current_state = self.buchi_graph.edges[(state,state)]['avoid']
    #                 # print(avoid_current_state)
    #                 self.buchi_graph.add_edge(state, next_state, AP = symbol_copy, 
    #                                           AP_keys=symbol_keys, truth=truth_table,
    #                                           avoid=avoid_regions, avoid_self_loop=avoid_current_state,
    #                                           transition_skill = edge_skill, task_assign = current_assignment,
    #                                           task_label_ref=task_ref, weight = 0.01)
    #         else:
    #             state_skip = re.findall(state + r':\n\tskip\n', output, re.DOTALL)
    #             if state_skip:
    #                 avoid_regions={}
    #                 avoid_current_state={}
    #                 for i in range(self.number_of_robots):
    #                     avoid_regions[i]=[]
    #                     avoid_current_state[i]=[]
    #                 # print(avoid_current_state)
    #                 self.buchi_graph.add_edge(state, state, AP='1', AP_keys=[], truth='1',
    #                                           avoid=avoid_regions, avoid_self_loop=avoid_current_state,
    #                                           transition_skill = {}, task_assign = {}, task_label_ref={},
    #                                           weight = 0.01)

    # def get_truth_assignment(self, symbol):
    #     """
    #     get one set of truth assignment that makes the symbol true
    #     :param symbol: logical expression which controls the transition
    #     :return: a set of truth assignment enables the symbol
    #     """
    #     # empty symbol
    #     if symbol == '(1)':
    #         return '1'
    #     # non-empty symbol
    #     else:
    #         exp = symbol.replace('||', '|').replace('&&', '&').replace('!', '~')
    #         # add extra constraints: a single robot can reside in at most one region
    #         robot_region = self.robot2region(exp)
    #         for robot, region in robot_region.items():
    #             mutual_execlusion = list(combinations(region, 2))
    #             # single label in the symbol
    #             if not mutual_execlusion: continue
    #             for i in range(len(mutual_execlusion)):
    #                 mutual_execlusion[i] = '(~(' + ' & '.join(list(mutual_execlusion[i])) + '))'
    #             exp = '(' + exp + ') & ' + ' & '.join(mutual_execlusion)
            
    #         exp=parse_expr(exp)     #samarth change
    #         # find one truth assignment that makes symbol true using function satisfiable
    #         # truth = satisfiable(exp, algorithm="dpll")
    #         truth = satisfiable(exp)
    #         try:
    #             truth_table = dict()
    #             for key, value in truth.items():
    #                 truth_table[key.name] = value
    #         except AttributeError:
    #             return False
    #         else:
    #             return truth_table
    
    """ MODIFIED!!!! for all truth tables in case of OR"""           
    def construct_buchi_graph(self):
        """
        parse the output of the program ltl2ba and build the buchi automaton
        """
        # directory of the program ltl2ba
        dirname = os.path.dirname(__file__)
        # output of the program ltl2ba
        output = subprocess.check_output(dirname + "/./ltl2ba -f \"" + self.formula + "\"", shell=True).decode(
            "utf-8")
        
        # find all states/nodes in the buchi automaton
        state_re = re.compile(r'\n(\w+):\n\t')
        state_group = re.findall(state_re, output)

        # find initial and accepting states
        init = [s for s in state_group if 'init' in s]
        ''' accept to accept_al and vice versa loc 1/4'''
        # accept = [s for s in state_group if 'accept' in s]  
        accept = [s for s in state_group if 'accept_all' in s]  
        # finish the inilization of the graph of the buchi automaton
        self.buchi_graph.graph['init'] = init
        self.buchi_graph.graph['accept'] = accept
        
        order_key = list(self.subformula.keys())
        order_key.sort(reverse=True)
        # for each state/node, find it transition relations
        for state in state_group:
            # add node
            self.buchi_graph.add_node(state)
            # loop over all transitions starting from current state
            state_if_fi = re.findall(state + r':\n\tif(.*?)fi', output, re.DOTALL)
            if state_if_fi:
                relation_group = re.findall(r':: (\(.*?\)) -> goto (\w+)\n\t', state_if_fi[0])
                for symbol, next_state in relation_group: # symbol that enables state to next_state
                    # delete edges with multiple subformulas
                    # if ' && ' in symbol: continue
                    # whether the edge is feasible in terms of atomic propositions
                    symbol_copy = symbol
                    for k in order_key:
                        symbol = symbol.replace('e{0}'.format(k), self.subformula[k][0])
                    # get the truth assignment
                    truth_table_all, num_of_truths  = self.get_truth_assignment_2(symbol)
                    
                    # infeasible transition
                    if not truth_table_all: continue
                    
                    symbol_keys = re.findall(r'[0-9]+', symbol_copy)                    
                    avoid_regions_all=[]
                    edge_skill_all=[]
                    current_assignment_all=[]
                    weight_all = []
                    task_ref_all = []
                    for truth_num in range(len(truth_table_all)):  
                        avoid_regions={}
                        truth_table=truth_table_all[truth_num]
                        for i in range(self.number_of_robots):
                            avoid_regions[i]=[]
                        for key in truth_table:
                            if key!='1':
                                if truth_table[key]==False:
                                    pair = key.split('_')  # region-robot pair
                                    robot_index = int(pair[1]) - 1
                                    distance=0
                                    for sub_f in symbol_keys:
                                        if key in self.subformula[int(sub_f)][0]:
                                            distance = self.subformula[int(sub_f)][2]
                                            # prob = self.subformula[int(sub_f)][2]
                                    
                                    avoid_regions[robot_index].append((pair[0],distance))
                        avoid_regions_all.append(avoid_regions)
                    
                        edge_skill={}
                        current_assignment={} #task: [rob_num, curr_score, fail_score]
                        task_ref = {}
                        if truth_table!="1":
                            for sub_f in symbol_keys:
                                for key in self.subformula[int(sub_f)][3]:
                                    edge_skill[key] = self.subformula[int(sub_f)][3][key][0]
                                    pair = key.split('_')  # region-robot pair
                                    rob_num = int(pair[1])
                                    current_assignment[key]=[rob_num,0,self.subformula[int(sub_f)][3][key][1]]
                                    task_ref[key]=key
                        edge_skill_all.append(edge_skill)
                        current_assignment_all.append(current_assignment)
                        weight_all.append(0.01)
                        task_ref_all.append(task_ref)
                    
                    
                    # add edge
                    avoid_current_state={}
                    for i in range(self.number_of_robots):
                        avoid_current_state[i]=[]
                    if state!=next_state and self.buchi_graph.has_edge(state,state):
                        avoid_current_state = self.buchi_graph.edges[(state,state)]['avoid']
                    # print(avoid_current_state)
                    self.buchi_graph.add_edge(state, next_state, AP = symbol_copy, 
                                              AP_keys=symbol_keys, 
                                              truth=truth_table_all[0], avoid=avoid_regions_all[0], 
                                              all_truth=truth_table_all, all_avoid=avoid_regions_all,
                                              avoid_self_loop=avoid_current_state,
                                              transition_skill = edge_skill_all[0], 
                                              all_transition_skill = edge_skill_all,
                                              task_assign = current_assignment_all[0],
                                              all_task_assign = current_assignment_all,
                                              task_label_ref=task_ref_all[0],
                                              all_task_label_ref=task_ref_all,
                                              counter = 0,
                                              weight = weight_all[0],
                                              all_weight=weight_all)
            else:
                state_skip = re.findall(state + r':\n\tskip\n', output, re.DOTALL)
                if state_skip:
                    avoid_regions={}
                    avoid_current_state={}
                    for i in range(self.number_of_robots):
                        avoid_regions[i]=[]
                        avoid_current_state[i]=[]
                    # print(avoid_current_state)
                    self.buchi_graph.add_edge(state, state, AP='1', 
                                              AP_keys=[], 
                                              truth='1', avoid=avoid_regions, 
                                              all_truth=['1'], all_avoid=[avoid_regions], 
                                              avoid_self_loop=avoid_current_state,
                                              transition_skill = {}, 
                                              all_transition_skill = [{}],
                                              task_assign = {},
                                              all_task_assign = [{}],
                                              task_label_ref={},
                                              all_task_label_ref = [{}],
                                              counter = 0,
                                              weight = 0.01,
                                              all_weight=[0.01])

    def get_truth_assignment_2(self, symbol):
        """
        get one set of truth assignment that makes the symbol true
        :param symbol: logical expression which controls the transition
        :rrn: a set of truth assignment enables the symbol
        """
        # empty symbol
        if symbol == '(1)':
            return '1',1
        # non-empty symbol
        else:
            exp = symbol.replace('||', '|').replace('&&', '&').replace('!', '~')
            # add extra constraints: a single robot can reside in at most one region
            if '|' not in exp:
                robot_region = self.robot2region(exp)
                for robot, region in robot_region.items():
                    mutual_execlusion = list(combinations(region, 2))
                    # single label in the symbol
                    if not mutual_execlusion: continue
                    for i in range(len(mutual_execlusion)):
                        if mutual_execlusion[i][0]!=mutual_execlusion[i][1]:
                            mutual_execlusion[i] = '(~(' + ' & '.join(list(mutual_execlusion[i])) + '))'
                        else:
                            mutual_execlusion[i] = '(' + ' & '.join(list(mutual_execlusion[i])) + ')'
                            
                    exp = '(' + exp + ') & ' + ' & '.join(mutual_execlusion)
                
                exp=parse_expr(exp)     
                
                # find one truth assignment that makes symbol true using function satisfiable
                truth = satisfiable(exp)
                try:
                    truth_table = dict()
                    for key, value in truth.items():
                        truth_table[key.name] = value
                except AttributeError:
                    return False,0
                else:
                    return [truth_table],1
            # In case of or condition in logic multiple truth values may be possible
            else: 
                robot_region = self.robot2region(exp)
                for robot, region in robot_region.items():
                    mutual_execlusion = list(combinations(region, 2))
                    # single label in the symbol
                    if not mutual_execlusion: continue
                    for i in range(len(mutual_execlusion)):
                        mutual_execlusion[i] = '(~(' + ' & '.join(list(mutual_execlusion[i])) + '))'
                    exp = '(' + exp + ') & ' + ' & '.join(mutual_execlusion)
                
                exp=parse_expr(exp)     #samarth change
                # find one truth assignment that makes symbol true using function satisfiable
                # truth = satisfiable(exp, algorithm="dpll")
                # truth_simple = satisfiable(exp)
                truth = satisfiable(exp,all_models=True)
                try:
                    all_truths=[]
                    for i in truth:
                        truth_table = dict()
                        for key, value in i.items():
                            truth_table[key.name] = value
                        all_truths.append(truth_table)
                except AttributeError:
                    return False,0
                else:
                    return all_truths, len(all_truths)

    def get_minimal_length(self):
        """
        search the shortest path from a node to another, i.e., # of transitions in the path
        :return: 
        """
        # loop over pairs of buchi states
        for head_node in self.buchi_graph.nodes():
            for tail_node in self.buchi_graph.nodes():
                # head_node = tail_node, and tail_node is an accepting state
                ''' accept to accept_al and vice versa loc 2/4'''
                # if head_node != tail_node and 'accept' in tail_node:
                if head_node != tail_node and 'accept_all' in tail_node:
                    try:
                        length, path = nx.algorithms.single_source_dijkstra(self.buchi_graph,
                                                                         source=head_node, target=tail_node)
                    # couldn't find a path from head_node to tail_node
                    except nx.exception.NetworkXNoPath:
                        length = np.inf
                    self.min_length[(head_node, tail_node)] = length
                    # print(path)
                    if len(path) ==1:
                        abab=7
                    self.min_length_target[(head_node, tail_node)] = path[1]
                # head_node != tail_node and tail_node is an accepting state
                # move 1 step forward to all reachable states of head_node then calculate the minimal length
                    ''' accept to accept_al and vice versa loc 3/4'''
                # elif head_node == tail_node and 'accept' in tail_node:
                elif head_node == tail_node and 'accept_all' in tail_node:
                    length = np.inf
                    for suc in self.buchi_graph.succ[head_node]:
                        try:
                            len1, path = nx.algorithms.single_source_dijkstra(self.buchi_graph,
                                                                           source=suc, target=tail_node)
                        except nx.exception.NetworkXNoPath:
                            len1 = np.inf
                        if len1 < length:
                            length = len1 + 1
                    self.min_length[(head_node, tail_node)] = length
                    self.min_length_target[(head_node, tail_node)] = path[0]

    def get_feasible_accepting_state(self):
        """
        get feasbile accepting/final state, or check whether an accepting state is feaasible
        :return:
        """
        accept = self.buchi_graph.graph['accept']
        self.buchi_graph.graph['accept'] = []
        for ac in accept:
            for init in self.buchi_graph.graph['init']:
                if self.min_length[(init, ac)] < np.inf and self.min_length[(ac, ac)] < np.inf:
                    self.buchi_graph.graph['accept'].append(ac)
                    break

    def robot2region(self, symbol):
        """
        pair of robot and corresponding regions in the expression
        :param symbol: logical expression
        :return: robot index : regions
        eg: input:  exp = 'l1_1 & l3_1 & l4_1 & l4_6 | l3_4 & l5_6'
            output: {1: ['l1_1', 'l3_1', 'l4_1'], 4: ['l3_4'], 6: ['l4_6', 'l5_6']}
        """

        robot_region = dict()
        for r in range(self.number_of_robots):
            findall = re.findall(r'(l\d+?_{0})[^0-9]'.format(r + 1), symbol) + re.findall(r'(c\d+?_{0})[^0-9]'.format(r + 1), symbol)
            if findall:
                robot_region[str(r + 1)] = findall

        return robot_region
    
    """ original"""  
    # def reassign(self):
    #     """
    #     parses buchi_graph and does necessary reassignment.
    #     Returns
    #     -------
    #     If reassignemnt is done, returns true
    #     else false.
    #     """
    #     reassign_flag = False
    #     for edge in self.buchi_graph.edges:
    #         edge_skill = self.buchi_graph.edges[(edge)]['transition_skill']
    #         edge_truth = self.buchi_graph.edges[(edge)]['truth']
    #         print("\n\n here1",self.buchi_graph.edges[(edge)]['AP'])
    #         if edge_skill:
    #             task_assign_curr = self.buchi_graph.edges[(edge)]['task_assign']
    #             robot_assign = get_robot_assignments(task_assign_curr,edge_truth) # dictionary containing robot number and its assigned task
    #             edge_task_fail_list = [] #contains failed_task,robots avilable for task and the penalty for failure
    #             skilled_robs_avlbl={}
    #             skilled_robs_unavlbl={}
    #             robot_prevelance = [0]*(self.number_of_robots+1) 
    #             # robot_prevelance keeps track of how many tasks a robot can attmpt
    #             # note 0 index of robot_prevelance is offsetted!! 
    #             # that is robot_prevelance[1] is for robot 1 
    #             for edge_task in edge_skill:
    #                 skill_needed = edge_skill[edge_task]
    #                 skilled_robs_for_task = self.rob_team.get_able_robs(skill_needed)
    #                 skilled_robs_avlbl[edge_task] = []
    #                 skilled_robs_unavlbl[edge_task] = []
    #                 for rob in skilled_robs_for_task:
    #                     robot_prevelance[rob]+=1
    #                     if rob in get_used_robots(task_assign_curr):
    #                         skilled_robs_unavlbl[edge_task].append(rob)
    #                     else:
    #                         skilled_robs_avlbl[edge_task].append(rob)
    #                 if task_assign_curr[edge_task][0] not in skilled_robs_for_task:
    #                     edge_task_fail_list.append((edge_task,len(skilled_robs_for_task),
    #                                                 task_assign_curr[edge_task][2]))
    #                     # num_able_robs.append(len(skilled_robs_for_task))
    #                     # penalty_for_fail.append(task_assign_curr[edge_task][2])  
    #             '''
    #             at this point i have all available robots for edge tasks
    #             we compared with task_assign and see if reassignment is needed
    #             needed reassignment is stored in edge_task_fail_list
    #             Now we implement CSP MRV on skilled_robs_avlbl
    #             while keeping track of already used robs in task_assign_curr
    #             for fail in edge_task_fail_list:
    #             '''
    #             reassignment_needed = False
    #             if edge_task_fail_list:
    #                 print("\n",self.buchi_graph.edges[(edge)]['AP'], task_assign_curr)
    #                 reassignment_needed = True
    #                 reassign_flag = True
    #             while edge_task_fail_list:
    #                 edge_task_fail_list = sorted(edge_task_fail_list, 
    #                                              key=lambda k: (k[1], k[2]), reverse=False)
    #                 # unsolvable_fails = []
    #                 fail_task = edge_task_fail_list[0][0]
    #                 fail_rob = task_assign_curr[fail_task][0]
    #                 answer_node = BFS(fail_task, task_assign_curr,robot_assign,skilled_robs_avlbl, skilled_robs_unavlbl)
    #                 parent_node = answer_node.parent
    #                 replacement_loop = False
    #                 leaf_node=True
    #                 if not parent_node:
    #                     task_assign_curr[answer_node.task][0] = 0
    #                     task_assign_curr[answer_node.task][1] = task_assign_curr[answer_node.task][2]
                        
    #                 if fail_rob == answer_node.robot_number and parent_node:
    #                     replacement_loop = True
    #                 while parent_node:
    #                     if leaf_node:
    #                         if answer_node.available:
    #                             use_up_robot(answer_node.robot_number,
    #                                          skilled_robs_unavlbl, skilled_robs_avlbl)
    #                         else:
    #                             task_assign_curr[answer_node.task][0] = 0
    #                             task_assign_curr[answer_node.task][1] = task_assign_curr[answer_node.task][2]
    #                     leaf_node = False
    #                     task_assign_curr[parent_node.task][0] = answer_node.robot_number
    #                     answer_node = parent_node
    #                     parent_node = answer_node.parent
    #                 if not replacement_loop:
    #                     free_up_robot(answer_node.robot_number,
    #                                   skilled_robs_unavlbl, skilled_robs_avlbl)
    #                 edge_task_fail_list.pop(0)
                    
               
    #                     # edge_task_fail_list.append((from_task,
    #                     #                             len(skilled_robs_unavlbl[from_task])+len(skilled_robs_avlbl[from_task]),
    #                     #                             task_assign_curr[from_task][2]))
    #                     # free_up_robot(task_assign_curr[fail_task][0], 
    #                     #               skilled_robs_unavlbl, skilled_robs_avlbl)
    #                     # task_assign_curr[fail_task][0] = rob
    #                     # task_assign_curr[from_task][0] = 0
    #                     # use_up_robot(rob, skilled_robs_unavlbl, skilled_robs_avlbl)
    #                     # edge_task_fail_list.pop(0)
    #                     # task_assign_curr[fail_task][1] = 0

    #             if reassignment_needed:
    #                 print(task_assign_curr)
    #                 self.update_buchi_graph_edge(edge,task_assign_curr)
    #     return reassign_flag            
             
    """ MODIFIED!!!! for all truth tables in case of OR"""              
    def reassign(self,init_state):
        """
        parses buchi_graph and does necessary reassignment.
        Returns
        -------
        If reassignemnt is done, returns true
        else false.
        """
        reassign_flag = False
        remaining_edges=[]
        ''' accept to accept_al and vice versa loc 4/4'''
        # target_state = self.buchi_graph.graph['accept'][0]
        # for path in nx.all_simple_paths(self.buchi_graph, source=init_state, target=target_state):
        for path in nx.all_simple_paths(self.buchi_graph, source=init_state, target='accept_all'):
        
            l = len(path)
            for i in range(l-1):
                start = path[i]
                end = path[i+1]
                edgex = (start,end)
                if edgex not in remaining_edges:
                    remaining_edges.append(edgex)
            for i in range(l):
                edgex = (path[i],path[i])
                if edgex not in remaining_edges and edgex in self.buchi_graph.edges:
                    remaining_edges.append(edgex)
        print("Length of remaining edges:",len(remaining_edges))
        ctr1=0        
        ctr2=0        
        ctr3=0
        ctr4=0
        for edge in remaining_edges:
            # test_edge = ('T0_S29','T2_S69')
            # if edge == test_edge:
            #     blah =9
            found_solution_for_edge = False
            # print("\n\n\n\n",edge,"\n",self.buchi_graph.edges[(edge)])
            for counter in range(len(self.buchi_graph.edges[(edge)]['all_truth'])):
                # if not found_solution_for_edge:
                # if 1:
                ctr1+=1
                self.ctr_alternate_transition(edge[0], edge[1], counter)
                edge_skill = self.buchi_graph.edges[(edge)]['transition_skill']
                edge_truth = self.buchi_graph.edges[(edge)]['truth']
                # print("\n\n here1",self.buchi_graph.edges[(edge)]['AP'])
                if edge_skill:
                    ctr2+=1
                    task_assign_curr = self.buchi_graph.edges[(edge)]['task_assign']
                    robot_assign = get_robot_assignments(task_assign_curr,edge_truth) # dictionary containing robot number and its assigned task
                    edge_task_fail_list = [] #contains failed_task,robots avilable for task and the penalty for failure
                    skilled_robs_avlbl={}
                    skilled_robs_unavlbl={}
                    robot_prevelance = [0]*(self.number_of_robots+1) 
                    # robot_prevelance keeps track of how many tasks a robot can attmpt
                    # note 0 index of robot_prevelance is offsetted!! 
                    # that is robot_prevelance[1] is for robot 1 
                    # print("\nx\nx\nx\nx\nx\nx\nx\nx\nx\nx")
                    for edge_task in edge_skill:
                        skill_needed = edge_skill[edge_task]
                        # print("\n\nedge_task",edge_task,skill_needed)
                        skilled_robs_for_task = self.rob_team.get_able_robs(skill_needed)
                        # print(skilled_robs_for_task)
                        # print(task_assign_curr,edge_truth)
                        # print(get_used_robots(task_assign_curr,edge_truth))
                        skilled_robs_avlbl[edge_task] = []
                        skilled_robs_unavlbl[edge_task] = []
                        for rob in skilled_robs_for_task:
                            robot_prevelance[rob]+=1
                            if rob in get_used_robots(task_assign_curr,edge_truth):
                                skilled_robs_unavlbl[edge_task].append(rob)
                            else:
                                constrained = False
                                pair = edge_task.split('_')
                                const_task = pair[0]+'_'+str(rob)
                                if const_task in edge_truth.keys():
                                    if not edge_truth[const_task]:
                                        constrained = True
                                if not constrained:
                                    skilled_robs_avlbl[edge_task].append(rob)
                        if task_assign_curr[edge_task][0] not in skilled_robs_for_task:
                            if edge_truth[edge_task]:
                                edge_task_fail_list.append((edge_task,len(skilled_robs_for_task),
                                                            task_assign_curr[edge_task][2]))
                            # num_able_robs.append(len(skilled_robs_for_task))
                            # penalty_for_fail.append(task_assign_curr[edge_task][2])  
                    '''
                    at this point i have all available robots for edge tasks
                    we compared with task_assign and see if reassignment is needed
                    needed reassignment is stored in edge_task_fail_list
                    Now we implement CSP MRV on skilled_robs_avlbl
                    while keeping track of already used robs in task_assign_curr
                    for fail in edge_task_fail_list:
                    '''
                    # print("skilled_robs_unavlbl",skilled_robs_unavlbl)
                    # print("skilled_robs_avlbl",skilled_robs_avlbl)
                    reassignment_needed = False
                    if edge_task_fail_list:
                        # print("\n",self.buchi_graph.edges[(edge)]['AP'], task_assign_curr)
                        reassignment_needed = True
                        reassign_flag = True
                        ctr3+=1
                    while edge_task_fail_list:
                        ctr4+=1
                        edge_task_fail_list = sorted(edge_task_fail_list, 
                                                     key=lambda k: (k[1], k[2]), reverse=False)
                        # unsolvable_fails = []
                        fail_task = edge_task_fail_list[0][0]
                        fail_rob = task_assign_curr[fail_task][0]
                        robot_assign = get_robot_assignments(task_assign_curr,edge_truth)
                        answer_node = BFS(fail_task, task_assign_curr,robot_assign,skilled_robs_avlbl, skilled_robs_unavlbl)
                        parent_node = answer_node.parent
                        replacement_loop = False
                        leaf_node=True
                        if not parent_node:
                            task_assign_curr[answer_node.task][0] = 0
                            task_assign_curr[answer_node.task][1] = task_assign_curr[answer_node.task][2]
                        else:
                            found_solution_for_edge=True #ISSSUE If edge_task_fail has more than 1 fail then you need to set this true only if everything is fixed
                        if fail_rob == answer_node.robot_number and parent_node:
                            replacement_loop = True
                        while parent_node:
                            if leaf_node:
                                if answer_node.available:
                                    use_up_robot(answer_node.robot_number,
                                                 skilled_robs_unavlbl, skilled_robs_avlbl)
                                else:
                                    task_assign_curr[answer_node.task][0] = 0
                                    task_assign_curr[answer_node.task][1] = task_assign_curr[answer_node.task][2]
                            leaf_node = False
                            task_assign_curr[parent_node.task][0] = answer_node.robot_number
                            answer_node = parent_node
                            parent_node = answer_node.parent
                        if not replacement_loop:
                            free_up_robot(answer_node.robot_number,
                                          skilled_robs_unavlbl, skilled_robs_avlbl)
                        edge_task_fail_list.pop(0)
                        
                   
                            # edge_task_fail_list.append((from_task,
                            #                             len(skilled_robs_unavlbl[from_task])+len(skilled_robs_avlbl[from_task]),
                            #                             task_assign_curr[from_task][2]))
                            # free_up_robot(task_assign_curr[fail_task][0], 
                            #               skilled_robs_unavlbl, skilled_robs_avlbl)
                            # task_assign_curr[fail_task][0] = rob
                            # task_assign_curr[from_task][0] = 0
                            # use_up_robot(rob, skilled_robs_unavlbl, skilled_robs_avlbl)
                            # edge_task_fail_list.pop(0)
                            # task_assign_curr[fail_task][1] = 0
    
                    if reassignment_needed:
                        # print(task_assign_curr)
                        self.update_buchi_graph_edge(edge,task_assign_curr,counter)
                        '''NOTE: here penalty will be updated for weight according
                        to the counter ... so in case of least violition we can pick 
                        the counter which has least penalty
                        ''' 
            final_edge_weights = self.buchi_graph.edges[(edge)]['all_weight']
            counter = final_edge_weights.index(min(final_edge_weights))
            self.ctr_alternate_transition(edge[0], edge[1], counter)
        print("counters:",ctr1,ctr2,ctr3,ctr4)
        return reassign_flag,len(remaining_edges)       
    
    
    """ base case for comparison-global reassign in failed edges"""              
    def reassign_global_bad(self,init_state):
        """
        parses buchi_graph and does necessary reassignment.
        Returns
        -------
        If reassignemnt is done, returns true
        else false.
        """
        reassign_flag = False
        remaining_edges=[]
        ''' accept to accept_al and vice versa loc 4/4'''
        # target_state = self.buchi_graph.graph['accept'][0]
        # for path in nx.all_simple_paths(self.buchi_graph, source=init_state, target=target_state):
        for path in nx.all_simple_paths(self.buchi_graph, source=init_state, target='accept_all'):
        
            l = len(path)
            for i in range(l-1):
                start = path[i]
                end = path[i+1]
                edgex = (start,end)
                if edgex not in remaining_edges:
                    remaining_edges.append(edgex)
            for i in range(l):
                edgex = (path[i],path[i])
                if edgex not in remaining_edges and edgex in self.buchi_graph.edges:
                    remaining_edges.append(edgex)
        print("Length of remaining edges:",len(remaining_edges))
        ctr1=0        
        ctr2=0        
        ctr3=0
        ctr4=0
        for edge in remaining_edges:
            # test_edge = ('T0_S29','T2_S69')
            # if edge == test_edge:
            #     blah =9
            found_solution_for_edge = False
            # print("\n\n\n\n",edge,"\n",self.buchi_graph.edges[(edge)])
            for counter in range(len(self.buchi_graph.edges[(edge)]['all_truth'])):
                # if not found_solution_for_edge:
                # if 1:
                ctr1+=1
                self.ctr_alternate_transition(edge[0], edge[1], counter)
                edge_skill = self.buchi_graph.edges[(edge)]['transition_skill']
                edge_truth = self.buchi_graph.edges[(edge)]['truth']
                # print("\n\n here1",self.buchi_graph.edges[(edge)]['AP'])
                if edge_skill:
                    ctr2+=1
                    task_assign_curr = self.buchi_graph.edges[(edge)]['task_assign']
                    robot_assign = get_robot_assignments(task_assign_curr,edge_truth) # dictionary containing robot number and its assigned task
                    edge_task_fail_list = [] #contains failed_task,robots avilable for task and the penalty for failure
                    skilled_robs_avlbl={}
                    skilled_robs_unavlbl={}
                    robot_prevelance = [0]*(self.number_of_robots+1) 
                    # robot_prevelance keeps track of how many tasks a robot can attmpt
                    # note 0 index of robot_prevelance is offsetted!! 
                    # that is robot_prevelance[1] is for robot 1 
                    # print("\nx\nx\nx\nx\nx\nx\nx\nx\nx\nx")
                    for edge_task in edge_skill:
                        skill_needed = edge_skill[edge_task]
                        # print("\n\nedge_task",edge_task,skill_needed)
                        skilled_robs_for_task = self.rob_team.get_able_robs(skill_needed)
                        # print(skilled_robs_for_task)
                        # print(task_assign_curr,edge_truth)
                        # print(get_used_robots(task_assign_curr,edge_truth))
                        skilled_robs_avlbl[edge_task] = []
                        skilled_robs_unavlbl[edge_task] = []
                        for rob in skilled_robs_for_task:
                            robot_prevelance[rob]+=1
                            if rob in get_used_robots(task_assign_curr,edge_truth):
                                skilled_robs_unavlbl[edge_task].append(rob)
                            else:
                                constrained = False
                                pair = edge_task.split('_')
                                const_task = pair[0]+'_'+str(rob)
                                if const_task in edge_truth.keys():
                                    if not edge_truth[const_task]:
                                        constrained = True
                                if not constrained:
                                    skilled_robs_avlbl[edge_task].append(rob)
                        if task_assign_curr[edge_task][0] not in skilled_robs_for_task:
                            if edge_truth[edge_task]:
                                edge_task_fail_list.append((edge_task,len(skilled_robs_for_task),
                                                            task_assign_curr[edge_task][2]))
                            # num_able_robs.append(len(skilled_robs_for_task))
                            # penalty_for_fail.append(task_assign_curr[edge_task][2])  
                    '''
                    at this point i have all available robots for edge tasks
                    we compared with task_assign and see if reassignment is needed
                    needed reassignment is stored in edge_task_fail_list
                    Now we implement CSP MRV on skilled_robs_avlbl
                    while keeping track of already used robs in task_assign_curr
                    for fail in edge_task_fail_list:
                    '''
                    # print("skilled_robs_unavlbl",skilled_robs_unavlbl)
                    # print("skilled_robs_avlbl",skilled_robs_avlbl)
                    reassignment_needed = False
                    if edge_task_fail_list:
                        # print("\n",self.buchi_graph.edges[(edge)]['AP'], task_assign_curr)
                        reassignment_needed = True
                        reassign_flag = True
                        ctr3+=1
                    while edge_task_fail_list:
                        ctr4+=1
                        edge_task_fail_list = sorted(edge_task_fail_list, 
                                                     key=lambda k: (k[1], k[2]), reverse=False)
                        # unsolvable_fails = []
                        fail_task = edge_task_fail_list[0][0]
                        fail_rob = task_assign_curr[fail_task][0]
                        robot_assign = get_robot_assignments(task_assign_curr,edge_truth)
                        answer_node = BFS(fail_task, task_assign_curr,robot_assign,skilled_robs_avlbl, skilled_robs_unavlbl)
                        parent_node = answer_node.parent
                        replacement_loop = False
                        leaf_node=True
                        if not parent_node:
                            task_assign_curr[answer_node.task][0] = 0
                            task_assign_curr[answer_node.task][1] = task_assign_curr[answer_node.task][2]
                        else:
                            found_solution_for_edge=True #ISSSUE If edge_task_fail has more than 1 fail then you need to set this true only if everything is fixed
                        if fail_rob == answer_node.robot_number and parent_node:
                            replacement_loop = True
                        while parent_node:
                            if leaf_node:
                                if answer_node.available:
                                    use_up_robot(answer_node.robot_number,
                                                 skilled_robs_unavlbl, skilled_robs_avlbl)
                                else:
                                    task_assign_curr[answer_node.task][0] = 0
                                    task_assign_curr[answer_node.task][1] = task_assign_curr[answer_node.task][2]
                            leaf_node = False
                            task_assign_curr[parent_node.task][0] = answer_node.robot_number
                            answer_node = parent_node
                            parent_node = answer_node.parent
                        if not replacement_loop:
                            free_up_robot(answer_node.robot_number,
                                          skilled_robs_unavlbl, skilled_robs_avlbl)
                        edge_task_fail_list.pop(0)
                        
                   
                            # edge_task_fail_list.append((from_task,
                            #                             len(skilled_robs_unavlbl[from_task])+len(skilled_robs_avlbl[from_task]),
                            #                             task_assign_curr[from_task][2]))
                            # free_up_robot(task_assign_curr[fail_task][0], 
                            #               skilled_robs_unavlbl, skilled_robs_avlbl)
                            # task_assign_curr[fail_task][0] = rob
                            # task_assign_curr[from_task][0] = 0
                            # use_up_robot(rob, skilled_robs_unavlbl, skilled_robs_avlbl)
                            # edge_task_fail_list.pop(0)
                            # task_assign_curr[fail_task][1] = 0
    
                    if reassignment_needed:
                        # print(task_assign_curr)
                        self.update_buchi_graph_edge(edge,task_assign_curr,counter)
                        '''NOTE: here penalty will be updated for weight according
                        to the counter ... so in case of least violition we can pick 
                        the counter which has least penalty
                        ''' 
            final_edge_weights = self.buchi_graph.edges[(edge)]['all_weight']
            counter = final_edge_weights.index(min(final_edge_weights))
            self.ctr_alternate_transition(edge[0], edge[1], counter)
        print("counters:",ctr1,ctr2,ctr3,ctr4)
        return reassign_flag,len(remaining_edges)       
    
    # def reassign_old(self):
    #     """
    #     parses buchi_graph and does necessary reassignment.
    #     Returns
    #     -------
    #     If reassignemnt is done, returns true
    #     else false.
    #     """
    #     reassign_flag = False
    #     for edge in self.buchi_graph.edges:
    #         edge_skill = self.buchi_graph.edges[(edge)]['transition_skill']
            
    #         if edge_skill:
    #             task_assign_curr = self.buchi_graph.edges[(edge)]['task_assign']
    #             edge_task_fail_list = [] #contains failed_task,robots avilable fot task and the penalty for failure
    #             skilled_robs_avlbl={}
    #             skilled_robs_unavlbl={}
    #             robot_prevelance = [0]*(self.number_of_robots+1) 
    #             # robot_prevelance keeps track of how many tasks a robot can attmpt
    #             # note 0 index of robot_prevelance is offsetted!!
    #             for edge_task in edge_skill:
    #                 skill_needed = edge_skill[edge_task]
    #                 skilled_robs_for_task = self.rob_team.get_able_robs(skill_needed)
    #                 skilled_robs_avlbl[edge_task] = []
    #                 skilled_robs_unavlbl[edge_task] = []
    #                 for rob in skilled_robs_for_task:
    #                     robot_prevelance[rob]+=1
    #                     if rob in get_used_robots(task_assign_curr):
    #                         skilled_robs_unavlbl[edge_task].append(rob)
    #                     else:
    #                         skilled_robs_avlbl[edge_task].append(rob)
    #                 if task_assign_curr[edge_task][0] not in skilled_robs_for_task:
    #                     edge_task_fail_list.append((edge_task,len(skilled_robs_for_task),
    #                                                 task_assign_curr[edge_task][2]))
    #                     # num_able_robs.append(len(skilled_robs_for_task))
    #                     # penalty_for_fail.append(task_assign_curr[edge_task][2])  
    #             '''
    #             at this point i have all available robots for edge tasks
    #             we compared with task_assign and see if reassignment is needed
    #             needed reassignment is stored in edge_task_fail_list
    #             Now we implement CSP MRV on skilled_robs_avlbl
    #             while keeping track of already used robs in task_assign_curr
    #             for fail in edge_task_fail_list:
    #             '''
    #             reassignment_needed = False
    #             if edge_task_fail_list:
    #                 reassignment_needed = True
    #                 reassign_flag = True
    #             while edge_task_fail_list:
    #                 edge_task_fail_list = sorted(edge_task_fail_list, 
    #                                              key=lambda k: (k[1], k[2]), reverse=False)
    #                 # unsolvable_fails = []
    #                 fail_task = edge_task_fail_list[0][0]
    #                 if skilled_robs_avlbl[fail_task]:
    #                     rob = get_least_prevelant_robot(robot_prevelance,
    #                                                     skilled_robs_avlbl[fail_task])
    #                     free_up_robot(task_assign_curr[fail_task][0], 
    #                                   skilled_robs_unavlbl, skilled_robs_avlbl)
    #                     task_assign_curr[fail_task][0] = rob
    #                     use_up_robot(rob, skilled_robs_unavlbl, skilled_robs_avlbl)
    #                     edge_task_fail_list.pop(0)
    #                     task_assign_curr[fail_task][1] = 0
    #                 elif skilled_robs_unavlbl[fail_task]:
    #                     rob,from_task = search_from_task_with_spare(skilled_robs_unavlbl[fail_task], 
    #                                                 skilled_robs_avlbl, task_assign_curr)
    #                     if rob:
    #                         edge_task_fail_list.append((from_task,
    #                                                     len(skilled_robs_unavlbl[from_task])+len(skilled_robs_avlbl[from_task]),
    #                                                     task_assign_curr[from_task][2]))
    #                         free_up_robot(task_assign_curr[fail_task][0], 
    #                                       skilled_robs_unavlbl, skilled_robs_avlbl)
    #                         task_assign_curr[fail_task][0] = rob
    #                         task_assign_curr[from_task][0] = 0
    #                         use_up_robot(rob, skilled_robs_unavlbl, skilled_robs_avlbl)
    #                         edge_task_fail_list.pop(0)
    #                         task_assign_curr[fail_task][1] = 0
    #                     else:
    #                         rob,from_task = search_from_task_with_low_penalty(skilled_robs_unavlbl[fail_task],
    #                                                                           task_assign_curr[fail_task][2],
    #                                                                           task_assign_curr)
    #                         if rob:
    #                             edge_task_fail_list.append((from_task,
    #                                                         len(skilled_robs_unavlbl[from_task])+len(skilled_robs_avlbl[from_task]),
    #                                                         task_assign_curr[from_task][2]))
    #                             free_up_robot(task_assign_curr[fail_task][0], 
    #                                           skilled_robs_unavlbl, skilled_robs_avlbl)
    #                             task_assign_curr[fail_task][0] = rob
    #                             task_assign_curr[from_task][0] = 0
    #                             use_up_robot(rob, skilled_robs_unavlbl, skilled_robs_avlbl)
    #                             edge_task_fail_list.pop(0)
    #                             task_assign_curr[fail_task][1] = 0
    #                         else:
    #                             ''' Failure '''
    #                             # fail_task,num,penalty = edge_task_fail_list.pop(0)
    #                             edge_task_fail_list.pop(0)
    #                             task_assign_curr[fail_task][0] = 0
    #                             task_assign_curr[fail_task][1] = task_assign_curr[fail_task][2]
                                
    #                 else:
    #                     ''' Failure'''
    #                     edge_task_fail_list.pop(0)
    #                     task_assign_curr[fail_task][0] = 0
    #                     task_assign_curr[fail_task][1] = task_assign_curr[fail_task][2]

    #             if reassignment_needed:
    #                 self.update_buchi_graph_edge(edge,task_assign_curr)
    #     return reassign_flag            
                    
    def update_buchi_graph_edge(self,edge,task_assign_curr, counter):
        new_labels, penalty = get_new_task_labels(task_assign_curr)
        update_edge_with_new_labels(self.buchi_graph.edges[(edge)],new_labels, penalty, counter)
        
    def update_alternate_transition(self, state, next_state):
        """
        updates the truth to next alternate possiblity
        that enables transition from state to next_state.
        :param state: current state
        :param next_state: next state
        :return: success : true if success in finding alternate transition
        """
        edge_info = self.buchi_graph.edges[state,next_state]
        next_counter = edge_info['counter'] + 1
        possible_truths = len(edge_info['all_truth'])
        #if all possible transitions have been used then return false
        if next_counter>=possible_truths:
            return False
        
        self.buchi_graph.edges[state,next_state]['truth'] = edge_info['all_truth'][next_counter]
        self.buchi_graph.edges[state,next_state]['avoid'] = edge_info['all_avoid'][next_counter]
        self.buchi_graph.edges[state,next_state]['counter'] = next_counter
        return True
    
    def previous_alternate_transition(self, state, next_state):
        """
        updates the truth to previous alternate possiblity
        that enables transition from state to next_state.
        :param state: current state
        :param next_state: next state
        :return: success : true if success in finding alternate transition
        """
        edge_info = self.buchi_graph.edges[state,next_state]
        next_counter = edge_info['counter'] - 1
        #if all possible transitions have been used then return false
        if next_counter<0:
            return False
        
        self.buchi_graph.edges[state,next_state]['truth'] = edge_info['all_truth'][next_counter]
        self.buchi_graph.edges[state,next_state]['avoid'] = edge_info['all_avoid'][next_counter]
        self.buchi_graph.edges[state,next_state]['counter'] = next_counter
        return True
    
    def ctr_alternate_transition(self, state, next_state, next_counter):
        """
        updates the truth to alternate possiblity pointed by next_counter
        that enables transition from state to next_state.
        :param state: current state
        :param next_state: next state
        :param next_counter: will set counter to this value
        :return: success : true if success in finding alternate transition
        """
        edge_info = self.buchi_graph.edges[state,next_state]
        possible_truths = len(edge_info['all_truth'])
        #if all possible transitions have been used then return false
        if next_counter<0 and next_counter>=possible_truths:
            return False
        
        self.buchi_graph.edges[state,next_state]['truth'] = edge_info['all_truth'][next_counter]
        self.buchi_graph.edges[state,next_state]['avoid'] = edge_info['all_avoid'][next_counter]
        self.buchi_graph.edges[state,next_state]['transition_skill'] = edge_info['all_transition_skill'][next_counter]
        self.buchi_graph.edges[state,next_state]['task_assign'] = edge_info['all_task_assign'][next_counter]
        self.buchi_graph.edges[state,next_state]['weight'] = edge_info['all_weight'][next_counter]
        self.buchi_graph.edges[state,next_state]['task_label_ref'] = edge_info['all_task_label_ref'][next_counter]
        
        self.buchi_graph.edges[state,next_state]['counter'] = next_counter
        return True
    
"""
Helper functions
"""
def get_used_robots(task_assign_curr,edge_truth): #edge truth to determine if the robot is in assignment for negation
    used_robots = []
    for key in task_assign_curr:
        if edge_truth[key]:
            used_robots.append(task_assign_curr[key][0])
    return used_robots

def get_robot_assignments(task_assign_curr,truth):
    robot_assign = {}
    for key in task_assign_curr:
        if truth[key]:
            robot_assign[task_assign_curr[key][0]] = key
    return robot_assign

def free_up_robot(rob,skilled_robs_unavlbl,skilled_robs_avlbl):
    for key in skilled_robs_unavlbl:
        if rob in skilled_robs_unavlbl[key]:
            skilled_robs_unavlbl[key].remove(rob)
            skilled_robs_avlbl[key].append(rob)
def use_up_robot(rob,skilled_robs_unavlbl,skilled_robs_avlbl):
    for key in skilled_robs_avlbl:
        if rob in skilled_robs_avlbl[key]:
            skilled_robs_avlbl[key].remove(rob)
            skilled_robs_unavlbl[key].append(rob)
    
    
def get_least_prevelant_robot(robot_prevelance, skilled_robs_avlbl_for_task):
    least_prevelant_robot = None
    least_prevelance = 99999
    for rob in skilled_robs_avlbl_for_task:
        if robot_prevelance[rob] < least_prevelance:
            least_prevelant_robot = rob
            least_prevelance = robot_prevelance[rob]
    return least_prevelant_robot
                
def search_from_task_with_spare(unavlbl_robs, skilled_robs_avlbl, task_assign_curr):
    for unavlbl_rob in unavlbl_robs:
        for task in task_assign_curr:
            if task_assign_curr[task][0] == unavlbl_rob:
                if skilled_robs_avlbl[task]:
                    return unavlbl_rob, task
    return None,None                
        
def search_from_task_with_low_penalty(unavlbl_robs,fail_task_penalty,task_assign_curr):
    lowest_penalty = fail_task_penalty
    lowest_penalty_rob = None
    lowest_penalty_task = None
    for unavlbl_rob in unavlbl_robs:
        for task in task_assign_curr:
            if task_assign_curr[task][0] == unavlbl_rob:
                if task_assign_curr[task][2] > lowest_penalty:
                    lowest_penalty = task_assign_curr[task][2]
                    lowest_penalty_rob = unavlbl_rob
                    lowest_penalty_task = task
    return lowest_penalty_rob, lowest_penalty_task
        
def get_new_task_labels(task_assign_curr):
    new_labels = {}
    penalty = 0
    for task in task_assign_curr:
        penalty += task_assign_curr[task][1]
        pair = task.split('_')
        if int(pair[1]) != task_assign_curr[task][0]:
            new_labels[task] = pair[0]+'_'+str(task_assign_curr[task][0])
    return new_labels, penalty

def update_edge_with_new_labels(edge_details,new_labels, penalty, counter):
    for old_key in new_labels:
        if int(new_labels[old_key].split('_')[1])==0:
            if edge_details['truth'][old_key] == True:
                edge_details['truth'].pop(old_key)
        else:
            if int(old_key.split('_')[1])==0:
                edge_details['truth'][new_labels[old_key]] =  True
            else:    
                edge_details['truth'][new_labels[old_key]] = edge_details['truth'].pop(old_key)
        
        edge_details['transition_skill'][new_labels[old_key]] = edge_details['transition_skill'].pop(old_key)
        edge_details['task_assign'][new_labels[old_key]] = edge_details['task_assign'].pop(old_key)
    
    edge_details['weight'] = -penalty+0.01
    edge_details['all_weight'][counter] = -penalty+0.01
    for task_key in edge_details['task_label_ref']:
        if edge_details['task_label_ref'][task_key] in new_labels:
            edge_details['task_label_ref'][task_key] = new_labels[edge_details['task_label_ref'][task_key]]
    
        
def BFS(fail_task, task_assign_curr,robot_assign,skilled_robs_avlbl, skilled_robs_unavlbl):
    fail_robot = task_assign_curr[fail_task][0]
    visited = []
    root_node = BFS_node(fail_robot, False, fail_task, task_assign_curr[fail_task][2])
    lowest_penalty = task_assign_curr[fail_task][2]
    leaf_node = root_node
    to_visit = [root_node]
    visited = []
    found_solution = False
    tree_root = True
    # print("\nfailedrobot and task:",fail_robot,fail_task)
    while to_visit and not found_solution:
        parent_node = to_visit.pop(0)
        if parent_node.robot_number not in visited:
            if not tree_root:
                visited.append(parent_node.robot_number)
            tree_root=False
            # print("\n\n pt=",parent_node.task,"\n",skilled_robs_avlbl[parent_node.task],"\n",skilled_robs_unavlbl[parent_node.task])
            for child in skilled_robs_avlbl[parent_node.task]:
                leaf_node = BFS_node(child, parent = parent_node)
                found_solution = True
                break
            if found_solution:
                break
            for child in skilled_robs_unavlbl[parent_node.task]:
                if child == root_node.robot_number:
                    leaf_node = BFS_node(child, parent = parent_node)
                    found_solution = True
                    break
                elif child not in visited:
                    # print("child=",child, robot_assign,
                                           # parent_node)
                    # print("failtask=",fail_task, task_assign_curr,robot_assign,skilled_robs_avlbl, skilled_robs_unavlbl)
                    child_node = BFS_node(child,available=False, task=robot_assign[child],
                                          penalty=task_assign_curr[robot_assign[child]][2],
                                          parent = parent_node)
                    to_visit.append(child_node)
                    if child_node.penalty>lowest_penalty:
                        lowest_penalty = child_node.penalty
                        leaf_node = child_node
        if found_solution:
            break
        
    return leaf_node
        
        
        

class BFS_node:
    def __init__(self, robot_number, available=True, task=None, penalty=0,  parent=None):
        self.robot_number = robot_number
        self.task = task
        self.available = available
        self.penalty= penalty
        self.parent = parent

    def set_parent(self, parent):
        self.parent = parent

    def update_penalty(self, penalty):
        self.penalty = penalty
    
    
    
    
    
    
    
    
    
        
        
        