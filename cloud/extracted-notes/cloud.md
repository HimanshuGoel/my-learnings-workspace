# Extracted Notes - Cloud

## Virtual Machine

- The early 2000s was the era of the virtual machine. We are now firmly in the container era. They have much smaller footprint, quicker to download and a lot less resource needed to run them.

## Container

- Container image – a file system bundle containing all files, packages, dependencies, and kernel needed to run a service. To the host this is a single process. Container run isolated from other containers so software and dependencies installed on one container do not affect other containers. It has small footprint because there is no complete operating system with a container making them are much less resource hungry than running virtual machines.

## Linux

Linux represents collaboration, innovation, and technological freedom. The story of Linux begins with UNIX, the operating system that inspired Linux Torvalds to create a free and open-source alternative. Its core philosophy - FOSS (Free and Open Source Software). Unlike proprietary systems, Linux gives users control over their computing environment , making it an attractive choice for individuals and organizations alike.

One of Linux's defining aspects it its ecosystem, which includes various distribution (distros) tailored for different use cases. Debian, Red Hat, and Arch Linux each offer unique approaches to stability, customization and software management.

Linux provides users with a choice of desktop environments (GNOME, KDE, XFCE) and lightweight window managers, catering to different performance needs.

Linux follows modular design, divided into user space and kernel space. The kernel manages hardware interactions and system calls, while user space includes components like bootloader, init system and shell. The architecture ensures stability, security and flexibility making Linux idea for critical computing tasks.

The linux shell is a powerful interface for navigating managing files, and automating tasks. Scheduled operations are managed with cron jobs and systemd timers.

Linux adheres to the Filesystem Hierarchy Standard (FHS), organizing directories like /bin, /etc, and /var for system integrity.

The UNIX operating system, developed in the late 1960 at AT&T’s Bell Labs, introduced key computing principles: multi-user environments, hierarchical file structures, and a modular design. UNIX’s effectiveness made it highly sought after, but its licensing soon restricted access, prompting a counter-movement.

Enter Richard Stallman and the GNU project. In the 1980s. Stallman envisioned a completely free and open UNIX-like system. His Free Software Foundation (FSF) spearheaded this cause, laying the groundwork for what would become the GNU operating system. However, one crucial element remained missing – a kernel.

That missing piece arrived in 1991 when Linux Torvalds, a Finnish computer science student, developed the Linux kernel. By merging the GNU software with Torvalds’ kernel, a fully functional, free UNIX-like operating system emerged. Linux was born – not as a singular entity, but as a decentralized ecosystem powered by collaboration.

Linux vs. other operating systems – Linux differs fundamentally from proprietary OS like windows and macOS. Unlike their closed-source, monolithic structures, Linux is modular and customizable. It doesn’t dictate a single UX, instead it offers a vast array of distributions, interfaces and configurations.

With its permission-based architecture and extensive community oversight Linux is inherently less susceptible to malware. Additionally, performance optimization makes Linux a go-to choice for high permeance computing, form serves to embedded systems. Windows, offers plug-and-play simplicity, Linux often demands technical proficiency.

The linux ecosystem –

Debian-based (Ubuntu, Linux Mint) – user friendly, stability and ease of use.

Red Hat-based (Fedora, CentOS, RHEL) – popular in enterprise environments, reliability, security and support.

Arch-based (Arch Linux, Manjaro) – Geared towards experience users, minimalist, rolling-release system with complete customization.

Linux desktop environments (Des) – GNOME (Modern, minimalistic and touch-friendly), KDE Plasma (highly customizable), XFCE & LXQT (ideal for older hardware)

Linux kernel ensures secure interactions between software and hardware.

User space vs. Kernel space – this separation enhances stability. Even if a user application crashes, it won’t take down the entire system – a stark contrast to some proprietary OS where crashes can trigger widespread failures.

Foundation components – bootloader, Init System, Daemons (Background services), Shell (user’s gateway to the system, command like shells like Bash, Zsh and Fish provide powerful control over the OS, far beyond what graphical interfaces offer).

Partitioning layouts - /boot (contains kernel and bootloader files), /(Root) (houses the core system files), /home (user data and configurations), Swap (serving as virtual memory).

Installation options – Dual-booting (allows to run Linux alongside Windows or macOS on the same machine, this setup is beneficial for those who need access to multiple operating systems for different tasks), Virtualization (enables to run Linux in a virtualized environment without modifying their primary OS, useful for testing, development or running multiple OSes simultaneously)

BASH (Bourne Again Shell), Zsh shell, Fish shell (syntax highlighting).

Navigating the filesystem - pwd, ls, cd

File operations - cp, mv, rm, touch

Text manipulation - grep, sed, awk, cut

Variables, conditionals, loops - name="alice", if [true] then, for do done

Cron jobs can be used for scheduling recurring tasks, systemd timers alternative to cron for scheduling. By leveraging shell scripting, users can automate complex workflows, reducing manual intervention and increasing efficiency.

Filesystem structure - /bin(stores essential command binaries and necessary for basic system functionality), /etc (contains configuration files for system and application settings), /var (house variable data such as logs, caches, and spool files), /usr (holds secondary applications, libraries and documentation), /dev (represents device files, allowing user-space applications to interact with hardware components like disks and peripherals)

Linux treats everything as a file, including devices and inter process communication system.

Access control lists (ACLs) offer fine-grained permission control beyond the standard user/group/others model. ACLs allow administrators to define access rights for multiple users and groups beyond the standard three-category model.

Symbolic vs. hard links – symbolic links are useful for creating shortcuts or organizing files in different locations without duplication. Hard links provide redundancy and prevent accidental data loss by maintaining multiple references to the same node.

Filesystem types – ext4, Btrfs, XFS and ZFS. XFS is ideal for enterprise applications requiring high throughput, while ZFS is preferred for data integrity and redundancy.

IP addressing – every device connected to a network requires an IP address, which can either be assigned statically or dynamically. While static addressing offers control and predictability, DHCP simplifies management, especially in larger network where manually assigning addresses would be cumbersome.

Static IP addressing is often used for servers, printers, and other critical devices that require a fixed network identity. DHCP, on the other hand, is managed by a DHCP server, dynamically assigning IP addresses to devices as they connect to the network.

SSH (secure shell enables) remote access to Linux systems. Key-based authentication enhances security by eliminating the need for password-based logins.

Kernel is a core component that manages system resources and hardware communication.

Containers like Docker or Podman provide lightweight, portable environments for running applications consistently across different platforms.

Orchestration like Kubernetes manages containerized applications at scale like deploying applications, scaling and load balancing, self-healing and fault tolerance.

The shift towards zero-trust security models, which assume that threats could be both external and internal, has led to the development of tools and frameworks within Linux to enforce strict access controls and continuous verification.

The Linux foundation, along with key contributors like Red Hat Canonical and SUSE, plays a pivotal role in shaping Linux’s development. These organizations provide financial backing, infrastructure and strategic direction for critical projects.

Linux faces challenges including hardware driver support, fragmentation across distributions and maintaining ease of use for non-technical users.
