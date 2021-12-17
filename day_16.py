import numpy as np


def read():
    line = "005473C9244483004B001F79A9CE75FF9065446725685F1223600542661B7A9F4D001428C01D8C30C61210021F0663043A20042616C75868800BAC9CB59F4BC3A40232680220008542D89B114401886F1EA2DCF16CFE3BE6281060104B00C9994B83C13200AD3C0169B85FA7D3BE0A91356004824A32E6C94803A1D005E6701B2B49D76A1257EC7310C2015E7C0151006E0843F8D000086C4284910A47518CF7DD04380553C2F2D4BFEE67350DE2C9331FEFAFAD24CB282004F328C73F4E8B49C34AF094802B2B004E76762F9D9D8BA500653EEA4016CD802126B72D8F004C5F9975200C924B5065C00686467E58919F960C017F00466BB3B6B4B135D9DB5A5A93C2210050B32A9400A9497D524BEA660084EEA8EF600849E21EFB7C9F07E5C34C014C009067794BCC527794BCC424F12A67DCBC905C01B97BF8DE5ED9F7C865A4051F50024F9B9EAFA93ECE1A49A2C2E20128E4CA30037100042612C6F8B600084C1C8850BC400B8DAA01547197D6370BC8422C4A72051291E2A0803B0E2094D4BB5FDBEF6A0094F3CCC9A0002FD38E1350E7500C01A1006E3CC24884200C46389312C401F8551C63D4CC9D08035293FD6FCAFF1468B0056780A45D0C01498FBED0039925B82CCDCA7F4E20021A692CC012B00440010B8691761E0002190E21244C98EE0B0C0139297660B401A80002150E20A43C1006A0E44582A400C04A81CD994B9A1004BB1625D0648CE440E49DC402D8612BB6C9F5E97A5AC193F589A100505800ABCF5205138BD2EB527EA130008611167331AEA9B8BDCC4752B78165B39DAA1004C906740139EB0148D3CEC80662B801E60041015EE6006801364E007B801C003F1A801880350100BEC002A3000920E0079801CA00500046A800C0A001A73DFE9830059D29B5E8A51865777DCA1A2820040E4C7A49F88028B9F92DF80292E592B6B840"
    return hex_to_bin(line)


def hex_to_bin(hex_str):
    expected_length = 4 * len(hex_str)
    bin_str = str(bin(int(hex_str, 16)))[2:]
    return bin_str.zfill(expected_length)


def is_literal(bin_str):
    packet_type = bin_str[3:6]
    return packet_type == "100"


def get_type_id(bin_str):
    packet_type = bin_str[3:6]
    return int(packet_type, 2)


def get_version(bin_str):
    return int(bin_str[:3], 2)


def get_length_type_id(bin_str):
    return int(bin_str[6])


def get_length(bin_str, num_bits):
    start = 3 + 3 + 1
    end = start + num_bits
    length = bin_str[start:end]
    return int(length, 2)


def get_sub_packets_str(bin_str, length):
    start = 3 + 3 + 1 + 15
    end = start + length
    return bin_str[start:end]


def get_value(values, type_id):
    if type_id == 0:
        return sum(values)
    elif type_id == 1:
        return np.prod(values)
    elif type_id == 2:
        return min(values)
    elif type_id == 3:
        return max(values)
    elif type_id == 5:
        val = 1 if values[0] > values[1] else 0
        return val
    elif type_id == 6:
        val = 1 if values[0] < values[1] else 0
        return val
    elif type_id == 7:
        val = 1 if values[0] == values[1] else 0
        return val
    else:
        raise NotImplementedError(f"Don't know type id: {type_id}")

def solve(bin_str):
    if not bin_str:
        return 0

    version_num = get_version(bin_str)

    if is_literal(bin_str):
        print("literal")
        group_length = 5
        end = -1
        value = ""
        for i in range(6, len(bin_str), group_length):
            value += bin_str[i+1:i+group_length]
            if bin_str[i] == '0':  # Last group
                i += group_length
                end = i
                break

        value = int(value, 2)

        return version_num, end, value

    # its an operator
    id_ = get_length_type_id(bin_str)
    type_id = get_type_id(bin_str)

    if id_ == 0:
        print("Operator with 15 bits")
        length = get_length(bin_str, 15)
        print(f"Packet length: {length}")
        start = 3 + 3 + 1 + 15
        end = start + length
        values = []
        while start < end:
            sub_version, stop, value = solve(bin_str[start:start + length])
            version_num += sub_version
            start += stop
            length -= stop
            values.append(value)

        return version_num, end, get_value(values, type_id)
    else:
        print("Operator with 11 bits")
        num_sub_packets = get_length(bin_str, 11)
        print(f"Num packets: {num_sub_packets}")
        start = 3 + 3 + 1 + 11
        values = []

        for i in range(num_sub_packets):
            sub_version, stop, value = solve(bin_str[start:])
            start += stop
            version_num += sub_version
            values.append(value)

        return version_num, start, get_value(values, type_id)


def main():
    inp = read()
    version_sum = solve(inp)
    print(version_sum)


if __name__ == "__main__":
    main()