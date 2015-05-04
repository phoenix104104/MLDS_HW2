import csv

sil = 'L'
 
class UTTERANCE:
    def __init__(self):
        self.name           = ""    # audio filename
        self.id_list        = []    # frame id
        self.phone_list     = []    # frame phone
        self.phone_sequence = ''    # merged phone

    def trimming(self):
        phone_sequence = ""
        phone_curr = ""
        # trimming
        for phone in self.phone_list:
            if phone != phone_curr:
                phone_curr = phone
                phone_sequence += phone
        
        # eliminate sil at the beginning and the end
        st = 0
        ed = len(phone_sequence)
        if( phone_sequence[0] == sil ):
            st = 1
        if( phone_sequence[-1] == sil ):
            ed -= 1
        
        self.phone_sequence = phone_sequence[st:ed]

def extract_audio_name(string):
    s = string.split('_')
    person = s[0]
    audio = s[1]
    return person, audio

def save_csv(output_filename, header, data):

    with open(output_filename, 'w+') as file:
        print "Save %s" %output_filename
        writer = csv.writer(file)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

def load_csv(input_filename):
    
    with open(input_filename, 'r') as f:
        print "Load %s" %input_filename
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.append(row)

    header = data[0]
    data = data[1:]
    
    return data

