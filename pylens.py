from ast import Str
import settings as settings

import graphics as graph
from PIL import ImageGrab
import math as math

 
def save(widget, file_name):
    # https://www.cyberforum.ru/python-graphics/thread2528952.html
    root = widget.master
    x = root.winfo_rootx()+widget.winfo_x()
    y = root.winfo_rooty()+widget.winfo_y()
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save(file_name)

def draw_main_optical_axes(window, color="black", width=1):
    """Draw main optical axes"""
    main_optical_axes = graph.Line(
        graph.Point(0, window.getHeight() // 2),
        graph.Point(window.getWidth(), window.getHeight() // 2)
        )
    main_optical_axes.setOutline(color=color)
    main_optical_axes.setWidth(width)
    main_optical_axes.draw(window)
    return main_optical_axes

def draw_main_optical_axes_scale(window, phys_width, dashes, font_size, dash_size, color="black", width=1):
    """Draw scale for main optical axes"""
    for x in range(0,window.getWidth(), window.getWidth() // dashes):
        dash = graph.Line(graph.Point(x, window.getHeight() // 2 - dash_size // 2),
        graph.Point(x, window.getHeight() // 2 + dash_size // 2))
        dash.setOutline(color=color)
        dash.setWidth(width)
        dash.draw(window)
        text_scale = 1.1
        text = graph.Text(
            graph.Point(x, window.getHeight() // 2 + dash_size*text_scale // 2),
            (f"{round(phys_width*x/window.getWidth() - phys_width/2, 1)}")
        )
        text.setOutline(color=color)
        text.setSize(font_size)
        text.draw(window)
    return None

def draw_lens_scale(window, phys_height, dashes, font_size, dash_size, color="black", width=1):
    """Draw scale for main optical axes"""
    for y in range(0,window.getHeight(), window.getHeight() // dashes):
        dash = graph.Line(graph.Point(window.getWidth() // 2 - dash_size // 2, y),
        graph.Point(window.getWidth() // 2 + dash_size // 2, y))
        dash.setOutline(color=color)
        dash.setWidth(width)
        dash.draw(window)
        text_scale = 1.1
        text = graph.Text(
            graph.Point(window.getWidth() // 2 + dash_size*text_scale // 2, y),
            (f"{round(phys_height*y/window.getHeight() - phys_height/2, 1)}")
        )
        text.setOutline(color=color)
        text.setSize(font_size)
        text.draw(window)
    return None

def draw_lens(window, color="black", width=1,  k=0.9):
    """Draw lens
    
    k - height (a fraction of half the height of the window)

    """    
    lens = graph.Line(
        graph.Point(window.getWidth() // 2, ((1-k)/2)*window.getHeight()),
        graph.Point(window.getWidth() // 2, (1 - (1-k)/2)*window.getHeight())
        )
    lens.setOutline(color=color)
    lens.setWidth(width)
    lens.draw(window)
    return lens

def draw_object(window, h, d, color="black", width=1):
    """Draw object
    
    h - height (a fraction of half the height of the window)
    d - distance (distance from the object to the lens)
    
    """
    obj = graph.Line(
        graph.Point((1-d)*(window.getWidth() // 2), window.getHeight() // 2),
        graph.Point((1-d)*(window.getWidth() // 2), (1-h)*(window.getHeight() // 2))
        )
    obj.setOutline(color=color)
    obj.setWidth(width)
    obj.draw(window)
    return obj

def draw_object_image(window, H, f, color="black", width=1):
    """Draw image of object
    
    H - height (a fraction of half the height of the window)
    f - distance (distance from the lens to the image of object)
    
    """
    obj = graph.Line(
        graph.Point((1+f)*(window.getWidth() // 2), window.getHeight() // 2),
        graph.Point((1+f)*(window.getWidth() // 2), (1+H)*(window.getHeight() // 2))
        )
    obj.setOutline(color=color)
    obj.setWidth(width)
    obj.draw(window)
    return obj

def thin_lens(ret, **kwargs):
    F = kwargs.get("F")
    D = kwargs.get("D")
    f = kwargs.get("f")
    d = kwargs.get("d")
    h = kwargs.get("h")
    H = kwargs.get("H")
    k = kwargs.get("k")

    if (ret=="F") & (D!=None):
        return 1/D
    if (ret=="D") & (F!=None):
        return 1/F

    if (D!=None):
        F = 1/D
    if (F!=None):
        D = 1/F

    if (ret=="f") & (d!=None):
        return 1/(D - 1/d)
    if (ret=="d") & (f!=None):
        return 1/(D - 1/f)
    
    if (d!=None) & (D!=None):
        f = 1/(D - 1/d)
    if (f!=None) & (D!=None):
        d = 1/(D - 1/f)
    
    if (ret=="k") & (d!=None) & (f!=None):
        return f/d
    if (ret=="k") & (H!=None) & (h!=None):
        return H/h
    
    if (d!=None) & (f!=None):
        k = f/d
    if (H!=None) & (h!=None):
        k = H/h
    
    if (ret=="H") & (k!=None) & (h!=None):
        return h*k
    if (ret=="h") & (k!=None) & (H!=None):
        return H/k

def get_r_phi(p1, p2):
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    r = ((x2-x1)**2 + (y2-y1)**2)**(0.5)
    if (x1-x2)!=0:
        phi = math.atan((y2-y1)/(x2-x1))
    else:
        if y1>y2:
            phi = -math.pi/4
        else:
            phi = +math.pi/4
    return (r, phi)

def get_point(p0, r, phi):
    x0 = p0.x
    y0 = p0.y
    x = x0 + r*math.cos(phi)
    y = y0 + r*math.sin(phi)
    return graph.Point(x,y)

def draw_ray0(window, from_point, color="black", width=1, color_reflection="red", width_reflection=1):
    x1 = from_point.x
    y1 = from_point.y
    x2 = window.getWidth() // 2
    y2 = window.getHeight() // 2

    (r, phi) = get_r_phi(graph.Point(x1,y1), graph.Point(x2,y2))
    r = max(window.getWidth(), window.getHeight())
    to_point = get_point(from_point, r, phi)
    
    ray0 = graph.Line(from_point, to_point)
    ray0.setOutline(color=color)
    ray0.setWidth(width)
    ray0.draw(window)

    phi += math.pi
    to_point = get_point(from_point, r, phi)
    
    ray0_reflection = graph.Line(from_point, to_point)
    ray0_reflection.setOutline(color=color_reflection)
    ray0_reflection.setWidth(width_reflection)
    ray0_reflection.draw(window)
    return (ray0, ray0_reflection)

def draw_ray1(window, from_point, focus_point, color1="black", width1=1, color2="black", width2=1, color_reflection="red", width_reflection=1):
    x1 = from_point.x
    y1 = from_point.y
    x2 = window.getWidth() // 2
    y2 = y1
    fx = focus_point.x
    fy = focus_point.y

    in_lens_point = graph.Point(x2, y2)
    ray1_1 = graph.Line(from_point, in_lens_point)
    ray1_1.setOutline(color=color1)
    ray1_1.setWidth(width1)
    ray1_1.draw(window)

    (r, phi) = get_r_phi(in_lens_point, focus_point)
    r = max(window.getWidth(), window.getHeight())
    to_point = get_point(in_lens_point, r, phi)
    
    ray1_2 = graph.Line(in_lens_point, to_point)
    ray1_2.setOutline(color=color2)
    ray1_2.setWidth(width2)
    ray1_2.draw(window)

    phi += math.pi
    to_point = get_point(in_lens_point, r, phi)
    
    ray1_reflection = graph.Line(in_lens_point, to_point)
    ray1_reflection.setOutline(color=color_reflection)
    ray1_reflection.setWidth(width_reflection)
    ray1_reflection.draw(window)
    
    return (ray1_1, ray1_2, ray1_reflection)

def draw_focus(window, F, color1="green", width1=1, color2="green4", width2=1, radius=5):
    f1x = (1+F)*window.getWidth()//2
    f1y = window.getHeight()//2
    focus1_point = graph.Point(f1x, f1y)

    focus_1 = graph.Circle(focus1_point, radius)
    focus_1.setOutline(color=color1)
    focus_1.setWidth(width1)
    focus_1.draw(window)

    f2x = (1-F)*window.getWidth()//2
    f2y = f1y
    focus2_point = graph.Point(f2x, f2y)

    focus_2 = graph.Circle(focus2_point, radius)
    focus_2.setOutline(color=color2)
    focus_2.setWidth(width2)
    focus_2.draw(window)

    return (focus_1, focus_2)


def main():    
    window = graph.GraphWin(
        settings.WINDOW["title"], 
        settings.WINDOW["width"], 
        settings.WINDOW["height"]
        )

    phys_width = 2.0
    phys_height = 2.0
    scale_phys_height_to_frac = 1 / phys_height
    scale_phys_width_to_frac = 1 / phys_width

    D = 1.5
    F = thin_lens("F", D=D)
    d = 0.2
    f = thin_lens("f", D=D, d=d)
    h = 0.2
    H = thin_lens("H", D=D, f=f, d=d, h=h)

    F *= scale_phys_width_to_frac
    f *= scale_phys_width_to_frac
    d *= scale_phys_width_to_frac
    h *= scale_phys_height_to_frac
    H *= scale_phys_height_to_frac

    print("F=", F)
    print("f=", f)
    print("d=", d)
    print("h=", h)
    print("H=", H)

    # focus_point = graph.Point(F*window.getWidth()//2, window.getHeight() // 2)

    main_optical_axes = draw_main_optical_axes(window)
    draw_main_optical_axes_scale(window, phys_width, 10, 7, window.getHeight() // 30, "green", 1)
    draw_lens_scale(window, phys_height, 10, 7, window.getWidth() // 30, "green", 1)
    lens = draw_lens(window, settings.COLORS["lens"]["converging"], 3)
    obj = draw_object(window, h, d, settings.COLORS["object"]["real"], 5)
    object_image = draw_object_image(window, H, f, settings.COLORS["object"]["imaginary"], 5)
    (ray0, rayo_reflection) = draw_ray0(window, obj.p2, settings.COLORS["rays"]["ray0"], 1, settings.COLORS["rays"]["ray0_reflection"])
    (ray1_1, ray1_2, ray1_reflection) = draw_ray1(window, obj.p2, object_image.p2, settings.COLORS["rays"]["ray1_1"], 1, settings.COLORS["rays"]["ray1_2"], 1, settings.COLORS["rays"]["ray1_reflection"], 1)
    (focus_1, focus_2) = draw_focus(window, F, settings.COLORS["focuses"]["focus_1"], 5, settings.COLORS["focuses"]["focus_2"], 5, 5)
    
    save(window, settings.FILE_NAME)
    window.getMouse()
    window.close()

main()