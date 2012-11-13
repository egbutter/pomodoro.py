import fcntl,struct,array
import re

SIOCGIFCONF = 0x00008912 
SIOCGIFFLAGS = 0x00008913
SIOCSIFFLAGS = 0x00008914
IFF_UP = 0x1

## .. if sys.platform in ['linux','linux2','darwin']

def get_ifaces(sockfd, names_expected=8):
    bytes_reserved = names_expected*32
    names = array.array('B', '\0'*bytes_reserved)
    names_struct = struct.pack('iL', bytes_reserved, names.buffer_info()[0])
    names_call = fcntl.ioctl(sockfd, SIOCGIFCONF, names_struct)
    bytes_returned = struct.unpack('iL', names_call)[0]
    names_str = names.tostring()
    return [names_str[i:i+32].split('\0', 1)[0] for i in range(0, bytes_returned, 32)]

def _get_flags(sockfd, iface):
    ifreq = struct.pack('16sh', iface, 0)
    return struct.unpack('16sh', fcntl.ioctl(sockfd, SIOCGIFFLAGS, ifreq))[1]

def _set_flags(sockfd, iface, flags):
    ifreq = struct.pack('16sh', iface, flags)
    fcntl.ioctl(sockfd, SIOCSIFFLAGS, ifreq)

def is_iface_on(sockfd,iface):
    flags = _get_flags(sockfd, iface)
    if flags & IFF_UP:
        return True
    return False

def turn_on_iface(sockfd, iface, flags):
    flags = _get_flags(sockfd, iface)
    flags = flags | IFF_UP
    _set_flags(sockfd, iface, flags)

def turn_off_iface(sockfd, iface):
    flags = _get_flags(sockfd, iface)
    flags = flags & ~IFF_UP
    _set_flags(sockfd, iface, flags)


## TODO repeat win32api DeviceIoControl, duck type over these methods

