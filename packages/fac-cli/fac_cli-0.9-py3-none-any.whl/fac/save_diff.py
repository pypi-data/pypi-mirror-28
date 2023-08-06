from save import SaveFile

if __name__ == '__main__':
    import sys
    import yaml
    unklist = []
    values = {}
    for name in sys.argv[1:]:
        sf = SaveFile(name)
        unklist.append(sf.unknowns)

    for i, unk in enumerate(unklist):
        for k in unk:
            if k not in unk:
                continue
            if k not in values:
                values[k] = {}
            if unk[k] not in values[k]:
                values[k][unk[k]] = []
            values[k][unk[k]].append(sys.argv[1 + i])

    for k, vals in values.items():
        print('Values for field %s:' % k)
        for v, saves in vals.items():
            print(' - Value %r in:' % v)
            for save in saves:
                if '_autosave' in save:
                    continue
                print('   - %s' % save)
            print()
        print()

