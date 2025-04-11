# MinVio-MRP
MinVio-MRP is an implementation of a multi-robot planning framework that combines Linear Temporal Logic (LTL) specifications with failure-aware task reassignment. The goal of the planner is to enable a team of robots to complete complex missions defined using LTL—even in the presence of robot skill failures—by reassigning tasks of failed robos to the surviving robots and generating new plans that minimize the violation of the original mission objectives.

[1] S. Kalluraya, B. Zhou, Y. Kantaros, "Minimum-Violation Temporal Logic Planning for Heterogeneous Robots under Robot Skill Failures", https://arxiv.org/pdf/2410.17188

# Requirements
* [Python >=3.6](https://www.python.org/downloads/)
* [sympy](https://www.sympy.org/en/index.html)
* [re]()
* [Pyvisgraph](https://github.com/TaipanRex/pyvisgraph)
* [NetworkX](https://networkx.github.io)
* [Shapely](https://github.com/Toblerity/Shapely)
* [scipy](https://www.scipy.org)
* [matplotlib](https://matplotlib.org)
* [termcolor](https://pypi.org/project/termcolor/)
* [visilibity](https://github.com/tsaoyu/PyVisiLibity)



# Usage
## Structures
* Class [Task](task.py) defines the task specified in LTL
* Class [Workspace](workspace.py) define the workspace where robots reside
* Class [Landmark](workspace.py) define the landmarks in the workspace
* Class [Buchi](buchi_parse.py) constructs the graph of NBA from LTL formula
* Class [Geodesic](geodesic_path.py) constructs geodesic path for given environment
* Class [BiasedTree](biased_tree.py) involves the initialization of the tree and relevant operations
* Function [construction_biased_tree](construct_biased_tree.py) incrementally grow the tree
* Script [biased_TLRRT_star.py](biased_TLRRT_star.py) contains the main function
* Functions [path_plot](draw_picture.py) and [path_print](draw_picture.py) draw and print the paths, respectively
* Functions [export_disc_to_txt](draw_picture.py) and [export_cov_to_txt](draw_picture.py) export discretized waypoints and covariance at waypoints, respectively
## Basic procedure
* First, in the class [Workspace](/workspace.py) specify the size of the workspace, the layout of landmarks and obstacles.
* Then, in the class [Landmark](/workspace.py) specify the landmark details for visualization.
* Then, specify the LTL task in the class [Task](task.py), which mainly involves the assigned task (self.formula). The assigned task is given as an LTL formula with predicates. The description of each predicate is specified in self.subformula.
* robust_mission.py is the main file that will run the code. Here, initialize the robots belonging to the Robot class, and specify the skills and teams. Next specify the failured robots and the timestamp when the failure occurs.
* When you run robust_mission.py, the planner first generates the offline plans (line 147 in the code). It then considers the occurance of failures and generates new plans starting from the failure timestep (line 296 in the code)
