from tf2internal.shared.mathutil import Vec3, angle_to, clamp


def test_vec3_sub_and_length():
    a = Vec3(3, 4, 0)
    b = Vec3(0, 0, 0)
    assert (a - b).length() == 5.0


def test_angle_to_axis():
    assert abs(angle_to(Vec3(0, 0, 0), Vec3(1, 0, 0))) < 1e-6
    assert abs(angle_to(Vec3(0, 0, 0), Vec3(0, 1, 0)) - 90.0) < 1e-6


def test_clamp():
    assert clamp(400) == 180
    assert clamp(-400) == -180
    assert clamp(90) == 90