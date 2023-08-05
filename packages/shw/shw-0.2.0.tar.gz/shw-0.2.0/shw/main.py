import os
import json
import argparse
import traceback
import sys


class CommandError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)
        


def init():
    home_dir = os.path.expandvars('$HOME')
    config_file = home_dir+'/.shw.json'
    if not os.path.exists(config_file):
        print 'config file not found, generating...'
        comments = """{
  "_comments": [
    "ip is server host",
    "name is about the name you gonna type",
    "and port"
  ],  
  "hosts": [
          {   
                  "cmd": "ssh command...",
                  "todo": "......"
          },  
          {"example": {
                  "cmd": "ssh username@host -p port"
          }
    }
  ]
}"""
        with open(config_file, 'a') as f:
            f.writelines(comments)

    # todo: error caption for wrong json format
    try:
        with open(config_file, 'rb') as f:
            json_data = json.load(f)
    except ValueError, e:
        print 'please check your ~/.shw.json file format'
        print str(e)
        traceback.format_exc()
        sys.exit(1)
    return json_data

def parse_json(json_data, args):
    key = args.name
    try:
        name = json_data.get('hosts')[1].get(key).get('name')
        ip = json_data.get('hosts')[1].get(key).get('ip')
        port = json_data.get('hosts')[1].get(key).get('port')
    except AttributeError, e:
        print traceback.format_exc()
        # print repr(e)
        print 'please make sure you type the right name~\n'
    prefix = '%s@%s:'%(name, ip)
    if args.command == 'scp':
        new_input = args.input
        new_out = prefix + args.output
        for f in args.input:
            if not os.path.exists(f):
                new_input = [prefix+i for i in args.input]
                new_out = args.output
                break
        return 'scp -P %s %s'%(" ".join(str(i) for i in new_input), new_out)
    else:
        return 'ssh %s -p %s'%(prefix[:-1], port)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", action='store', type=str, help='ssh name', required=True)
    parser.add_argument("-c", "--command", action="store", type=str, help="ssh or scp", required=True)
    parser.add_argument("-i", "--input",  nargs='+', help="scp input list file, when
                        use ~ for a remote home, use \~ since shell will convert ~ to your local homedir")
    parser.add_argument("-o", "--output", type=str, action="store", help="scp output list file")
    args = parser.parse_args()
    return args


def main():
    json_data = init()
    args = parse_args()
    if args.command not in ['scp', 'ssh']:
        raise CommandError("options not correct, must be ssh or scp")
    if args.command == 'scp':
        if args.input == None or args.output == None :
            raise CommandError("in scp mode, input list and output list must be soecified")
    command = parse_json(json_data, args)
    print command
    # os.system(command)
    # print args.n, type(args.n)


if __name__ == '__main__':
    main()

