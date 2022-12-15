import matplotlib.pyplot as plt
import datetime

if __name__ == "__main__":
    #Plot the graph from time_window.txt
    with open('time_window.txt', 'r') as f:
        rawFile = f.readlines()
        # time_window = [tuple(map(float, x.split())) for x in time_window]
        time_window = []
        for a in rawFile:
            a = a.split()
            a[0] = a[0].split(':')
            a = (float(a[0][2]), a[1])
            time_window.append(a)
        
        # print(time_window)
        x = [t[0] for t in time_window]
        y = [t[1] for t in time_window]
        #plot only points
        #plot only beetween 0 and 1
        #keep only even points
        x = x[::]
        y = y[::]
        
        plt.plot(x, y, linewidth=1, marker='o', markersize=1)
        # plt.xlim(0, 0.2)
        plt.xlabel('Time (s)')
        plt.ylabel('Window size')
        plt.title('Window size over time')
        plt.show()
        