import pytest
import os
from utils import *


def test_clean_the_list_of_branches():
    sample = ['  admin_lte_theme', '  deploy', '  master', '  projectmodel', '* update_flow', '']
    expected_result = ['admin_lte_theme', ' deploy', 'master', 'projectmodel', '*update_flow']

    assert clean_the_list_of_branches(sample) == expected_result

def test_removing_all_branch_except_the_current():
    sample = ['admin_lte_theme', ' deploy', 'master', 'projectmodel', '*update_flow']
    expected_result = ['admin_lte_theme', ' deploy', 'master', 'projectmodel']

    assert get_list_of_branch(sample) == expected_result
