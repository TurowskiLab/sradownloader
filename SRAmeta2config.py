#!/usr/bin/env python

import pandas as pd
import urllib.request
import re, argparse

usage = "Converts SRA metafile into excel with additional data. The Excel file can be used as input for SRA_download.py"

parser = argparse.ArgumentParser(usage=usage, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
files = parser.add_argument_group('Options for input files')
files.add_argument("-f", dest="csv_file", help="CSV file name or path",
                 required=True, type=str)
files.add_argument("-o", dest="out_file", help="output file name or path. If empty the suffix is replaced to .xlsx",default=None)
args = parser.parse_args()

f_name=args.csv_file
if args.out_file:
    out_file = args.out_file
else:
    out_file = f_name.split(".")[0]+".xlsx"

def get_geo_name(srr_number,splitName=True):
    sample_name = ""

    with urllib.request.urlopen(f"https://www.ncbi.nlm.nih.gov/sra/?term={srr_number}&format=text") as response:
        for line in response:
            line = line.decode("UTF-8")
            if line.startswith("Title:"):
                line = line.strip()
                geosections = re.split("[:; ,]+",line)

                sample_name = "_".join(geosections[1:])
                break
    if splitName==True:
        sample_name = sample_name.split("_")[1:-3]
        return "_".join(sample_name)
        
    else:
        return sample_name

df_input = pd.read_csv(f_name,sep=',')

df_input['name_full'] = ""
df_input['exp_type'] = ""
df_input['author'] = ""
df_input['year'] = ""
df_input['month'] = ""
df_input['day'] = ""
df_input['bait'] = ""
df_input['background'] = ""
df_input['condition'] = ""
df_input['replicate'] = ""
df_input['media'] = df_input['Run'].apply(get_geo_name)
df_input['strandness'] = ""
df_input['barcode_id'] = ""
df_input['index_id'] = ""
df_input['index_id'] = ""
df_input['5adapter'] = ""
df_input['3adapter'] = ""
df_input['link'] = ""
df_input['strain'] = ""

df_final = df_input[['Run','name_full','exp_type',"SRA Study",'author','year','month','day','bait','background','condition','replicate','Organism','media','LibraryLayout',"AvgSpotLen","strandness","barcode_id",'index_id','index_id','5adapter','3adapter','link','strain']]
df_final.columns = ["SRR","name_full",'exp_type','exp_id','author','year','month','day','bait','background','condition','replicate','organism','media',"SEorPE","read_length","strandness","barcode_id",'index_id','index_id','5adapter','3adapter','link','strain']

df_final.to_excel(out_file,index=False)