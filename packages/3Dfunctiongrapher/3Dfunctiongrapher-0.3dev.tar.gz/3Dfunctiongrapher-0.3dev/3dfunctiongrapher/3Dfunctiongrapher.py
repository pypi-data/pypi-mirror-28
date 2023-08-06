__author__ = "robert_tarvid"

'''
This program will take the inputs of the user to create a three-dimensional graph of a three variabled function (x, y, z). 
The user will be able to decide on the boundaries and scales of the function on all three axes and will be able to enter the function they would like to be displayed within those boundaries.
If the user enters inputs that will create an invalid window and/or scales, the function will raise an error and will ask the user to input the window again.
'''

# Import needed modules
import tkinter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import ticker
import numpy as np
import webbrowser
import subprocess as sub


def window_process(raw_input):
    '''
    Takes the variables and converts them to floats, will raise an error if non-numerical values are entered

    :param raw_input: Raw input from tkinter.Entry() boxes
    :type raw_input: :str:
    '''
    try:
        value = float(raw_input)
    except ValueError:
        display.insert(tkinter.END, "\nValueError: {} contains non-numerical characters".format(value))
        raise ValueError("{} contains non-numerical characters".format(value))
		
    return value


def funcprocess(function):
    '''
    Checks the raw function string for malicious code

    :param function: Raw function input from tkinter.Text() box
    :type function: :str:
    '''
    malicious = [':', '_', 'subprocess', 'pickle', 'with', 'open', 'yaml', 'sql']
    function.lower()
    for d in malicious:
        if d in function:
            display.insert(tkinter.END, "ZeroDivisionError: You have attempted to inject malicious code into the application.")
            raise ZeroDivisionError("You have attempted to inject malicious code into the application.")
        else:
            continue   

    return function


x = None
y = None
z = None
def grapher(func, graphtype, xmin, xmax, xscale, ymin, ymax, yscale, zmin, zmax, zscale):
    '''
    Uses the processed variables to graph the function

    :param func: Processed function string
    :type func: :str:
    :param graphtype: Graphtype value from tkinter.Radiobutton()
    :type graphtype: :int:
    :param xmin: X-axis minimum
    :type xmin: :float:
    :param xmax: X-axis maximum
    :type xmax: :float:
    :param xscale: X-axis step
    :type xscale: :float:
    :param ymin: Y-axis minimum
    :type ymin: :float:
    :param ymax: Y-axis maximum
    :type ymax: :float:
    :param yscale: Y-axis step
    :type yscale: :float:
    :param zmin: Z-axis minimum
    :type zmin: :float:
    :param zmax: Z-axis maximum
    :type zmax: :float:
    :param zscale: Z-axis step
    :type zscale: :float:
    '''
    # Set up plot, get global variables
    global x
    global y
    global z
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Check if values are acceptable
    # Verify that the window will create a graphable graph, raise ValueError otherwise
    if (xmin >= xmax or xmax - xmin < xscale) or (ymin >= ymax or ymax - ymin < yscale) or (zmin >= zmax or zmax - zmin < zscale):
        display.insert(tkinter.END, "\n ValueError: The inputted window is invalid, please check that all mins are smaller than maxs and scales are smaller than max - min")
        raise ValueError("The inputted window is invalid, please check that all mins are smaller than maxs and scales are smaller than max - min")
    # Select mode
    relationlist = ['x =', 'x=', 'y =', 'y=', 'z =', 'z=']
    if any(rel in func for rel in relationlist[0:2]) and not any(rel in func for rel in relationlist[2:]): # x =
        display.insert(tkinter.END, '\nmode1')
        print('mode1')
        y = np.arange(ymin, ymax, yscale)
        z = np.arange(zmin, zmax, zscale)
        y, z = np.meshgrid(y, z)
        exec("global x;" + func)
    elif any(rel in func for rel in relationlist[2:4]) and not any(rel in func for rel in (relationlist[0:2] + relationlist[4:6])): # y =
        display.insert(tkinter.END, '\nmode2')
        print('mode2')
        x = np.arange(xmin, xmax, xscale)
        z = np.arange(zmin, zmax, zscale)
        x, z = np.meshgrid(x, z)
        exec("global y;" + func)
    elif any(rel in func for rel in relationlist[4:]) and not any(rel in func for rel in relationlist[0:4]): # z =
        display.insert(tkinter.END, '\nmode3')
        print('mode3')
        x = np.arange(xmin, xmax, xscale)
        y = np.arange(ymin, ymax, yscale)
        x, y = np.meshgrid(x, y)
        exec("global z;" + func)
    elif not any(rel in func for rel in relationlist[0:2]): # y = , z =
        display.insert(tkinter.END, '\nmode4')
        print('mode4')
        x = np.arange(xmin, xmax, xscale)
        x = np.meshgrid(x)
        exec("global y; global z;" + func)
    elif not any(rel in func for rel in relationlist[2:4]): # x = , z =
        display.insert(tkinter.END, '\nmode5')
        print('mode5')
        y = np.arange(ymin, ymax, yscale)
        y = np.meshgrid(y)
        exec("global x; global z;" + func)
    elif not any(rel in func for rel in relationlist[4:6]): # x = , y =
        display.insert(tkinter.END, '\nmode6')
        print('mode6')
        z = np.arange(zmin, zmax, zscale)
        z = np.meshgrid(z)
        exec("global x; global y;" + func)
    else:
        display.insert(tkinter.END, "\nValueError: Please input a valid equation.")
        raise ValueError("Please input a valid equation.")
    # Plot the surface/wireframe
    if graphtype == 1:
        display.insert(tkinter.END, '\nsurface')
        ax.plot_surface(x, y, z, rstride=int(np.ceil(xscale/2)), cstride=int(np.ceil(yscale/2)), cmap=cm.gnuplot2, vmin=(zmin-2*zscale), vmax=(zmax+2*zscale), linewidth=0, antialiased=False)
    elif graphtype == 2:
        display.insert(tkinter.END, '\nwire')
        ax.plot_wireframe(x, y, z, rstride=int(np.ceil(xscale)), cstride=int(np.ceil(yscale)))
    else:
        display.insert(tkinter.END, "ValueError: Please select a valid graph type.")
        raise ValueError("Please select a valid graph type.")
    # Make window
    ax.set_xlim(xmin, xmax)
    ax.xaxis.set_major_locator(ticker.LinearLocator((xmax - xmin) / xscale + 1))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.02f'))
    
    ax.set_ylim(ymin, ymax)
    ax.yaxis.set_major_locator(ticker.LinearLocator((ymax - ymin) / yscale + 1))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.02f'))

    ax.set_zlim(zmin, zmax)
    ax.zaxis.set_major_locator(ticker.LinearLocator((zmax - zmin) / zscale + 1))
    ax.zaxis.set_major_formatter(ticker.FormatStrFormatter('%.02f'))

    plt.show()


def main():
    '''Uses window_process(), funcprocess(), and grapher() to take the inputs and use the grapher to graph the inputted function in the specified window'''
    success = False
    # Get vars
    try:
        func = funcprocess(equationbox.get('1.0', tkinter.END))
        xmin = window_process(xmin1.get())
        xmax = window_process(xmax1.get())
        xscale = window_process(xscale1.get())
        ymin = window_process(ymin1.get())
        ymax = window_process(ymax1.get())
        yscale = window_process(yscale1.get())
        zmin = window_process(zmin1.get())
        zmax = window_process(zmax1.get())
        zscale = window_process(zscale1.get())
        graphtype = checkvalue.get()

        success = True
    except ValueError as e:
        print(e)

    if success:
        display.insert(tkinter.END, '\n' + func)
        print(func, graphtype, xmin, xmax, xscale, ymin, ymax, yscale, zmin, zmax, zscale)
        grapher(func, graphtype, xmin, xmax, xscale, ymin, ymax, yscale, zmin, zmax, zscale)
        print(x)
        print(y)
        print(z)
        display.insert(tkinter.END, '\n' + str(x))
        display.insert(tkinter.END, '\n' + str(y))
        display.insert(tkinter.END, '\n' + str(z))

savenumber = 0

def savegraph():
    '''Saves the graph as an image, savenumber is used as global var to allow increment after each save'''
    global savenumber
    plt.savefig(r"C:\Users\Public\Desktop\graph{}.png".format(savenumber))
    savenumber += 1


def quitfunc():
    '''Closes Tk window'''
    global root
    root.destroy()


def github_open():
    '''Opens new tab in browser and directs user to GitHub repository'''
    webbrowser.open('https://github.com/rtarvids/3D-Function-Grapher', new=2)


if __name__ == "__main__":
    # Creating and setting up main window
    root = tkinter.Tk()

    root.title('3D Function Grapher By Robert Tarvid')
    root.geometry('1760x990')

    # Creating interpreter display
    display = tkinter.Text(root, relief='raised', borderwidth=1)
    display.grid(row=0, column=0, sticky='nsew', rowspan='14')
    # Interpreter messages are directed to display from within the functions using .insert()

    # Configuring columns for the interface
    root.columnconfigure(0, weight=12)
    root.columnconfigure(1, weight=2)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    root.columnconfigure(4, weight=2)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=2)
    root.rowconfigure(2, weight=7)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=1)
    root.rowconfigure(5, weight=1)
    root.rowconfigure(6, weight=1)
    root.rowconfigure(7, weight=1)
    root.rowconfigure(8, weight=1)
    root.rowconfigure(9, weight=1)
    root.rowconfigure(10, weight=1)
    root.rowconfigure(11, weight=1)
    root.rowconfigure(12, weight=4)
    root.rowconfigure(13, weight=4)

    # Creating textbox and info
    equationtitle = tkinter.Label(root, text='Equation:')
    equationtitle.grid(row=0, column=1, sticky='w')
    equationbox = tkinter.Text(root)
    equationbox.grid(row=1, column=1, columnspan=4, sticky='nsew')
    info1 = tkinter.Label(root, anchor='w', text='+ -> addition\n - -> subtraction\n * -> multiplication\n / -> division\n ** -> exponentiation')
    info1.grid(row=2, column=1, sticky='w', padx=30)
    info2 = tkinter.Label(root, anchor='w', text='np.log(x) -> logarithm\n % -> modulo\n np.(trigfunction)(x) -> see below\n np.fabs(x) -> absolute value')
    info2.grid(row=2, column=2, columnspan=2, sticky='w', padx=30)
    info3 = tkinter.Label(root, anchor='w', text='np.cumprod(x) -> factorial\n np.ceil(x) -> ceiling\n np.floor(x) -> floor')
    info3.grid(row=2, column=4, sticky='w', padx=30)
    info4 = tkinter.Label(root, anchor='w', text='For roots, please use fractional exponents. For two input logarithms, use the base change rule. \n For frac, use (n - int(n))\n Available trig functions are: sin(x), cos(x), tan(x), arcsin(x), arccos(x), arctan(x).\n To get their hyperbolic variants, just add an h to the function name.\n Please use reciprocal and quotient identities for the rest.')
    info4.grid(row=3, column=1, columnspan=4, sticky='w', padx=30)

    # Creating settings area
    preferences = tkinter.Label(root, text='Settings')
    preferences.grid(row=4, column=1, sticky='w', padx=30)

    # Window settings
    windowset = tkinter.Label(root, text='Window')
    windowset.grid(row=5, column=1, sticky='w', padx=30)
    tx = tkinter.Label(root, text='X')
    ty = tkinter.Label(root, text='Y')
    tz = tkinter.Label(root, text='Z')
    tx.grid(row=6, column=1, sticky='w', padx=30)
    ty.grid(row=6, column=2, columnspan=2, sticky='w', padx=30)
    tz.grid(row=6, column=4, sticky='w', padx=30)

    xmin1 = tkinter.Entry(root)
    xmin1.grid(row=7, column=1, sticky='e', padx=40)
    xmin2 = tkinter.Label(root, text='min:')
    xmin2.grid(row=7, column=1, sticky='w', padx=30)
    xmax1 = tkinter.Entry(root)
    xmax1.grid(row=8, column=1, sticky='e', padx=40)
    xmax2 = tkinter.Label(root, text='max:')
    xmax2.grid(row=8, column=1, sticky='w', padx=30)
    xscale1 = tkinter.Entry(root)
    xscale1.grid(row=9, column=1, sticky='e', padx=40)
    xscale2 = tkinter.Label(root, text='scale:')
    xscale2.grid(row=9, column=1, sticky='w', padx=30)

    ymin1 = tkinter.Entry(root)
    ymin1.grid(row=7, column=2, sticky='e', columnspan=2, padx=40)
    ymin2 = tkinter.Label(root, text='min:')
    ymin2.grid(row=7, column=2, sticky='w', columnspan=2, padx=30)
    ymax1 = tkinter.Entry(root)
    ymax1.grid(row=8, column=2, sticky='e', columnspan=2, padx=40)
    ymax2 = tkinter.Label(root, text='max:')
    ymax2.grid(row=8, column=2, sticky='w', columnspan=2, padx=30)
    yscale1 = tkinter.Entry(root)
    yscale1.grid(row=9, column=2, sticky='e', columnspan=2, padx=40)
    yscale2 = tkinter.Label(root, text='scale:')
    yscale2.grid(row=9, column=2, sticky='w', columnspan=2, padx=30)

    zmin1 = tkinter.Entry(root)
    zmin1.grid(row=7, column=4, sticky='e', padx=40)
    zmin2 = tkinter.Label(root, text='min:')
    zmin2.grid(row=7, column=4, sticky='w', padx=30)
    zmax1 = tkinter.Entry(root)
    zmax1.grid(row=8, column=4, sticky='e', padx=40)
    zmax2 = tkinter.Label(root, text='max:')
    zmax2.grid(row=8, column=4, sticky='w', padx=30)
    zscale1 = tkinter.Entry(root)
    zscale1.grid(row=9, column=4, sticky='e', padx=40)
    zscale2 = tkinter.Label(root, text='scale:')
    zscale2.grid(row=9, column=4, sticky='w', padx=30)

    # Graph type settings
    graphtype1 = tkinter.Label(root, text='Graph Type')
    graphtype1.grid(row=10, column=1, sticky='w', padx=30)

    checkvalue = tkinter.IntVar()
    checkvalue.set(1)
    check1 = tkinter.Radiobutton(root, text='Surface Plot', value=1, variable=checkvalue)
    check2 = tkinter.Radiobutton(root, text='Wireframe', value=2, variable=checkvalue)
    check1.grid(row=11, column=1, columnspan=2)
    check2.grid(row=11, column=3, columnspan=2)

    # Four buttons
    graphbutton = tkinter.Button(root, text='Graph Equation', command=main)
    graphbutton.grid(row=12, column=1, columnspan=2, sticky='nsew')
    saver = tkinter.Button(root, text='Save Plot To Desktop', command=savegraph)
    saver.grid(row=12, column=3, columnspan=2, sticky='nsew')
    document = tkinter.Button(root, text='Quit The Program', command=quitfunc)
    document.grid(row=13, column=3, columnspan=2, sticky='nsew')
    github = tkinter.Button(root, text='GitHub', command=github_open)
    github.grid(row=13, column=1, columnspan=2, sticky='nsew')

    root.mainloop()
