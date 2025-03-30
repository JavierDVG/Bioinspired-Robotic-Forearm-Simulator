from pid_controller import PIDController

def test_pid_response():
    pid = PIDController(1.0, 0.1, 0.05, 0.1)
    output = pid.compute(1.0, 0.5)
    assert isinstance(output, float)
