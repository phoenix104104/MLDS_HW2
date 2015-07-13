#!/usr/bin/python -u
import sys, argparse, os

if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument('-f' , dest='feature_filename' , required=True, help='feature name')
    parser.add_argument('-c' , dest='c' , type=int, required=True, help='C')
    opts = parser.parse_args(sys.argv[1:])  
    
    input_dir  = '../../feature'
    model_dir  = '../../model'
    output_dir = '../../pred'

    train_filename = os.path.join(input_dir, 'train.' + opts.feature_filename)
    model_filename = os.path.join(model_dir, 'train.' + opts.feature_filename + '.c%d' %opts.c)
    
    if( not os.path.isfile(train_filename) ):
        print "%s does not exist!" %train_filename
        exit(1)
        
    # training
    cmd = './svm_empty_learn -c %s %s %s' %(str(opts.c), train_filename, model_filename)
    print "============================================================================="
    print cmd
    print "============================================================================="
    os.system(cmd)

    # testing
    for t in ["test", "test.old"]:
        fv_name = '%s.%s' %(t, opts.feature_filename)
        test_filename = os.path.join(input_dir, fv_name)
        output_filename = os.path.join(output_dir, '%s.c%s.pred' %(fv_name, str(opts.c)) )

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
    
   


