import argparse
import gzip
import itertools
import sys
import traceback
from safeseqs import utilities

#Read the command line arguments and return them in args
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--supMutTabs', help='The Super Mutant Tabulation file name', required=True)
    parser.add_argument('-w', '--wellFam', help='The WellFamily file name', required=True)
    parser.add_argument('-r', '--reads', help='The reads file name', required=True)
    parser.add_argument('-b', '--barcodes', help='The barcodes file name', required=True)
    parser.add_argument('-o', '--output', help='reads', required=True)
    parser.add_argument('-i', '--index', help='indexes', required=True)

    args = parser.parse_args()
    return args    


def perform_get_example(args):
    UIDs ={}
    supMutTabs_fh = open(args.supMutTabs,'r')
    for line in supMutTabs_fh:
        t = utilities.SuperMutantTabsRecord(*line.strip().split('\t'))
        if (t.chrom == 'chr17' and t.position == '7578191' and t.baseFrom == 'A' and t.baseTo == 'G'):
            UIDs[t.uid] = {}
            target_barcode = t.barcode
    supMutTabs_fh.close()
    
    print('UIDs found: ' + str(len(UIDs)))
    
    if len(UIDs) == 0:
        return

#WellFamilyRecord = namedtuple('WellFamilyRecord', ['seqUID', 'read_seq', 'barcode', 'uid', 'read_cnt', 'primer'])
    read_cnt = 0
    wellFam_fh = open(args.wellFam,'r')
    for line in wellFam_fh:
        w = utilities.WellFamilyRecord(*line.strip().split('\t'))
        if (w.uid in UIDs):
            read_cnt += int(w.read_cnt)
            if w.read_seq not in UIDs[w.uid]:
                UIDs[w.uid][w.read_seq] = int(w.read_cnt)
            else:
                UIDs[w.uid][w.read_seq] += int(w.read_cnt)

    wellFam_fh.close()
    print('Reads to find: ' + str(read_cnt))
    
    read_fh = open(args.output,'w')
    index_fh = open(args.index,'w')
    reads = open_file(args.reads)
    indexes = open_file(args.barcodes)

    i = 0       
    read_cnt = 0
    #Process all the reads in the fastq reads file one read at a time.  
    #Reads have four lines in each file. As each line is read collect the pertinent info.
    #As a line is read from the fastq reads file, the corresponding 
    #index is read.
    for raw_read, raw_idx in itertools.zip_longest(reads, indexes):
        read = raw_read.strip() 
        idx = raw_idx.strip()
        i += 1
        if i == 1: #we are looking at the headers from the read and index; they must match when evaluating the read
            read_line1 = raw_read
            index_line1 = raw_idx
        elif i == 2: #save the UID that is on the front of the read sequence separately
            barcode = idx.upper()
            UidSequence = read[0: 14].upper()
            ReadSequence = read[14: len(read)].upper()
            read_line2 = raw_read
            index_line2 = raw_idx
        elif i == 3: 
            read_line3 = raw_read
            index_line3 = raw_idx
            
        elif i == 4: 
            read_line4 = raw_read
            index_line4 = raw_idx

            i = 0

            if barcode == target_barcode:
                if UidSequence in UIDs:
                    if ReadSequence in UIDs[UidSequence]:
                        read_cnt += 1
                        read_fh.write(read_line1)
                        read_fh.write(read_line2)
                        read_fh.write(read_line3)
                        read_fh.write(read_line4)
                        index_fh.write(index_line1)
                        index_fh.write(index_line2)
                        index_fh.write(index_line3)
                        index_fh.write(index_line4)

    print('Reads found: ' + str(read_cnt))
    reads.close()
    indexes.close()   
    read_fh.close()

def open_file(filepath):

    if filepath.endswith(".gz"):
        fh = gzip.open(filepath, "rt")
    else:
        fh = open(filepath, 'r')
    return fh
    
def main():
     
    args = get_args()
    
    try:
        perform_get_example(args)

    except Exception as err:
        traceback.print_exc()
        sys.exit(1)
    
       
if __name__ == "__main__": main()