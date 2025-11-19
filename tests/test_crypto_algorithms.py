import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path, find_callable

CRYPTO_ALGOS = {
    "sha256": [
        "semester_04",
        "lecture_18_crypto_algorithms",
        "sha256",
        "algorithm.py",
    ],
    "rsa": [
        "semester_04",
        "lecture_18_crypto_algorithms",
        "rsa",
        "algorithm.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", CRYPTO_ALGOS.items())
def test_crypto_algorithms(algo_name, path_parts):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)
    if algo_name == "sha256":
        fn = find_callable(
            module, ["sha256_hex", "sha256"]
        )  # prefer hex for comparison
        if fn is None:
            pytest.skip("sha256 function not found")
        # Known test vector for 'abc'
        if fn.__name__ == "sha256_hex":
            assert fn(b"abc") == (
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
            )
        else:
            res = fn(b"abc")
            if isinstance(res, bytes):
                assert res.hex() == (
                    "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
                )
            else:
                pytest.skip("Unsupported return type for sha256")
    elif algo_name == "rsa":
        # Minimal: ensure helper functions exist or smoke import
        has_is_prime = getattr(module, "is_prime", None)
        if callable(has_is_prime):
            assert has_is_prime(2) is True
            assert has_is_prime(1) is False
        else:
            pytest.skip("RSA primitives not exposed; skipping functional check")
