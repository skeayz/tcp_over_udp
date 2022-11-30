import matplotlib.pyplot as plt
import datetime

if __name__ == "__main__":
    #Plot the graph from time_window.txt
    with open('time_window.txt', 'r') as f:
        time_window = f.readlines()
        time_window = [tuple(map(float, x.split())) for x in time_window]
        x = [t[0] for t in time_window]
        y = [t[1] for t in time_window]
        #plot only points
        #keep only even points
        x = x[::4]
        y = y[::4]
        
        plt.plot(x, y, linewidth=0.5)
        plt.xlabel('Time (s)')
        plt.ylabel('Window size')
        plt.title('Window size over time')
        plt.show()
        