import unittest
import numpy as np

from jive.ajive_fig2 import *
from jive.Jive import *
from jive.block_visualization import *


class JiveViz(unittest.TestCase):
    """
    Make sure visualization fucntions run

    """
    def setUp(self):
        """
        Sample data and compute JIVE estimates
        """
        # sample platonic data
        seed = 23423
        X_obs, X_joint, X_indiv, X_noise, \
        Y_obs, Y_joint, Y_indiv, Y_noise = generate_data_ajive_fig2(seed)

        blocks = [X_obs, Y_obs]
        jive = Jive(blocks=blocks)
        jive.compute_initial_svd()
        jive.set_signal_ranks([2, 3])
        jive.compute_joint_svd()
        jive.estimate_joint_rank()
        jive.estimate_jive_spaces()

        self.blocks = blocks
        self.full_block_estimates = jive.get_block_full_estimates()

    def test_block_plot(self):
        """
        Make sure plot_data_blocks() runs without error.
        """
        plot_data_blocks(self.blocks)
        self.assertTrue(True)

    def test_jive_plot(self):
        """
        Make sure plot_jive_full_estimates() runs without error.
        """
        plot_jive_full_estimates(self.full_block_estimates, self.blocks)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
