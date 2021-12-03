import settings as settings
import graphics as graph


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

def main():    
    window = graph.GraphWin(
        settings.WINDOW["title"], 
        settings.WINDOW["width"], 
        settings.WINDOW["height"]
        )
    draw_main_optical_axes(window)
    draw_lens(window, "blue", 3)
    draw_object(window, 0.3, 0.5, "red", 5)
    draw_object_image(window, 0.6, 0.5, "orange", 5)

    window.getMouse()
    window.close()

main()