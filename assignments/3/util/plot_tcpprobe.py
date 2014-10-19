from helper import *
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', dest="port", default='5001')
parser.add_argument('-f', dest="files", nargs='+', required=True)
parser.add_argument('-o', '--out', dest="out", default=None)
parser.add_argument('-H', '--histogram', dest="histogram",
                    help="Plot histogram of sum(cwnd_i)",
                    action="store_true",
                    default=False)

args = parser.parse_args()

def first(lst):
    return map(lambda e: e[0], lst)

def second(lst):
    return map(lambda e: e[1], lst)

def label_for_port(port):
    # Find the IP Address
    d = os.path.dirname(args.files[0])
    f = 'iperf_server.txt'
    p = os.path.join(d, f)
    fd = open(p, 'r')
    raw = fd.read()
    fd.close()
    ip = None
    for line in raw.split('\n'):
        if not len(line): continue
        if not line.endswith('%d'%port): continue
        ip = line.split()[-3]
        break

    # find the host name
    rxp = '^iperf_.*.txt$'
    rcm = re.compile(rxp)
    host = None
    for f in os.listdir(d):
        if not rcm.match(f): continue
        if 'iperf_server.txt' == f: continue
        # XXX: redo using regex matching
        fd = open(os.path.join(d, f), 'r')
        raw = fd.read()
        fd.close()
        if '%s,%d'%(ip, port) in raw:
            host = f[6:-4]
            break

    return host

"""
Sample line:
2.221032535 10.0.0.2:39815 10.0.0.1:5001 32 0x1a2a710c 0x1a2a387c 11 2147483647 14592 85
"""
def parse_file(f):
    times = defaultdict(list)
    cwnd = defaultdict(list)
    srtt = []
    for l in open(f).xreadlines():
        fields = l.strip().split(' ')
        if len(fields) != 10:
            break
        if fields[2].split(':')[1] != args.port:
            continue
        sport = int(fields[1].split(':')[1])
        times[sport].append(float(fields[0]))

        c = int(fields[6])
        cwnd[sport].append(c * 1480 / 1024.0)
        srtt.append(int(fields[-1]))
    return times, cwnd

added = defaultdict(int)
events = []

def plot_cwnds(ax):
    global events
    for f in args.files:
        times, cwnds = parse_file(f)
        for port in sorted(cwnds.keys()):
            t = times[port]
            cwnd = cwnds[port]

            events += zip(t, [port]*len(t), cwnd)
            ax.plot(t, cwnd, label=label_for_port(port))

    events.sort()
total_cwnd = 0
cwnd_time = []

min_total_cwnd = 10**10
max_total_cwnd = 0
totalcwnds = []

m.rc('figure', figsize=(16, 6))
fig = plt.figure()
plots = 1
if args.histogram:
    plots = 2

axPlot = fig.add_subplot(1, plots, 1)
plot_cwnds(axPlot)

for (t,p,c) in events:
    if added[p]:
        total_cwnd -= added[p]
    total_cwnd += c
    cwnd_time.append((t, total_cwnd))
    added[p] = c
    totalcwnds.append(total_cwnd)

axPlot.plot(first(cwnd_time), second(cwnd_time), lw=2, label="$\sum_i W_i$")
axPlot.grid(True)
axPlot.legend()
axPlot.set_xlabel("seconds")
axPlot.set_ylabel("cwnd KB")
axPlot.set_title("TCP congestion window (cwnd) timeseries")

if args.histogram:
    axHist = fig.add_subplot(1, 2, 2)
    n, bins, patches = axHist.hist(totalcwnds, 50, normed=1, facecolor='green', alpha=0.75)

    axHist.set_xlabel("bins (KB)")
    axHist.set_ylabel("Fraction")
    axHist.set_title("Histogram of sum(cwnd_i)")

if args.out:
    print 'saving to', args.out
    plt.savefig(args.out)
else:
    plt.show()
