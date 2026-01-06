import statistics


def detect_flakiness(results, execution_times):
    """
    Detects test flakiness based on:
    - Failure ratio
    - Execution time variance

    Args:
        results (list[str]): List of "PASS" / "FAIL"
        execution_times (list[float]): Execution times per run

    Returns:
        tuple:
            is_flaky (bool)
            failure_ratio (float)
            time_variance (float)
    """

    if not results or not execution_times:
        raise ValueError("Results and execution times cannot be empty")

    total_runs = len(results)
    failures = results.count("FAIL")

    # 🔹 Failure ratio (simple ML heuristic)
    failure_ratio = failures / total_runs

    # 🔹 Variance in execution time
    if len(execution_times) > 1:
        time_variance = statistics.variance(execution_times)
    else:
        time_variance = 0.0

    # 🔹 Heuristic-based ML decision
    # (In real ML, this would be a trained model)
    is_flaky = False

    if failure_ratio >= 0.3:
        is_flaky = True

    if time_variance > 0.05:
        is_flaky = True

    return is_flaky, round(failure_ratio, 2), round(time_variance, 4)
