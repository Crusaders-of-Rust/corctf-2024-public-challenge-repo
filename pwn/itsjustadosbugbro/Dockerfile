FROM alpine

RUN apk add --no-cache qemu-system-x86_64

WORKDIR /opt
COPY bzImage initramfs.cpio.gz ./

CMD stty intr '^]' && \
    qemu-system-x86_64 \
        -m 512M \
        -smp 1 \
        -nographic \
        -kernel "./bzImage" \
        -append "console=ttyS0 loglevel=3 panic=-1 oops=panic clearcpuid=smap pti=on no5lvl" \
        -no-reboot \
        -monitor /dev/null \
        -cpu host \
        -nic none \
        -initrd "./initramfs.cpio.gz" \
        -enable-kvm
