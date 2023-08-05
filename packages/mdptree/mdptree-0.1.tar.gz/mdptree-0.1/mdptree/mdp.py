import numpy as np
from collections import namedtuple
from .graphs import OrientedTree
from .utils import fituple

__all__ = ['MDP', 'MDPProcess', 'MDPTree']


class MDP:
    def __init__(self, name, users, states, actions, processes):
        if len(actions) != len(states):
            raise ValueError(
                'The number of elements in the action argument differs from th'
                'e number of states.')
        if len(processes) != len(users):
            raise ValueError(
                'The number of processes differs from the number of users.')
        if any(not isinstance(_, MDPProcess) for _ in processes):
            raise TypeError('The type of the processes must be MDPProcess.')
        self.name = name
        self.users = fituple(users)
        self.nuser = len(users)
        self.states = fituple(states)
        self.nstate = len(states)
        self.actions = tuple(fituple(action) for action in actions)
        self.nactions = tuple(len(_) for _ in actions)
        self.processes = processes

    def get_occurences(self):
        """
        occurences = mdp.get_occurences()

        Returns
        -------
        occurences : list of nstate (nuser, naction[state], nstate) int ndarrays
            For a given user i, occurences[s1][i, a, s2] is the number of times
            the user went from state s1 to state s2 through action a.

        """
        occurences = [np.zeros((self.nuser, naction, self.nstate),
                               dtype=int) for naction in self.nactions]
        for iuser in range(self.nuser):
            occurences_ = [occurences[s1][iuser] for s1 in range(self.nstate)]
            self._get_occurences_user(iuser, occurences_)
        return occurences

    def _get_occurences_user(self, iuser, occurences):
        for s1, a, s2 in self.processes[iuser]:
            occurences[s1][a, s2] += 1

    def get_probabilities(self):
        """
        p_s2_s1a, p_s2_s1 = mdp.get_probabilities()

        Returns
        -------
        p_s2_s1a : list of nstate (nuser, naction[state], nstate) float ndarrays
            p_s2_s1a[s1][:, a, s2] is the probability P(s2|s1, a) of the users.
        p_s2_s1 : (nuser, nstate, nstate) float ndarray
            p_s2_s1[:, s1, s2] is the transition matrix, i.e. the probability
            P(s2|s1) of the users.

        """
        p_s2_s1a = [np.zeros((self.nuser, naction, self.nstate))
                    for naction in self.nactions]
        p_a_s1 = [np.zeros((self.nuser, naction))
                  for naction in self.nactions]
        p_s2_s1 = np.zeros((self.nuser, self.nstate, self.nstate))

        with np.errstate(invalid='ignore'):
            for iuser in range(self.nuser):
                self._get_probabilities_user(iuser, p_s2_s1a, p_a_s1, p_s2_s1)
        return p_s2_s1a, p_s2_s1

    def _get_probabilities_user(self, iuser, p_s2_s1a, p_a_s1, p_s2_s1):
        # some references for clarity
        p_s2_s1a = [p_s2_s1a[s1][iuser] for s1 in range(self.nstate)]
        p_a_s1 = [p_a_s1[s1][iuser] for s1 in range(self.nstate)]
        p_s2_s1 = p_s2_s1[iuser]
       
        # compute the number of occurences
        self._get_occurences_user(iuser, p_s2_s1a)

        # occurences -> probabilities
        for s1 in range(self.nstate):
            noccurence = np.sum(p_s2_s1a[s1], axis=-1)   # for each action
            p_a_s1[s1] = noccurence / np.sum(noccurence)
            p_a_s1[s1][np.isnan(p_a_s1[s1])] = 0
            p_s2_s1a[s1] /= noccurence[:, None]
            p_s2_s1a[s1][np.isnan(p_s2_s1a[s1])] = 0
            p_s2_s1[s1] = np.sum(p_s2_s1a[s1] * p_a_s1[s1][:, None], axis=0)

    def get_reward_samples(self, coef):
        """
        reward_samples = mdp.get_reward_samples(coef)

        Returns
        -------
        reward_samples : (nstate, coef * state**2) float ndarray
            Sampling of the reward space.

        """
        nsample = int(coef * self.nstate ** 2)
        return np.random.dirichlet(
            np.ones(self.nstate), size=nsample).T

    def get_utility(self, reward, p_s2_s1, gamma=0.9):
        """
        utility = mdp.get_utility(reward, p_s2_s1, gamma)

        Returns
        -------
        utility : (nuser, nstate, nsample) float ndarray
            The utility U associated to the specified reward.

        """
        mat = np.eye(self.nstate, self.nstate)[None, ...] - gamma * p_s2_s1
        return np.linalg.solve(mat, reward)

    def get_utility_action(self, utility, p_s2_s1a):
        """
        utility_action = mdp.get_utility_action(utility, p_s2_s1a)

        Returns
        -------
        utility_action : list of nstate (nuser, naction[state]) float ndarrays
            The utility of the actions.

        """
        out = []
        for istate in range(self.nstate):
            out.append(np.sum(utility[:, None, :] * p_s2_s1a[istate], axis=2))
        return out
        
    def get_reward_softmax(self, reward_samples, utility_samples, T=10):
        """
        reward = mdp.get_reward_softmax(reward_samples, utility_samples, T=10):

        Returns
        -------
        reward : (nuser, nstate) float ndarray
            Softmax estimation of each state reward.

        """
        reward = np.empty((self.nuser, self.nstate))
        for iuser in range(self.nuser): 
            states = self.processes[iuser].states
            if len(states) < self.nstate:
                states = np.pad(
                    states, (0, self.nstate - len(states)), mode='wrap')
            expr = np.exp(T * utility_samples[iuser]) # (nstate, nsample)
            p_G_H = np.sum(expr[states, :], axis=0) / np.sum(expr, axis=0)
            reward[iuser] = np.dot(reward_samples, p_G_H) / np.sum(p_G_H)
        return reward


class MDPProcess(namedtuple('MDPProcessNamedTuple', ['states', 'actions'])):
    __slots__ = ()
    def __iter__(self):
        states = iter(self.states)
        actions = iter(self.actions)
        try:
            s1 = next(states)
        except StopIteration:
            return
        for a, s2 in zip(actions, states):
            yield s1, a, s2
            s1 = s2

    def __getnewargs__(self):
        return self.states, self.actions


class MDPTree(OrientedTree):
    """
    An oriented tree to store an MDP in each node.

    """
    def __setitem__(self, key, value):
        """
        We make sure that only MDPs can be used as node and that the node
        key is equal to the MDP name.

        """
        if not isinstance(value, MDPTree):
            if not isinstance(value, MDP):
                raise TypeError('The node is not an MDP.')
            if key != value.name:
                raise ValueError(
                    'The MDP name is different from the node name.')
        OrientedTree.__setitem__(self, key, value)
