import subprocess
from color import colors

log_file = "command_logs.txt"


def run_command(command):
    print(colors.fg.green + "Running command: " + colors.reset + command)
    log_command(colors.fg.green + f"Running command: " + colors.reset + command)

    try:
        # Виконання команди і збереження виводу в змінну
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)

        # Збереження виводу команди у файл логів
        with open(log_file, "a") as f:
            f.write(result.stdout)

    except subprocess.CalledProcessError as e:
        # Збереження інформації про помилку
        log_command(colors.fg.red + f"Error command: {command}" + colors.reset)
        log_command(str(e))
        exit(1)


def log_command(log_message):
    # Запис інформації у файл логів
    with open(log_file, "a") as f:
        f.write(log_message + "\n")


def arch_system():
    run_command("echo 'User-PC' >> /etc/hostname")
    run_command("ln -sf /usr/share/zoneinfo/Europe/Kiev /etc/localtime")
    run_command(r"sed -i -E 's%^# *(\(en_US.UTF-8 UTF-8\)) %\1%' /etc/locale.gen")
    run_command(r"sed -i -E 's%^# *(\(uk_UA.UTF-8 UTF-8\)) %\1%' /etc/locale.gen")
    run_command(r"sed -i -E 's%^# *(\(ru_RU.UTF-8 UTF-8\)) %\1%' /etc/locale.gen")
    run_command("locale-gen")
    run_command("echo 'LANG=en_US.UTF-8' >> /etc/locale.conf")
    run_command("mkinitcpio -P")

def grub():
    run_command("pacman -Syy")
    run_command("pacman -S --noconfirm grub efibootmgr")
    run_command("grub-install /dev/sda")
    run_command("pacman -S --noconfirm os-prober mtools fuse")
    run_command("grub-mkconfig -o /boot/grub/grub.cfg")


def user():
    run_command("useradd -m -g users -G wheel -s /bin/zsh user")


def root_password():
    new_password = "1234"  # Замініть на фактичний пароль
    command = f"echo '{new_password}\n{new_password}' | passwd"
    subprocess.run(command, shell=True)


def user_password():
    new_password = "1234"  # Замініть на фактичний пароль
    command = f"echo '{new_password}\n{new_password}' | passwd user"
    subprocess.run(command, shell=True)


def add_user_root():
    run_command(r"sed -i '/root ALL=(ALL:ALL) ALL/a user ALL=(ALL:ALL) ALL' /etc/sudoers")


def mirrorlist():
    run_command(r"sed -i 's/^#\(ParallelDownloads = 5\)/\1/' /etc/pacman.conf")
    run_command(r"sed -i 's/^#[[:space:]]*\(UseSyslog\)/\1/' /etc/pacman.conf")
    run_command(r"sed -i 's/^#[[:space:]]*\(Color\)/\1/' /etc/pacman.conf")
    run_command(r"sed -i 's/^#[[:space:]]*\(VerbosePkgLists\)/\1/' /etc/pacman.conf")
    run_command(r"sed -i 's/^#[[:space:]]*\[multilib\]/[multilib]/' /etc/pacman.conf")
    run_command(r"sed -i '/^\[multilib\]$/,/^$/ s/^#[[:space:]]*\(.*\)/\1/' /etc/pacman.conf")
    run_command("reflector --verbose --country 'Ukraine,Germany' --sort rate --save /etc/pacman.d/mirrorlist")


def aur():
    run_command("git clone https://aur.archlinux.org/yay.git")
    run_command("cd yay")
    run_command("makepkg -sric --install")
    run_command("pacman -Syy")
    run_command("cd")


def install_pkg():
    run_command("pacman -Syy")
    run_command("pacman -Syy")
    run_command("pacman-key --init")
    run_command("pacman-key --populate archlinux")
    run_command("pacman -S --noconfirm lrzip unrar unzip unace p7zip squashfs-tools")
    run_command("pacman -S --noconfirm file-roller")
    run_command(
        "pacman -S --noconfirm nvidia-dkms nvidia-utils lib32-nvidia-utils nvidia-settings vulkan-icd-loader lib32-vulkan-icd-loader lib32-opencl-nvidia opencl-nvidia libxnvctrl nvidia-prime")
    run_command("mkinitcpio -P")
    run_command("pacman -S --noconfirm xorg-server xorg-server-common xorg-server-xwayland xorg-xinit")
    run_command("pacman -S --noconfirm noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-liberation")
    run_command(
        "pacman -S --noconfirm mesa lib32-mesa vulkan-intel lib32-vulkan-intel vulkan-icd-loader lib32-vulkan-icd-loader")
    run_command("pacman -S --noconfirm intel-ucode polkit ntfs-3g")
    run_command("mkinitcpio -P")
    run_command("grub-mkconfig -o /boot/grub/grub.cfg")
    run_command("pacman -S --noconfirm dialog wpa_supplicant dhcpcd netctl networkmanager network-manager-applet ppp")
    run_command("pacman -S --noconfirm pulseaudio pulseaudio-alsa pulseaudio-jack pavucontrol")
    run_command("pacman -S --noconfirm alsa-lib alsa-utils alsa-firmware alsa-card-profiles alsa-plugins")
    run_command("pacman -S --noconfirm pulseaudio pulseaudio-alsa pulseaudio-jack pavucontrol")
    run_command("pacman -S --noconfirm grub-customizer obs-studio vlc kitty firefox qbittorrent ntp")
    run_command("pacman -S --noconfirm grub-customizer obs-studio vlc kitty firefox qbittorrent ntp")
    run_command("pacman -S --noconfirm xfce4 xfce4-goodies lightdm")
    run_command("pacman -Rscn --noconfirm $(pacman -Qtdq --noconfirm)")


def sysctl():
    run_command("systemctl enable lightdm NetworkManager")


arch_system()
grub()
user()
root_password()
user_password()
add_user_root()
mirrorlist()
aur()
install_pkg()
sysctl()
