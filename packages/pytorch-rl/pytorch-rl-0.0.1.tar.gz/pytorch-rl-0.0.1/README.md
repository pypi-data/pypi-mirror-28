# pytorch-rl
## DDPG 
Un-Trained		           | Trained
:-------------------------:|:-------------------------:
<img src="./assets/pendulum_untrained.gif" width="200">  |  <img src="./assets/pendulum_trained.gif" width="200">
## Double DQN
Un-Trained		           | Trained
:-------------------------:|:-------------------------:
<img src="./assets/cartpole_untrained.gif" width="200">  |  <img src="./assets/cartpole_trained.gif" width="200">

pytorch-rl is a python package based on pytorch library which aims to build standard deep reinforcement learning agent for the user to build various algorithms around it. pytorch-rl also includes some of the state-of-the-art implementations of popular deep reinforcement learning. 
## Installation
pytorch-rl can be easily installed using `pip`  as follows: 
```
pip install pytorch-rl
```
This code currently uses python 2.7 and is compatible with both CPU and GPU (cuda 8.0). 
## Usage
All the algorithmic implementations of a RL agent lies in the `rl` repository. While the RL agent (say DDPG) can be imported as follows, 
```
from rl.agents import DDPGAgent
```
The standard DNN model associated with particular agent can be imported as follows
```
from rl.models.ddpg import ActorNetwork, CriticNetwork
```
Similarly, to run one of our RL agents( say DDPG) on a standard environment, simply run the following command 
```
python examples/ddpg_pendulum.py
```
```
python examples/ddpg_cartpole.py
```
## TODO
Agents implemeted currently
- [x] DDPG 
- [x] DDQN
- [ ] Duel DQN
- [ ] CEM
