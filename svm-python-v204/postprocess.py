import os
import csv

def save_label(output_filename, utterance_all):

    # save csv file
    csv_data = []
    for utterance in utterance_all:
        csv_data.append([utterance.name, utterance.phones])
    
    with open(output_filename, 'w+') as file:
        print "Save %s" %output_filename
        writer = csv.writer(file)
        writer.writerow(["id", "phone_sequence"])
        for row in csv_data:
            writer.writerow(row)



class UTTERANCE:
    def __init__(self):
        self.name       = ""    # audio filename
        self.id_list    = []    # frame id
        self.phone_list = []    # frame phone
        self.phones     = ''    # merged phone

sil_id = 37
sil = 'L'

map_filename = '../../48_idx_chr.map_b'
map_id_to_39 = {}
with open(map_filename, 'r') as f:
    print "Load %s..." %map_filename
    for line in f.readlines():
        s = line.rstrip().split()
        phone_48 = s[0]
        phone_id = int(s[1])
        phone_39 = s[2]
        map_id_to_39[phone_id] = phone_39


data_dir = '../../feature'
dataname = 'train.fbank.label'

filename = os.path.join(data_dir, dataname)
utterance_all = []
current_name = ""
with open(filename, 'r') as f:
    print "Load %s..." %filename
    for line in f.readlines():
        s = line.rstrip().split()
        names = s[0].split('_')
        name = names[0] + '_' + names[1]
        id = int(s[1])
        if( name != current_name ):
            utterance = UTTERANCE()
            utterance.name = name
            current_name = name
            utterance_all.append(utterance)

        utterance.id_list.append(id)
        utterance.phone_list.append(map_id_to_39[id])
        


for utterance in utterance_all:
    phone_curr = ''
    
    phones_trim = ""
    # trimming
    for phone in utterance.phone_list:
        if phone != phone_curr:
            phone_curr = phone
            phones_trim += phone
    
    # eliminate sil at the beginning and the end
    st = 0
    ed = len(phones_trim)
    if( phones_trim[0] == sil ):
        st = 1
    if( phones_trim[-1] == sil ):
        ed -= 1
    
    utterance.phones = phones_trim[st:ed]
    #print '%s: %s' %(utterance.name, utterance.phones)

output_filename = 'test.pred'
save_label(output_filename, utterance_all)






