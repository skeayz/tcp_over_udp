if __name__ == '__main__':
    file = open("big.txt", 'w')
    for i in range (0, 10000000):
        file.write("abcdefghijklmnopqrstuvwxyz\n")
    file.close()
    