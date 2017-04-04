import zmq
import msgpack
from struct import unpack_from
import os
import csv
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("pebble_id", type=int)
parser.add_argument("recv_port", type=str)
args = parser.parse_args()

context = zmq.Context()
# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://127.0.0.1:5000")



file_path = os.environ.get('PEBBLE_DATA_LOC')
if file_path is None:
    print("DID NOT FIND PEBBLE_DATA_LOC")
    print(os.environ)
    exit(1)

if not os.path.exists(file_path):
    os.mkdir(file_path)


newFile = True
iterFile = 0

while True:
    try:
        data = msgpack.unpackb(receiver.recv())
        packet_count = int(len(data)/208)
        print("got {} packets".format(packet_count))
        if iterFile>=(50*60*60): newFile = True
    
        if (packet_count>0 & packet_count<10):
            timestamp = unpack_from('Q',data,208*0)
            if newFile==True:
                filename = str(file_path) + "pebble_data_"+ str(timestamp[0]) + ".csv"
                print("file name: {}".format(filename))
                newFile = False
                iterFile = 0
                try:
                    with open(filename,'w') as datafile:
                        datafile.write("z,y,x,offset,timestamp\n")
                        print("Opened file: {}".format(filename))
                    datafile.close()
                except:
                    print("Error opening new file!")
                    datafile.close()					
            for k in range(packet_count):
                timestamp = unpack_from('Q',data,208*k)
                acc_data = []
                for i in range(25):
                    acc_data.append(unpack_from('hhhH',data,(208*k)+(i+1)*8))
                print("timestamp:{}".format(timestamp[0]))
                print("data:{}".format(acc_data))
                for data_t in acc_data:
                    iterFile = iterFile + 1
                    try:
                        with open(filename,'a') as datafile1:
                            datafile1.write("{0},{1},{2},{3},{4}\n".format(data_t[0],data_t[1],data_t[2],data_t[3],timestamp[0]))
                        datafile1.close()
                    except:
                        datafile1.close()
                        print("Error in writing data!")
                        exit(1)
            #datafile.close()
        else:
            print("Size Error!")

    except:
        print("Error!")
