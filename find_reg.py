import datetime
import subprocess
import os

keywords = 'partial keywords that are emitted in case of error'
start_date = '2017-10-02'   # any known date when code was compiling OK
end_date = '2018-01-18'     # any known date when code was not compiling OK
travis = True               # is this going to be run on Travis CI?

# local bin directory of current user
init_path = '/home/travis/.cargo/bin/'
# <filename>.rs to run (here, 'test.rs')
cmd = [init_path + 'rustc', os.path.abspath('test.rs')]
# toolchain to test compile on
toolchain_type = 'nightly'

last_date = start_date


def middle_date(start_date, end_date):
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    mid = start + (end - start) / 2
    return str(mid.date())


def output_has_keywords(cmd, capture):
    output = subprocess.run(cmd,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    stdout = output.stdout.decode('utf-8')
    stderr = output.stderr.decode('utf-8')
    print(stdout.replace('\\n', '\n'), stderr.replace('\\n', '\n'))

    return capture in stderr or capture in stdout


def set_default_toolchain(toolchain):
    cmd = [init_path + 'rustup', 'default', toolchain]
    output = subprocess.run(cmd,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    subprocess.run([init_path + 'rustc', '-vV'])
    return output.stdout


mid_date = middle_date(start_date, end_date)
toolchain = '{0}-{1}'.format(toolchain_type, mid_date)

if travis:
    subprocess.run(['bash', 'rustup.sh', '-y', '--default-toolchain', toolchain])
else:
    set_default_toolchain(toolchain)


while not last_date == mid_date:
    last_date = mid_date
    if output_has_keywords(cmd, keywords):
        end_date = mid_date
    else:
        start_date = mid_date

    mid_date = middle_date(start_date, end_date)
    toolchain = '{0}-{1}'.format(toolchain_type, mid_date)

    print('Setting defaults: ' + toolchain)
    set_default_toolchain(toolchain)

print('\nLast working toolchain: ' + toolchain)
