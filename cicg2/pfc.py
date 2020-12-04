from libpfc import create_pfc
import argparse, os

  
def main():
    parser = argparse.ArgumentParser(description='Description a définir')
    parser.add_argument('-fn', '--file_name', required=True, help='Nom du fichier')
    args = parser.parse_args()
    print(args)

    try:
        fw = open(args.file_name, "w")
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        exit()
    except: #handle other exceptions such as attribute errors
        print("Unexpected error:", sys.exc_info()[0])
        exit()
        
    pfc = create_pfc('nom', 1, fw)
    
    fw.close()
    
    
if __name__ == '__main__':
    main()    