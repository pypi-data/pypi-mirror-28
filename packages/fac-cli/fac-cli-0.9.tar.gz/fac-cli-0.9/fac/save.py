from zipfile import ZipFile
from struct import Struct


class Deserializer:
    u16 = Struct('<H')
    u32 = Struct('<I')

    def __init__(self, stream):
        self.stream = stream
        self.version = tuple(self.read_u16() for i in range(4))

    def read(self, n):
        return self.stream.read(n)

    def read_fmt(self, fmt):
        return fmt.unpack(self.read(fmt.size))[0]

    def read_u8(self):
        return self.read(1)[0]

    def read_bool(self):
        return bool(self.read_u8())

    def read_u16(self):
        return self.read_fmt(self.u16)

    def read_u32(self):
        return self.read_fmt(self.u32)

    def read_str(self, dtype=None):
        length = self.read_fmt(dtype or self.u32)
        return self.read(length).decode('utf-8')

    def read_optim(self, dtype):
        if self.version >= (0, 14, 14, 0):
            byte = self.read_u8()
            if byte != 0xFF:
                return byte
        return self.read_fmt(dtype)

    def read_optim_u16(self):
        return self.read_optim(self.u16)

    def read_optim_u32(self):
        return self.read_optim(self.u32)

    def read_optim_str(self):
        length = self.read_optim_u32()
        return self.read(length).decode('utf-8')

    def read_optim_tuple(self, dtype, num):
        return tuple(self.read_optim(dtype) for i in range(num))


class SaveFile:
    def __init__(self, filename):
        zf = ZipFile(filename, 'r')
        datfile = None

        for f in zf.namelist():
            if f.endswith('/level.dat'):
                datfile = f
                break

        if not datfile:
            raise IOError("level.dat not found in save file")

        ds = Deserializer(zf.open(datfile))
        self.version = self.version_str(ds.version)
        self.campaign = ds.read_str()
        self.name = ds.read_str()
        self.base_mod = ds.read_str()

        # 0: Normal, 1: Old School, 2: Hardcore
        self.difficulty = ds.read_u8()

        self.finished = ds.read_bool()
        self.player_won = ds.read_bool()
        self.next_level = ds.read_str()  # usually empty

        if ds.version >= (0, 12, 0, 0):
            self.can_continue = ds.read_bool()
            self.finished_but_continuing = ds.read_bool()

        self.saving_replay = ds.read_bool()
        self.loaded_from = self.version_str(ds.read_optim_tuple(ds.u16, 3))
        self.loaded_from_build = ds.read_u16()

        self.allowed_commands = ds.read_u8()
        if ds.version <= (0, 13, 0, 87):
            if not self.allowed_commands:
                self.allowed_commands = 2
            else:
                self.allowed_commands = 1

        self.stats = {}
        if ds.version <= (0, 13, 0, 42):
            num_stats = ds.read_u32()
            for i in range(num_stats):
                force_id = ds.read_u8()
                self.stats[force_id] = []
                for j in range(3):
                    st = {}
                    length = ds.read_u32()
                    for k in range(length):
                        k = ds.read_u16()
                        v = ds.read_u32()
                        st[k] = v
                    self.stats[force_id].append(st)

        self.mods = {}
        num_mods = ds.read_u32()
        for i in range(num_mods):
            name = ds.read_optim_str()
            version = ds.read_optim_tuple(ds.u16, 3)
            if ds.version > (0, 15, 0, 91):
                ds.read_u32()  # CRC
            self.mods[name] = self.version_str(version)

    @staticmethod
    def version_str(ver):
        return '.'.join(str(x) for x in ver)


if __name__ == '__main__':
    import sys
    try:
        from yaml import safe_dump
    except ImportError:
        print('Install PyYAML for pretty printing')

        def safe_dump(s, **kw):
            return repr(s)

    for name in sys.argv[1:]:
        sf = SaveFile(name)
        print('%s:' % name)
        print()
        print(safe_dump(sf.__dict__, default_flow_style=False))
        print('---')
