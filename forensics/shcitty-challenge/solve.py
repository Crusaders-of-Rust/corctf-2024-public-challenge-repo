"""
With the given shc version and command arguments, you can compile/encrypt a few test scripts and spot some patterns.
Looking at the generated intermediate C files, take note of the ARC4 algo, xsh crypt function, and write a crypter to
decyrpt and print the known offsets and lengths of the data array to find bytestrings to use for cribbing.
In our solver, load the .data section, clean it, and sliding window brute force each sequential crypt call data section
with our cribs to decrypt the text/original shell script.

If the "-r" was used during shc generation, run the script as-is.

If the "-r" option was NOT used, details about the system default shell binary are used in the encryption process.
You will need to compile and run the below C program ON THE MACHINE USED TO GENERNATE THE SHC ENCRYPTED BINARY
to get this information to use in decryption. Save the printed "Control Bytes" output of this program to the
variable "control" in this script, set "RFLAG = False", and run as normal.

```c
#include <stdio.h>     // printf
#include <string.h>    // memset
#include <sys/stat.h>  // stat statf


int key_with_file(char * file)
{
        struct stat statf[1];
        struct stat control[1];

        if (stat(file, statf) < 0)
                return -1;

        /* Turn on stable fields */
        memset(control, 0, sizeof(control));
        control->st_ino = statf->st_ino;
        control->st_dev = statf->st_dev;
        control->st_rdev = statf->st_rdev;
        control->st_uid = statf->st_uid;
        control->st_gid = statf->st_gid;
        control->st_size = statf->st_size;
        control->st_mtime = statf->st_mtime;
        control->st_ctime = statf->st_ctime;

        // Print readable file information
        printf("\nInode Number: %lu\n", control->st_ino);
        printf("Device Number: %lu\n", control->st_dev);
        printf("Device ID: %lu\n", control->st_rdev);
        printf("User ID: %u\n", control->st_uid);
        printf("Group ID: %u\n", control->st_gid);
        printf("File Size: %ld\n", control->st_size);
        printf("Last Modification Time: %ld\n", control->st_mtime);
        printf("Last Status Change Time: %ld\n\n", control->st_ctime);

        // Print raw bytes of control
        unsigned char *bytes = (unsigned char *)control;
        printf("\nControl bytes: ");
        for (size_t i = 0; i < sizeof(control); i++) {
            printf("%02x", bytes[i]);
        }
        printf("\n\n");
        return 0;
}

int main()
{
    char *filepath = "/bin/sh";
    int result = key_with_file(filepath);
    if (result == -1) {
        printf("Failed to retrieve file stats.\n\n");
    }
    return 0;
}
```

In our "teminal_output.txt" we can see that a similar program is run by the user, giving us the
the "control bytes" information we need for the host default shell binary, so in the "file_information.c"
file, we can just fill in those values and print out the "control" struct hex bytes as shown above, or
use the "get_control_bytes" function below.
"""
import struct
import lief


def get_control_bytes(st_dev, st_ino, st_id, st_gid, st_rdev, st_size,
                      st_mtime, st_ctime):
    """Generate a byte sequence representing a structured control block."""

    # Define the values
    control_bytes = struct.pack(

        # Types are probably fucked up, hell I may have even fucked 
        #  the order up but I don't care because it works
        "QQQQIIQQQQQQQQQQQQQ",  # Format string

        st_dev,  # 8 bytes
        st_ino,  # 8 bytes
        0,  # 8 bytes Unused
        0,  # 8 bytes Unused
        st_id,  # 4 bytes
        st_gid,  # 4 bytes
        st_rdev,  # 8 bytes
        st_size,  # 8 bytes
        0,  # 8 bytes Unused
        0,  # 8 bytes Unused
        0,  # 8 bytes Unused
        0,  # 8 bytes Unused
        st_mtime,  # 8 bytes
        0,  # 8 bytes Unused
        st_ctime,  # 8 bytes
        0,  # 8 bytes Unused
        0,  # 8 bytes Unused
        0,  # 8 bytes Unused
        0,  # 8 bytes Unused
    )
    return control_bytes


# 'Alleged RC4' #

# Global state for the RC4 cipher
stte = list(range(256))
indx = 0
jndx = 0
kndx = 0


def stte_0():
    """Reset the RC4 state."""
    global stte, indx, jndx, kndx
    indx = jndx = kndx = 0
    stte = list(range(256))


def key(data):
    """Set the key for RC4. This can be called multiple times."""
    global stte, indx, kndx
    len_data = len(data)
    while len_data > 0:
        while indx < 256:
            tmp = stte[indx]
            kndx = (kndx + tmp + data[indx % len(data)]) % 256
            stte[indx], stte[kndx] = stte[kndx], stte[indx]
            indx += 1
        data = data[256:]  # Move the pointer by 256 bytes in the array
        len_data -= 256
        indx = 0  # Reset indx for next block


def arc4(data):
    """Encrypt or decrypt data in-place using the current RC4 state."""
    global stte, indx, jndx
    n = len(data)
    output = bytearray(data)
    for i in range(n):
        indx = (indx + 1) % 256
        jndx = (jndx + stte[indx]) % 256
        stte[indx], stte[jndx] = stte[jndx], stte[indx]
        t = (stte[indx] + stte[jndx]) % 256
        output[i] ^= stte[t]
    data[:] = output  # Update the original data in-place


# End of ARC4 #


# Binary file to crack
FILE = "flag"

# Crib text to use for the original shell script
CRIB = "#!/bin/sh"

# Set False if shc was run without the -r option 
RFLAG = False

# File stat details of the host system default shell binary used for encryption
DEVICE_NUMBER = 2050
INODE_NUMER = 42467530
USER_ID = 0
GROUP_ID = 0
DEVICE_ID = 0
FILE_SIZE = 125688
LAST_MODIFICATION_TIME = 1648043363
LAST_STATUS_CHANGE_TIME = 1686442713

try:
    control = get_control_bytes(DEVICE_NUMBER, INODE_NUMER, USER_ID, GROUP_ID,
                                DEVICE_ID, FILE_SIZE, LAST_MODIFICATION_TIME,
                                LAST_STATUS_CHANGE_TIME)
except:
    control = b'\x00'

# Load the ELF file
elf_file = lief.parse(FILE)

# Find the .data section
data_section = elf_file.get_section(".data")
if data_section:
    # Get the content of the .data section as a list of bytes (integers)
    # Convert list of integers to a bytearray
    # Remove the first 32 bytes
    # Strip trailing null bytes (0x00)
    data = bytearray(data_section.content)[32:].rstrip(b'\x00')

# Data and pswd size
data_size = len(data)
pswd_size = 256

# # Cribs; may need to adjust depending on options used when shc was run

# Round 1 cribs
msg1_content = b'has expired!\nPlease contact your provider jahidulhamid@yahoo.com\x00'
msg1_size = len(msg1_content)
date_content = b'\x00'
date_size = len(date_content)
shll_content = b'/bin/sh\x00'
shll_size = len(shll_content)
inlo_content = b'-c\x00'
inlo_size = len(inlo_content)
xecc_content = b'exec \'%s\' "$@"\x00'
xecc_size = len(xecc_content)
lsto_content = b'\x00'
lsto_size = len(lsto_content)
tst1_content = b'location has changed!\x00'
tst1_size = len(tst1_content)

# Round 2 cribs
chk1_content = b'location has changed!\x00'
chk1_size = len(chk1_content)
msg2_content = b'abnormal behavior!\x00'
msg2_size = len(msg2_content)
rlax_content = b'\x92'
rlax_size = len(rlax_content)
opts_content = b'\x00'
opts_size = len(opts_content)
chk2_size = 19 # Not used
tst2_size = 19 # Not used

# Largest possible text size
p_text_size = data_size - sum([
    pswd_size, msg1_size, date_size, shll_size, inlo_size, xecc_size,
    lsto_size, tst1_size, chk1_size, msg2_size, rlax_size, opts_size,
    chk2_size, tst2_size
])

# Get key and round 1 crypt
for pswd_s_idx in range(data_size - pswd_size + 1):
    pswd = data[pswd_s_idx:pswd_s_idx + pswd_size]
    for msg1_s_idx in range(data_size - msg1_size + 1):
        msg1 = data[msg1_s_idx:msg1_s_idx + msg1_size]
        stte_0()
        key(pswd)
        arc4(msg1)
        if msg1 == msg1_content:
            # print(msg1)

            for date_s_idx in range(data_size - date_size + 1):
                date = data[date_s_idx:date_s_idx + date_size]
                stte_0()
                key(pswd)
                arc4(msg1)
                arc4(date)
                if date == date_content:
                    # print(date)

                    for shll_s_idx in range(data_size - shll_size + 1):
                        shll = data[shll_s_idx:shll_s_idx + shll_size]
                        stte_0()
                        key(pswd)
                        arc4(msg1)
                        arc4(date)
                        arc4(shll)
                        if shll == shll_content:
                            # print(shll)

                            for inlo_s_idx in range(data_size - inlo_size + 1):
                                inlo = data[inlo_s_idx:inlo_s_idx + inlo_size]
                                stte_0()
                                key(pswd)
                                arc4(msg1)
                                arc4(date)
                                arc4(shll)
                                arc4(inlo)
                                if inlo == inlo_content:
                                    # print(inlo)

                                    for xecc_s_idx in range(data_size - xecc_size + 1):
                                        xecc = data[xecc_s_idx:xecc_s_idx + xecc_size]
                                        stte_0()
                                        key(pswd)
                                        arc4(msg1)
                                        arc4(date)
                                        arc4(shll)
                                        arc4(inlo)
                                        arc4(xecc)
                                        if xecc == xecc_content:
                                            # print(xecc)

                                            for lsto_s_idx in range(data_size - lsto_size + 1):
                                                lsto = data[lsto_s_idx:lsto_s_idx + lsto_size]
                                                stte_0()
                                                key(pswd)
                                                arc4(msg1)
                                                arc4(date)
                                                arc4(shll)
                                                arc4(inlo)
                                                arc4(xecc)
                                                arc4(lsto)
                                                if lsto == lsto_content:
                                                    # print(lsto)

                                                    for tst1_s_idx in range(data_size - tst1_size + 1):
                                                        tst1 = data[tst1_s_idx:tst1_s_idx + tst1_size]
                                                        stte_0()
                                                        key(pswd)
                                                        arc4(msg1)
                                                        arc4(date)
                                                        arc4(shll)
                                                        arc4(inlo)
                                                        arc4(xecc)
                                                        arc4(lsto)
                                                        arc4(tst1)
                                                        if tst1 == tst1_content:
                                                            # print(tst1)

                                                            # Round 2 crypt, preserve keys
                                                            for chk1_s_idx in range(data_size - chk1_size + 1):
                                                                pswd = data[pswd_s_idx:pswd_s_idx + pswd_size]
                                                                tst1 = data[tst1_s_idx:tst1_s_idx + tst1_size]
                                                                chk1 = data[chk1_s_idx:chk1_s_idx + chk1_size]
                                                                stte_0()
                                                                key(pswd)
                                                                arc4(msg1)
                                                                arc4(date)
                                                                arc4(shll)
                                                                arc4(inlo)
                                                                arc4(xecc)
                                                                arc4(lsto)
                                                                arc4(tst1)
                                                                key(tst1)
                                                                arc4(chk1)
                                                                if chk1 == chk1_content:
                                                                    # print(chk1)

                                                                    for msg2_s_idx in range(data_size - msg2_size + 1):
                                                                        pswd = data[pswd_s_idx:pswd_s_idx + pswd_size]
                                                                        tst1 = data[tst1_s_idx:tst1_s_idx + tst1_size]
                                                                        msg2 = data[msg2_s_idx:msg2_s_idx + msg2_size]
                                                                        stte_0()
                                                                        key(pswd)
                                                                        arc4(msg1)
                                                                        arc4(date)
                                                                        arc4(shll)
                                                                        arc4(inlo)
                                                                        arc4(xecc)
                                                                        arc4(lsto)
                                                                        arc4(tst1)
                                                                        key(tst1)
                                                                        arc4(chk1)
                                                                        arc4(msg2)
                                                                        if msg2 == msg2_content:
                                                                            # print(msg2)

                                                                            for rlax_s_idx in range(data_size - rlax_size + 1):
                                                                                pswd = data[pswd_s_idx:pswd_s_idx + pswd_size]
                                                                                tst1 = data[tst1_s_idx:tst1_s_idx + tst1_size]
                                                                                rlax = data[rlax_s_idx:rlax_s_idx + rlax_size]
                                                                                stte_0()
                                                                                key(pswd)
                                                                                arc4(msg1)
                                                                                arc4(date)
                                                                                arc4(shll)
                                                                                arc4(inlo)
                                                                                arc4(xecc)
                                                                                arc4(lsto)
                                                                                arc4(tst1)
                                                                                key(tst1)
                                                                                arc4(chk1)
                                                                                arc4(msg2)
                                                                                arc4(rlax)

                                                                                for opts_s_idx in range(data_size - opts_size + 1):
                                                                                    pswd = data[pswd_s_idx:pswd_s_idx + pswd_size]
                                                                                    tst1 = data[tst1_s_idx:tst1_s_idx + tst1_size]
                                                                                    opts = data[opts_s_idx:opts_s_idx + opts_size]
                                                                                    stte_0()
                                                                                    key(pswd)
                                                                                    arc4(msg1)
                                                                                    arc4(date)
                                                                                    arc4(shll)
                                                                                    arc4(inlo)
                                                                                    arc4(xecc)
                                                                                    arc4(lsto)
                                                                                    arc4(tst1)
                                                                                    key(tst1)
                                                                                    arc4(chk1)
                                                                                    arc4(msg2)
                                                                                    arc4(rlax)
                                                                                    if not RFLAG:
                                                                                        key(control)
                                                                                    arc4(opts)
                                                                                    if opts == opts_content:
                                                                                        # print(opts)

                                                                                        while p_text_size > 0:
                                                                                            for text_s_idx in range(data_size):
                                                                                                pswd = data[pswd_s_idx:pswd_s_idx + pswd_size]
                                                                                                tst1 = data[tst1_s_idx:tst1_s_idx + tst1_size]
                                                                                                text = data[text_s_idx:text_s_idx + data_size]
                                                                                                stte_0()
                                                                                                key(pswd)
                                                                                                arc4(msg1)
                                                                                                arc4(date)
                                                                                                arc4(shll)
                                                                                                arc4(inlo)
                                                                                                arc4(xecc)
                                                                                                arc4(lsto)
                                                                                                arc4(tst1)
                                                                                                key(tst1)
                                                                                                arc4(chk1)
                                                                                                arc4(msg2)
                                                                                                arc4(rlax)
                                                                                                if not RFLAG:
                                                                                                    key(control)
                                                                                                arc4(opts)
                                                                                                arc4(text)
                                                                                                if CRIB.encode("utf-8") in text:
                                                                                                    print("\n" + text[:p_text_size].decode("utf-8", errors="ignore"))
                                                                                                    # print("\n", text[:p_text_size])
                                                                                                    quit()
