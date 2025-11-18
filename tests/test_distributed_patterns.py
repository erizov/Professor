import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path

DISTRIBUTED_ALGOS = {
    "leader_election": [
        "semester_04",
        "lecture_19_distributed_patterns",
        "leader_election",
        "algorithm.py",
    ],
    "two_phase_commit": [
        "semester_04",
        "lecture_19_distributed_patterns",
        "two_phase_commit",
        "algorithm.py",
    ],
    "gossip_protocol": [
        "semester_04",
        "lecture_19_distributed_patterns",
        "gossip_protocol",
        "algorithm.py",
    ],
    "consistent_hashing": [
        "semester_04",
        "lecture_19_distributed_patterns",
        "consistent_hashing",
        "algorithm.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", DISTRIBUTED_ALGOS.items())
def test_distributed_patterns(algo_name, path_parts):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)

    if algo_name == "leader_election":
        LeaderElection = getattr(module, "LeaderElection", None)
        if LeaderElection is None:
            pytest.skip("LeaderElection class not found")
        le = LeaderElection(["n1", "n2", "n3"])
        le.start_election("n1")
        leader = le.get_leader()
        assert leader in {"n1", "n2", "n3", None}
    elif algo_name == "consistent_hashing":
        fn = getattr(module, "consistent_hashing", None)
        if callable(fn):
            try:
                fn()
            except TypeError:
                pytest.skip("consistent_hashing requires parameters")
        else:
            pytest.skip("consistent_hashing function not found")
    else:
        # Smoke test functions if present
        fn = getattr(module, algo_name, None)
        if callable(fn):
            try:
                fn()
            except TypeError:
                pytest.skip(f"{algo_name} requires parameters")
        else:
            pytest.skip(f"{algo_name} function not found")
