import glob
import os
import numpy as np 
import csv
import cv2
import argparse

parser = argparse.ArgumentParser(description="", add_help='How to use', prog='python creating_numpy.py <options>')

parser.add_argument("-if", "--inputfile", default="../data/tarin.csv",
                    help='Path to the CSV file [DEFAULT: "data/tarin.csv"]')

parser.add_argument("-o", "--outputdir", default="../data/tarin_np/",
                    help='Path to save the files to[DEFAULT: "data/tarin_np/"]')

parser.add_argument("-in", "--inputdir", default="../data/tarin/",
                    help='Path to actual images[DEFAULT: "data/tarin/"]')

parser.add_argument("-s", "--skip", default="10000",
                    help='number of records per file')

parser.add_argument("-sz", "--size", default="64",
                    help='size of the prodused Images ( default = 64 )')


args = parser.parse_args()

train_path = args.inputdir
output_path = args.outputdir

# get a list of all files
a=glob.glob( os.path.join(train_path, '*.jpg'))
X_train=[]
y_train=[]
counter=0
csv_file=csv.reader(open(args.inputfile ),delimiter=',')
csv_file_1=dict((rows[0],rows[2])for rows in csv_file)
csv_file=csv_file_1

counter=0

records_per_file = int( args.skip )
image_size = ( int( args.size ) ,int( args.size )  )
for i in range (0,len(a)):
    
    if(i%100000==0 and i > 0):
        print("current=",i)
    try:

        temp_x=cv2.imread((train_path+str(a[i].replace(train_path,'').strip())),1)

        try:
            y_train.append(csv_file[str(a[i].replace(train_path,'').replace('.jpg',''))])
            X_train.append(cv2.resize(temp_x,image_size))

        except:

            print("cant find entry, skipping!")
        
        if i % records_per_file == 0 and i > 0:
            np.save(output_path+ '/X_train'+ str(counter)+'.npy',np.array(X_train))
            np.save(output_path+'/y_train'+ str(counter)+'.npy',np.array(y_train))
            counter += 1
            X_train = []
            y_train = []

    except:
        raise
        print('error', i)


# save the last section
if len(X_train) > 0:
    np.save(output_path + '/X_train' + str(counter) + '.npy', np.array(X_train))
    np.save(output_path + '/y_train' + str(counter) + '.npy', np.array(y_train))



