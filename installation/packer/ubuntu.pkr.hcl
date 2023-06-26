variable "wifi_ssid" {
  type = string
}

variable "wifi_password" {
  type      = string
  sensitive = true
}

variables {
  home = env("HOME")
}

source "arm" "ubuntu" {
  file_urls             = [
    "https://cdimage.ubuntu.com/releases/22.04.2/release/ubuntu-22.04.2-preinstalled-server-arm64+raspi.img.xz"
  ]
  file_checksum_url     = "http://cdimage.ubuntu.com/releases/22.04.2/release/SHA256SUMS"
  file_checksum_type    = "sha256"
  file_target_extension = "xz"
  file_unarchive_cmd    = ["xz", "--decompress", "$ARCHIVE_PATH"]
  image_build_method    = "reuse"
  image_path            = "ubuntu.img"
  image_size            = "3.9G"
  image_type            = "dos"

  image_partitions {
    name         = "boot"
    type         = "c"
    start_sector = "2048"
    filesystem   = "fat"
    size         = "256M"
    mountpoint   = "/boot/firmware"
  }
  image_partitions {
    name         = "root"
    type         = "83"
    start_sector = "526336"
    filesystem   = "ext4"
    size         = "3.6G"
    mountpoint   = "/"
  }

  image_chroot_env             = ["PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"]
  qemu_binary_source_path      = "/usr/bin/qemu-aarch64-static"
  qemu_binary_destination_path = "/usr/bin/qemu-aarch64-static"
}

build {
  sources = ["source.arm.ubuntu"]

  provisioner "file" {
    source      = "${var.home}/.ssh/id_rsa.pub"
    destination = "/tmp/id_rsa.pub"
  }

  provisioner "file" {
    source      = "resources/network-config"
    destination = "/boot/firmware/network-config"
  }

  provisioner "file" {
    source      = "resources/user-data"
    destination = "/boot/firmware/user-data"
  }

  provisioner "shell" {
    inline = [
      "touch /boot/ssh",
      "touch /boot/firmware/meta-data",
      "touch /boot/firmware/vendor-data",
      "sed -i 's/$wifi_ssid/${var.wifi_ssid}/g' /boot/firmware/network-config",
      "sed -i 's/$wifi_password/${var.wifi_password}/g' /boot/firmware/network-config",
      "sed -i '/$ssh_public_key/ r /tmp/id_rsa.pub' /boot/firmware/user-data",
      "sed -i -z 's/$ssh_public_key\\n//g' /boot/firmware/user-data",
      "rm /tmp/id_rsa.pub"
    ]
  }

  provisioner "file" {
    direction   = "download"
    source      = "/boot/firmware/initrd.img"
    destination = "./"
  }

  provisioner "file" {
    direction   = "download"
    source      = "/boot/firmware/vmlinuz"
    destination = "./"
  }
}
