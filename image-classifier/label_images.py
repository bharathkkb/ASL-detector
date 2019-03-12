import cv2

def process_and_label(list_images):
    #Returns two arrays
    #X is array data of the passed in list_images
    #Y is an array of labels

    X = [] #Images
    y = [] # labels

    for image in list_images:
        X.append(cv2.imread(image, cv2.IMREAD_COLOR))
        #Retrieve Labels
        if 'A' in image:
            y.append('A')
        elif 'B' in image:
            y.append('B')
        elif 'C' in image:
            y.append('C')
        elif 'D' in image:
            y.append('D')
        elif 'E' in image:
            y.append('E')
        elif 'F' in image:
            y.append('F')
        elif 'G' in image:
            y.append('G')
        elif 'H' in image:
            y.append('H')
        elif 'I' in image:
            y.append('I')
        elif 'J' in image:
            y.append('J')
        elif 'K' in image:
            y.append('K')
        elif 'L' in image:
            y.append('L')
        elif 'M' in image:
            y.append('M')
        elif 'N' in image:
            y.append('N')
        elif 'O' in image:
            y.append('O')
        elif 'P' in image:
            y.append('P')
        elif 'Q' in image:
            y.append('Q')
        elif 'R' in image:
            y.append('R')
        elif 'S' in image:
            y.append('S')
        elif 'T' in image:
            y.append('T')
        elif 'U' in image:
            y.append('U')
        elif 'V' in image:
            y.append('V')
        elif 'W' in image:
            y.append('W')
        elif 'X' in image:
            y.append('X')
        elif 'Y' in image:
            y.append('Y')
        elif 'Z' in image:
            y.append('Z')
        elif 'del' in image:
            y.append('del')
        elif 'nothing' in image:
            y.append('nothing')
        elif 'space' in image:
            y.append('space')
    
    return X, y