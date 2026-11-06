"""Package/verify only. No upload, Azure login or service activation."""
import argparse,pathlib,sys,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from reference.release_package import package,verify
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=pathlib.Path,default=pathlib.Path('sample-api'));parser.add_argument('--output',type=pathlib.Path,default=pathlib.Path('.release'));parser.add_argument('--source-sha',required=True);args=parser.parse_args()
    receipt=package('api',args.source,args.output,args.source_sha);verify('api',args.output,args.source_sha)
    print(json.dumps({'packageVerified':True,**receipt,'uploaded':False,'servicesStarted':False}))
