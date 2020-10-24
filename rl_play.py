import tensorflow as tf
from tf_agents.environments import tf_py_environment

from rl_game_environment import RLGameEnvironment

py_env = RLGameEnvironment(simulate=False)
env = tf_py_environment.TFPyEnvironment(py_env)

saved_policy = tf.compat.v2.saved_model.load('policies/exploit_policy_50')
policy_state = saved_policy.get_initial_state(batch_size=1)
time_step = env.reset()
while True:
    policy_step = saved_policy.action(time_step, policy_state)
    policy_state = policy_step.state
    time_step = env.step(policy_step.action)
