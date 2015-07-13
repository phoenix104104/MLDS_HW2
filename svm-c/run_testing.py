#!/usr/bin/python -u
import sys, argparse, os

if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument('-f' , dest='feature_filename' , required=True, help='feature name')
    parser.add_argument('-c' , dest='c' , type=int, required=True, help='C')
    parser.add_argument('-n' , dest='n' , type=int, required=True, help='n-best')
    opts = parser.parse_args(sys.argv[1:])  
    
    input_dir  = '../../feature'
    model_dir  = '../../model'
    output_dir = '../../pred'

        
    # testing
    fv_name = 'test.%s' %opts.feature_filename
    test_filename = os.path.join(input_dir, fv_name)
    if( not os.path.isfile(test_filename) ):
        print "%s does not exist!" %test_filename
        exit(1)

    model_filename = os.path.join(model_dir, 'train.' + opts.feature_filename + '.c%d' %opts.c)
    if( not os.path.isfile(model_filename) ):
        print "%s does not exist!" %model_filename
        exit(1)
    

    output_filename = os.path.join(output_dir, '%s.c%s.nbest%s.pred' %(fv_name, str(opts.c), str(opts.n)) )

    cmd = "./svm_empty_classify %s %s %s" %(test_filename, model_filename, output_filename)
    print "============================================================================="
    print cmd
    print "============================================================================="
    os.system(cmd)

    # preprocessing
        
    cmd = './postprocess.py -i %s' %output_filename
    print "============================================================================="
    print cmd
    print "============================================================================="
    os.system(cmd)
    
   


