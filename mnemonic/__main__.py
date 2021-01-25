from mnemonic import Mnemonic
import sys,os,argparse

def main() -> None:
    parser = argparse.ArgumentParser(description='Encode/Decode mnemonics')
    parser.add_argument('-i --input',dest='typein',choices=['generate','hex','entropy','mnemonic','stamp'],default='generate',help="generate mnemonic or input type at stdin")
    parser.add_argument('-o --output',dest='typeout',choices=['entropy','hex','mnemonic','stamp','seed','key'],default='mnemonic',help="type of output to print to stdout")
    parser.add_argument('-l --language',dest='lang',choices=[f.split('.')[0] for f in os.listdir(Mnemonic._get_directory())],default='english')
    parser.add_argument('-s --strength',dest='strength',choices = [128, 160, 192, 224, 256],default=128)
    parser.add_argument('-p --passphrase',dest='passphrase',type=str,default='')
    parser.add_argument('-t --testnet',dest='testnet',type=bool,default=False)
    args = parser.parse_args()

    m = Mnemonic(args.lang)
    # input types
    if args.typein == 'generate':
        mnemonic = m.generate(args.strength)
    elif args.typein == 'hex':
        num = int(sys.stdin.readline().strip(),16)
        mnemonic = m.from_int(num)
    elif args.typein == 'entropy':
        entropy = sys.stdin.buffer.read()
        mnemonic = m.to_mnemonic(entropy)
    elif args.typein == 'mnemonic':
        mnemonic = sys.stdin.readline().strip()
        if not m.check(mnemonic): raise ValueError(mnemonic)
    elif args.typein=='stamp':
        stamp = sys.stdin.readline().strip()
        mnemonic = m.from_stamp(stamp)
    # output types
    if args.typeout=='entropy':
        sys.stdout.buffer.write(m.to_entropy(mnemonic))
    if args.typeout=='hex':
        print(hex(m.to_int(mnemonic)))
    elif args.typeout=='mnemonic':
        print(mnemonic)
    elif args.typeout=='stamp':
        print(m.to_stamp(mnemonic))
    elif args.typeout=='seed':
        print(m.to_seed(mnemonic,args.passphrase))
    elif args.typeout=='key':
        print(m.to_hd_master_key(m.to_seed(mnemonic,args.passphrase),args.testnet))


if __name__ == "__main__":
    main()
