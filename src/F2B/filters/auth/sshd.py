from F2B.filters import Filter


class Sshd(Filter):
    subs = {
        '_daemon': 'sshd',
    }

    failregexes = [
         '^%(__prefix_line)s(?:error: PAM: )?[aA]uthentication (?:failure|error) for .* from <HOST>( via \S+)?\s*$',
         '^%(__prefix_line)s(?:error: PAM: )?User not known to the underlying authentication module for .* from <HOST>\s*$',
         '^%(__prefix_line)sFailed \S+ for .*? from <HOST>(?: port \d*)?(?: ssh\d*)?(: (ruser .*|(\S+ ID \S+ \(serial \d+\) CA )?\S+ %(__md5hex)s(, client user ".*", client host ".*")?))?\s*$',
         '^%(__prefix_line)sROOT LOGIN REFUSED.* FROM <HOST>\s*$',
         '^%(__prefix_line)s[iI](?:llegal|nvalid) user .* from <HOST>\s*$',
         '^%(__prefix_line)sUser .+ from <HOST> not allowed because not listed in AllowUsers\s*$',
         '^%(__prefix_line)sUser .+ from <HOST> not allowed because listed in DenyUsers\s*$',
         '^%(__prefix_line)sUser .+ from <HOST> not allowed because not in any group\s*$',
         '^%(__prefix_line)srefused connect from \S+ \(<HOST>\)\s*$',
         '^%(__prefix_line)sReceived disconnect from <HOST>: 3: \S+: Auth fail$',
         '^%(__prefix_line)sUser .+ from <HOST> not allowed because a group is listed in DenyGroups\s*$',
         '^%(__prefix_line)sUser .+ from <HOST> not allowed because none of user\'s groups are listed in AllowGroups\s*$',
         '^(?P<__prefix>%(__prefix_line)s)User .+ not allowed because account is locked<SKIPLINES>(?P=__prefix)(?:error: )?Received disconnect from <HOST>: 11: .+ \[preauth\]$',
         '^(?P<__prefix>%(__prefix_line)s)Disconnecting: Too many authentication failures for .+? \[preauth\]<SKIPLINES>(?P=__prefix)(?:error: )?Connection closed by <HOST> \[preauth\]$',
         '^(?P<__prefix>%(__prefix_line)s)Connection from <HOST> port \d+(?: on \S+ port \d+)?<SKIPLINES>(?P=__prefix)Disconnecting: Too many authentication failures for .+? \[preauth\]$',
         '^%(__prefix_line)spam_unix\(sshd:auth\):\s+authentication failure;\s*logname=\S*\s*uid=\d*\s*euid=\d*\s*tty=\S*\s*ruser=\S*\s*rhost=<HOST>\s.*$',
    ]
