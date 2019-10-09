from cloud_f2b.filters import Filter


class Postfix(Filter):
    subs = {
        '_daemon': 'postfix/\S+',
    }

    failregexes = [
        '^%(__prefix_line)sNOQUEUE: reject: RCPT from \S+\[%(host)s\]: 450 4\.7\.1 : Helo command rejected: Host not found; from=<> to=<> proto=ESMTP helo= *$',
        '^%(__prefix_line)sNOQUEUE: reject: RCPT from \S+\[%(host)s\]: 454 4\.7\.1\.*',
        '^%(__prefix_line)sNOQUEUE: reject: RCPT from \S+\[%(host)s\]: 554 5\.7\.1 .*$',
        '^%(__prefix_line)s\S*: reject: (VRFY|RCPT) from \S+\[%(host)s\]: 550 5\.1\.1 .*$',
        '^%(__prefix_line)simproper command pipelining after \S+ from [^[]*\[%(host)s\]:?$',
        '^%(__prefix_line)stoo many errors after RCPT from \S+\[%(host)s\]$',
        '^%(__prefix_line)swarning: \S+\[%(host)s\]: .+ authentication failed:.*$',
    ]
