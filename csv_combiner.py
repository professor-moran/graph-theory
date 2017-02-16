import pandas as pd
import sys
import os

# Program to combine CSV files, by copying all column data from the input
# CSV file, then adding them as new columns to the destination CSV file.
#
# For information on how to use Pandas to read columnar data from one CSV file, and then
# append those columns to another CSV file (and write the updated contents of the 2nd
# CSV file), please refer to the following link:
# http://stackoverflow.com/questions/11070527/how-to-add-a-new-column-to-a-csv-file-using-python
#
# Start by adding the contents of the first CSV into the target file (note the 
# input file name, and the suffix used 'a'):
#
# python csv_combiner.py 100x100_results/instrument-analysis-graphtool-wilcoxon  wlcx_gt_dijk_grp2_iter2a-PARSED.csv ./ test.csv a 0
#
#
# Instructions:
#
# 1. Start by moving contents of iteration 'a' to the target output file. Note the 
# input file name, and the suffix values:
#   python csv_combiner.py 100x100_results/instrument-analysis-graphtool-wilcoxon  wlcx_gt_dijk_grp2_iter2a-PARSED.csv ./ test.csv a 0
#
# 2. Next, use iteration 'b' input file, and change the suffix accordingly:
#   python csv_combiner.py 100x100_results/instrument-analysis-graphtool-wilcoxon  wlcx_gt_dijk_grp2_iter2b-PARSED.csv ./ test.csv b 0
# 
# 3. Next, use iteration 'c' input file and change the suffix accordingly:
#   python csv_combiner.py 100x100_results/instrument-analysis-graphtool-wilcoxon  wlcx_gt_dijk_grp2_iter2c-PARSED.csv ./ test.csv c 0
#
# 4. Use iteration 'd' input file and change suffix accordingly:
#   python csv_combiner.py 100x100_results/instrument-analysis-graphtool-wilcoxon  wlcx_gt_dijk_grp2_iter2d-PARSED.csv ./ test.csv d 0
#
# 5. Merge last file, iteration 'e' and change suffix accordingly:
#   python csv_combiner.py 100x100_results/instrument-analysis-graphtool-wilcoxon  wlcx_gt_dijk_grp2_iter2e-PARSED.csv ./ test.csv e 0
#
# 6. Finally, renamed the merged output csv file (currently named test.csv in the above steps)
# into a more appropriate name. 
# 6b. Load the csv in Excel to check data.
# 6c. Load the (cleaned up) csv in SPSS to do statistical analysis.
# 
# Done!
#


############################################################
def isNotEmpty(s):
    return bool(s and s.strip())


############################################################
def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


############################################################
# This function creates the path, if it doesn't already exist,
# under the location of the current running script directory.
#
# Then it appends the filename to that path (but does not create
# the file itself), and returns the complete path + filename string.
#
# The caller is responsible for actually creating the file,
# using the string returned from this function as its fullpath
# and filename.
#
def createPathFileName( fileName, path, debug=False):

    #get path to this running Python script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if debug: print(">> script_dir = %s" % script_dir)
    
    #get target path:
    target_dir = os.path.join(script_dir, path)
    if debug: print(">> target_dir = %s" % target_dir)
    
    #attempt to make the directory, if it doesn't already exist:
    try:
        os.makedirs(target_dir)
        if debug: print(">> created directory: %s" % target_dir)
    except OSError:
        if debug: print(">> directory already exists?: %s" % target_dir )
        pass    #path already exists

    finalPathFileName = os.path.join( target_dir, fileName )
    return finalPathFileName


############################################################
# This function just checks to see if target directory
# exists or not. It does not create the directory.
# It looks for the target directory under the location of the
# current working directory where this script is running.
#
# The caller is responsible for creating the directory if it
# doesn't already exist. For more details, see function:
# "createPathFileName()".
#
def checkPath( path, debug=False ):

    #get path to this running Python script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if debug: print(">> script dir = %s" % script_dir)
    
    #build path to target path:
    target_dir = os.path.join(script_dir, path)
    if debug: print(">> target dir = %s" % target_dir)
    
    #does path exist?
    if os.path.exists(target_dir):
        if debug: print(">> found target path: %s" % target_dir)
        return True
    else:
        print(">> path %s does not exist." % target_dir)
        return False


############################################################
# Function that checks to see if path and file name exist.
# If they exist, True is returned, as is a string of the path+filename of the file.
# If the path does not exist, or the path exists but the file does not, then
# only a boolean False is returned.
#
def checkPathFile( fileName, path, debug=False):

    """
    #get path to this running Python script:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if debug: print(">> script dir = %s" % script_dir)
    
    #get path to output path + file:
    dest_dir = os.path.join(script_dir, path)
    if debug: print(">> target dir = %s" % dest_dir)
    
    #does path exist?
    if os.path.exists(dest_dir):
    """

    #First check to see if path exists:
    if (checkPath(path, debug) ):
        if debug: print(">> Path %s exists." % path)
        
        #Next check of target file exists:
        targetPathFileName = os.path.join ( path, fileName)
        if os.path.isfile(targetPathFileName):
            if debug: print(">> found target file: %s" % (targetPathFileName) )
            return True, targetPathFileName
        else:
            print(">> target file %s does not exist." % targetPathFileName)
            return False
    else: 
        print(">> path %s does not exist." % path)
        return False
        
############################################################

def main():

    #Display usage info:
    print ("\nUsage:\n %s [source file path: str] [source file name: str] [target file path: str] [target file name: str] [suffix: str] [debugMode: 0 or 1]\n" % str(sys.argv[0]) )
    print ("e.g.\n  python  %s  ./in_path  input.csv  ./out_path  output.csv  a1  0\n" % str(sys.argv[0]) )

    in_path = ''
    in_filename = ''
    out_path = ''
    out_filename = ''
    suffix = ''
    debug = 0
    
    
    #Read in the input params:
    in_path = str(sys.argv[1])
    if isNotEmpty(in_path) == False: 
        print ("Input path cannot be null or empty. Exiting.")
        sys.exit(1)

    in_filename = str(sys.argv[2])
    if isNotEmpty(in_filename) == False: 
        print ("Input filename cannot be null or empty. Exiting.")
        sys.exit(2)

    out_path = str(sys.argv[3])
    if isNotEmpty(out_path) == False:
        print("Output path cannot be null or empty. Exiting.")
        sys.exit(3)

    out_filename = str(sys.argv[4])
    if isNotEmpty(out_filename) == False:
        print("Output filename cannot be null or empty. Exiting.")
        sys.exit(4)

    suffix = str(sys.argv[5])
    if isNotEmpty(suffix) == False:
        print("Suffix cannot be null or empty. Exiting.")
        sys.exit(5)

    debug = int(sys.argv[6])
    if debug == 1: 
        debug = True
    else: 
        debug = False


    print("Running %s with user-selected options:" % str(sys.argv[0]) )
    print("  input Path=\t\t%s\n  input Filename=\t%s\n  output Path=\t\t%s\n  output Filename=\t%s\n  suffix=\t\t%s\n  debug=\t\t%s\n"
        % (in_path, in_filename, out_path, out_filename, suffix, debug) )


    inpath = False
    infile = False
    inpathfile = ''
    outpath = False
    outfile = False
    outpathfile = ''
    outresults = False
    outputfile = ''

    #Step 1: Check input path and input file:
    if ( checkPath( in_path, debug) ): 
        inpath = True
        print ("Input path [%s] exists" % in_path )
        results = checkPathFile( in_filename, in_path, debug)
        if ( results[0] ):
            infile = True
            inpathfile = results[1]
            print ("Input file [%s] exists" % inpathfile )

    if ( checkPath ( out_path, debug) ):
        outpath = True
        print ("Output path [%s] exists" % out_path )
        outresults = checkPathFile ( out_filename, out_path, debug)
        outputfile = createPathFileName( out_filename, out_path, debug)
        if ( outresults == False ):
            #outputfile = createPathFileName( out_filename, out_path, debug)
            print ("Output file [%s] does not exist." % outputfile)
            #file doesn't exist, so create it:
            touch( outputfile )
        else:
            print ("len(outresults) = %d" % len(outresults) )
            print ("Output file [%s] already exists." % outputfile)


    #Read the input file, pass in full directory path + filename:
    column_names = ['ALGORITHM_' + suffix, 'FILE_NAME_' + suffix, 'PATH_LENGTH_' + suffix, 'ELAPSED_TIME_' + suffix, 'MEMORY_CONSUMED_' + suffix]
    #print('Column names = %s' % column_names)
    #Pandas: pass in "header=0" to be able to replace existing column names in file with new ones:
    df1 = pd.read_csv(inpathfile, sep=",", header=0, names = column_names)
    #print ("Input file contents:")
    #print (df1)

    #output file is new, so just add new data to it:
    if (outresults == False):
        print("Writing to new csv file...")
        df1.to_csv(outputfile, sep=',', encoding='utf-8', index_label='INDEX', header=True, index=True) 
        print("Done.")
        
    #else if output file already exists, we're appending:
    elif (len(outresults) == 2 and outresults[0] == True):
        print("Appending...")
        column_names_target = ['ALGORITHM_1', 'FILE_NAME_1', 'PATH_LENGTH_1', 'ELAPSED_TIME_1', 'MEMORY_CONSUMED_1']
        #print('Column names target = %s' % column_names_target)
        #outputfile = createPathFileName( out_filename, out_path, debug)
        outputfile = outresults[1]
        df2 = pd.read_csv(outputfile, sep=",", header=0)
        #print ("Output file contents:")
        #print(df2)
        #Now append input of dataframe1 to target (dataframe2) file contents, then write df2.
        df2['ALGORITHM_' + suffix] = df1['ALGORITHM_' + suffix]
        df2['FILE_NAME_' + suffix] = df1['FILE_NAME_' + suffix]
        df2['PATH_LENGTH_' + suffix] = df1['PATH_LENGTH_' + suffix]
        df2['ELAPSED_TIME_' + suffix] = df1['ELAPSED_TIME_' + suffix]
        df2['MEMORY_CONSUMED_' + suffix] = df1['MEMORY_CONSUMED_' + suffix]
        df2.to_csv(outputfile, sep=',', encoding='utf-8', index=False, header=True)
        print("Done.")


############################################################

if __name__ == '__main__':
    main()

