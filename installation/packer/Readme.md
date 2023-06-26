# Launch Qemu

```
sudo packer build -var-file="variables.pkrvars.hcl" ubuntu.pkr.hcl
sudo qemu-system-aarch64  -M virt -append "rw earlyprinrw root=/dev/vda2 console=ttyAMA0 loglevel=8 rootwait fsck.repair=yes memtest=1" -initrd initrd.img -kernel vmlinuz -m 1G -cpu cortex-a72 -serial stdio -drive file=ubuntu.img -netdev user,id=net0,hostfwd=tcp::5022-:22 -device virtio-net-device,netdev=net0
```
