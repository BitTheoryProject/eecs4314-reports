#/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

# todo: build out subsystems more accuratly, FreeBSD is structured with standard naming 
# practices so it's possible to build the subsystems from the existing modules.

# Create a containment file from generated TA and source
# Usage: perl containment.pl <ta_dependency_file> <containment_file_name> <src_path>

# Change this to OS path seperator generated by Understand
my $s = "/";

# Subsystems and their components, todo: accept arg file with this format for flexibility
my %subsystems = (
    "IPC.ss" => {
        "SYSTEMV.ss" => [
            "sys${s}kern${s}sysv_msg.c",
            "sys${s}kern${s}sysv_sem.c",
            "sys${s}kern${s}sysv_shm.c",
            "sys${s}kern${s}sysv_ipc.c",
        ],
        "POSIX.ss" => [
            "sys${s}kern${s}posix4_mib.c",
        ],
        "MQUEUE.ss" => [
            "sys${s}kern${s}uipc_mqueue.c",
        ],
        "KQUEUE.ss" => [
            "sys${s}kern${s}kern_event.c",
            "sys${s}kern${s}kern_kqueue.c",
        ],
        "PTY.ss" => [
            "sys${s}kern${s}tty_pty.c",
            "sys${s}kern${s}tty_tty.c",
        ],
        "SIGNAL.ss" => [
            "sys${s}kern${s}kern_sig.c",
            "sys${s}kern${s}kern_sigqueue.c",
        ],
        "SOCKET.ss" => [
            "sys${s}kern${s}uipc_domain.c",
            "sys${s}kern${s}uipc_mbuf.c",
            "sys${s}kern${s}uipc_socket.c",
            "sys${s}kern${s}uipc_socket2.c",
        ],
        "PROCESS_MANAGEMENT.ss" => [
            "sys${s}kern${s}kern_exit.c",
            "sys${s}kern${s}kern_fork.c",
            "sys${s}kern${s}kern_kthread.c",
            "sys${s}kern${s}kern_resource.c",
            "sys${s}kern${s}kern_sched.c",
            "sys${s}kern${s}kern_synch.c",
        ],
    },
    "KERNEL.ss" => [
        "sys${s}kern${s}sys_pipe.c",
        "sys${s}kern${s}sys_procdesc.c",
        "sys${s}kern${s}sys_process.c",
        "sys${s}kern${s}sys_socket.c",
        "sys${s}kern${s}syscalls.c",
    ],
);

# Parse args
my ($ta_file, $contain_file, $src_path) = @ARGV;

# Read ta_dependency_file dependencies
open(my $fh, '<', $ta_file) or die "Could not open file '$ta_file': $!";
my @dependencies;

while (my $line = <$fh>) {
    chomp $line;
    my ($type, $from, $to) = split(/\s+/, $line);

    # We only care about the concrete files
    if ($type eq "\$INSTANCE") {
        push @dependencies, $from;
    } 
}
close($fh);

# Create the containment file from defined subsystems
# Use glob patterns or substring match (default). 

# Examples:
# src_path/sys/kern/sys* -> match system kernel files
# src_path/sys/kern/uipc* -> match kernel ipc files
open my $cfh, ">", $contain_file or die "Failed to open $contain_file: $!";

# write top level ipc subsystems
foreach my $subsystem (keys %subsystems) {
    print $cfh "contain freebsd $subsystem\n";
    if (ref $subsystems{$subsystem} eq "HASH") {
        foreach my $ipc_subsystem (keys %{$subsystems{$subsystem}}) {
            print $cfh "contain $subsystem $ipc_subsystem\n";
        }
    }
}
print $cfh "\n\n";

foreach my $subsystem (keys %subsystems) {
    if (ref $subsystems{$subsystem} eq "HASH") {
        foreach my $ipc_subsystem (keys %{$subsystems{$subsystem}}) {
            foreach my $component (@{$subsystems{$subsystem}{$ipc_subsystem}}) {
                if (index($component, "*") != -1) {
                        my @files = glob("${src_path}${component}");
                        if (@files) {
                            foreach my $match (@files) {
                                $match = substr $match, length($src_path);
                                print $cfh "contain $ipc_subsystem $match\n";
                            }
                        }
                } else {
                    foreach my $file (@dependencies) {
                        if ($file =~ /$component/i) {
                            print $cfh "contain $ipc_subsystem $file\n";
                        } 
                    }
                }
            }
        }
    } 
    elsif (ref $subsystems{$subsystem} eq "ARRAY") {
        foreach my $component (@{$subsystems{$subsystem}}) {
            if (index($component, "*") != -1) {
                my @files = glob("${src_path}${component}");
                if (@files) {
                    foreach my $match (@files) {
                        $match = substr $match, length($src_path);
                        print $cfh "contain $subsystem $match\n";
                    }
                }
            } else {
                foreach my $file (@dependencies) {
                    if ($file =~ /$component/i) {
                        print $cfh "contain $subsystem $file\n";
                    }
                }
            }
        }
    }
}

close($cfh);