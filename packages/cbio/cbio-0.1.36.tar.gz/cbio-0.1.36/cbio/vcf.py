class VCF():
    def __init__(self, filepath, args):
        self.filepath = filepath
        self.args = args

    def head(self):
        print('==> HEAD OF VCF FILE <==')
        c = 0
        fhand = open(self.filepath, 'r')
        for line in fhand:
            if line.startswith('##'):
                continue
            elif line.startswith('#'):
                print(line.strip('\n'))
                continue

            line = line.strip('\n').split('\t')

            if self.args.pretty:
                line[7] = line[7][0:4] + '[...]' + line[7][-7:]
            print('\t'.join(line))
            c += 1

            if c == 5:
                print()
                fhand.close()
                break

        return ()

    def tail(self):
        c = 0
        print('==> TAIL OF VCF FILE <==')
        print('#' + "\t".join(['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE']))

        fhand = open(self.filepath)
        lastLines = tl.tail(fhand, 5)
        fhand.close()

        for line in lastLines:
            if line.startswith('##'):
                continue
            elif line.startswith('#'):
                print(line.strip('\n'))
                continue

            line = line.strip('\n').split('\t')

            if self.args.pretty:
                line[7] = line[7][0:4] + '[...]' + line[7][-7:]
            print('\t'.join(line))
            c += 1

            if c == 5:
                print()
                break

        return ()
