from mookfist_lled_controller.colors import color_from_hls, color_from_rgb, color_from_html

def test_colors():

    redhls = color_from_hls(0,0.5,100)
    redrgb = color_from_rgb(255,0,0)
    redhtml = color_from_html('ff0000')

    assert redhls == redrgb == redhtml

