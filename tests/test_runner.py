from cmd2func.runner import ProcessRunner


def test_process_runner():
    runner = ProcessRunner("python -c '1+1'")
    runner.run()
    out = list(runner.stream())
    assert len(out) == 0
    runner = ProcessRunner("python -c 'print(1)'")
    runner.run(capture_stdout=False)  # Don't capture stdout
    out = list(runner.stream())
    assert len(out) == 0


def test_runner_shell():
    runner = ProcessRunner("python -c 'print(1)'")
    runner.run(shell=True)
    out = list(runner.stream())
    assert len(out) == 1
