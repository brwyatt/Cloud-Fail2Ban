from F2B.filters import Filter


class Sshd(Filter):
    subs = {
        '_daemon': 'sshd',
    }

    failregexes = [
        '^%(__prefix_line)s(?:error: PAM: )?[aA]uthentication (?:failure|error) for .* from %(host)s( via \S+)?\s*$',
        '^%(__prefix_line)s(?:error: PAM: )?User not known to the underlying authentication module for .* from %(host)s\s*$',
        '^%(__prefix_line)sFailed \S+ for .*? from %(host)s(?: port \d*)?(?: ssh\d*)?(: (ruser .*|(\S+ ID \S+ \(serial \d+\) CA )?\S+ %(__md5hex)s(, client user ".*", client host ".*")?))?\s*$',
        '^%(__prefix_line)sROOT LOGIN REFUSED.* FROM %(host)s\s*$',
        '^%(__prefix_line)s[iI](?:llegal|nvalid) user .* from %(host)s(?: port \d+)?\s*$',
        '^%(__prefix_line)sUser .+ from %(host)s not allowed because not listed in AllowUsers\s*$',
        '^%(__prefix_line)sUser .+ from %(host)s not allowed because listed in DenyUsers\s*$',
        '^%(__prefix_line)sUser .+ from %(host)s not allowed because not in any group\s*$',
        '^%(__prefix_line)srefused connect from \S+ \(%(host)s\)\s*$',
        '^%(__prefix_line)sReceived disconnect from %(host)s: 3: \S+: Auth fail$',
        '^%(__prefix_line)sUser .+ from %(host)s not allowed because a group is listed in DenyGroups\s*$',
        '^%(__prefix_line)sUser .+ from %(host)s not allowed because none of user\'s groups are listed in AllowGroups\s*$',
        '^%(__prefix_line)spam_unix\(sshd:auth\):\s+authentication failure;\s*logname=\S*\s*uid=\d*\s*euid=\d*\s*tty=\S*\s*ruser=\S*\s*rhost=%(host)s\s.*$',
    ]
