import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent import run_agent, get_user_memory


def test_cross_user_isolation():

    run_agent("user_a", "Private message from user A")
    run_agent("user_b", "Private message from user B")

    user_a_memory = get_user_memory("user_a")
    user_b_memory = get_user_memory("user_b")

    assert "Private message from user A" in user_a_memory
    assert "Private message from user B" in user_b_memory

    assert "Private message from user B" not in user_a_memory
    assert "Private message from user A" not in user_b_memory