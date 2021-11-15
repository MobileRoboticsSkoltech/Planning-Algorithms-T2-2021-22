import matplotlib.pyplot as plt
import numpy as np
import pickle
from environment import State, ManipulatorEnv
from rrt import RRTPlanner


# You are free to change any interfaces for your needs.


def main():
    with open("data.pickle", "rb") as handle:
        data = pickle.load(handle)

    start_state = State(np.array(data["start_state"]))
    goal_state = State(np.array(data["goal_state"]))
    env = ManipulatorEnv(obstacles=np.array(data["obstacles"]),
                         initial_state=start_state,
                         collision_threshold=data["collision_threshold"])

    planner = RRTPlanner(env)

    plan = planner.plan(start_state, goal_state)
    print("RRT planner has finished successfully")

    ax = plt.gca()
    ax.set_xlim([-4, 4])
    ax.set_ylim([-2.5, 2.5])
    for i, state in enumerate(plan):
        env.state = state
        env.render(plt_show=False)
        if i != len(plan) - 1:
            plt.pause(0.05)
            plt.clf()
        else:
            plt.show()


if __name__ == '__main__':
    main()
