from pylab import *
class MouseMonitor:
    event = None
    xdatalist = []
    ydatalist = []

    def mycall(self, event):
        self.event = event
        self.xdatalist.append(event.xdata)
        self.ydatalist.append(event.ydata)
        
        print 'x = %s and y = %s' % (event.xdata,event.ydata)
        
        ax = gca()  # get current axis
        ax.hold(True) # overlay plots.
        
        # Plot a red circle where you clicked.
        ax.plot([event.xdata],[event.ydata],'ro')
        
        draw()  # to refresh the plot.
        
if __name__=="__main__":
    # Example usage
    mouse = MouseMonitor()
    connect('button_press_event', mouse.mycall)
    plot([1,2,3])
    show()
