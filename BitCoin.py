# to read csv file
from csv import reader

# global varibles
netWeight = 0
netProfit = 0

data = {} 
data_list = []
id_list = []

class MempoolTransaction():
    
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = [parent for parent in parents.strip().split(';')]
        if(self.parents[0] == '' and self.weight <= 4000000):
            data[self.txid] = {
                'fee': self.fee,
                'self_fee': self.fee,
                'weight': self.weight,
                'self_weight': self.weight,
                'parent': []
            }
            
        else:
            if set(self.parents).issubset(data.keys()):
                amt = self.weight
                cut = self.fee
                for parent in self.parents:
                    if((amt + data[parent]['weight']) <= 4000000):
                        amt += data[parent]['weight']
                        cut += data[parent]['fee']
                    else:
                        break
                data[self.txid] = {
                                    'fee': cut,
                                    'self_fee': self.fee,
                                    'weight': amt,
                                    'self_weight': self.weight,
                                    'parent': self.parents
                                }
            
            else:
                return

def parse_mempool_csv():
    with open("mempool.csv", "r") as file:
        next(file)
        csv_reader = reader(file)
        for row in csv_reader:
            MempoolTransaction(row[0], row[1], row[2], row[3])

parse_mempool_csv()



def adder(parent):
    data_list.append(
        [
            parent, 
            data[parent]['fee'], 
            data[parent]['self_fee'], 
            data[parent]['weight'], 
            data[parent]['self_weight']
        ]
    )

def iterator(parents):
    for parent in parents:
        if data[parent]['parent']:
            iterator(data[parent]['parent'])

        if parent not in data_list:
            adder(parent)

for key, val in data.items():
    if val['parent']:
        iterator(val['parent'])
    
    if key not in data_list:
        adder(key)

data_list.sort(key= lambda x: x[1], reverse=True)

def duplicate_check(parents):
    for parent in parents:

        if data[parent]['parent']:
            duplicate_check(data[parent]['parent'])

        if parent not in id_list:
            id_list.append(parent)


for entry in data_list:
    if (entry[3] + netWeight) <= 4000000:

        if data[entry[0]]['parent']:
            duplicate_check(data[entry[0]]['parent'])

        if entry[0] not in id_list:
            id_list.append(entry[0])

        netWeight += entry[3]
        netProfit += entry[1]



open("block.txt", "w").close()
f = open("block.txt", "a")
for id in id_list:
    f.write(f"{id}\n")
f.close()
print("Successfully completed!!")
