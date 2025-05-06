#https://mungingdata.com/python/split-csv-write-chunk-pandas/


batch_size=40000

def write_chunk(part_id , lines):
     with open("C:\\Users\\conne\\snowflake\\files\\load\\s3_data\\1995_part"+str(part_id)+".csv" , 'w') as fw:
          fw.write(header);
          fw.writelines(lines);
     

with open("C:\\Users\\conne\\snowflake\\files\\load\\s3_data\\1995\\1995_data.csv", "r") as f:
    count = 0
    lines = []
    header = f.readline() #this will repeat in  all files
    for l in f:
        lines.append(l)
        count += 1 #loop first 40000 lines and accumulate the counter till 40000 to be divisible by it
        if count % batch_size == 0 : #first 40k, next 80k and so on
            write_chunk(count // batch_size , lines )   # part file number (floor division) and lines list
            lines = [] #reset in order to hold next set of lines
    
    if len(lines) > 0:
          # we need this as the count won't be divisible by the batch size
          write_chunk((count // batch_size) + 1, lines ) #the remaining part ,say 26000




       