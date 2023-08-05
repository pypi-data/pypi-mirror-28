import threading
import click
import json
import requests
import textwrap
import time
import os
import subprocess
from subprocess import PIPE
from colorclass import Color
from terminaltables import GithubFlavoredMarkdownTable
from bs4 import BeautifulSoup


@click.group()
def cli():
    pass


@click.command(help="Print recent contests")
@click.option(
    '-n', '--number', default=10, type=int, help='Print N recent contests')
@click.option('-a', '--all', is_flag=True, help='Print ALL contests')
def contest(number, all):
    number = max(number, 1)
    data = json.loads(
        requests.get("http://codeforces.com/api/contest.list").text)
    contests = data['result'][:min(len(data['result']),
                                   number)] if not all else data['result']
    table_data = [['ID', 'Contest Name', 'Status']]
    for x in contests:
        idx = str(x['id'])
        name = '\n'.join(textwrap.wrap(x['name'], 50))
        data = [
            Color('{autogreen}' + idx + '{/autogreen}'), name,
            Color('{autored}' + x['phase'] + '{/autored}')
            if x['phase'] != 'BEFORE' else Color('{autogreen}' + time.strftime(
                '%Y-%m-%d %H-%M-%S %Z', time.localtime(x['startTimeSeconds']))
                                                 + '{/autogreen}')
        ]
        table_data.append(data)
    print(GithubFlavoredMarkdownTable(table_data).table)


@click.command(help='Parse contest by CONTEST_ID')
@click.argument('contest_id')
@click.option('--gym/--no-gym', default=False, help='gym contest')
@click.option('--problem/--no-problem', default=False, help='only problem')
def parse(contest_id, gym, problem):
    if gym:
        url = 'http://codeforces.com/gym/%s' % contest_id
    elif problem:
        name = ''.join(contest_id.split('/')[-2:])
        parseProblem(contest_id, name, '')
        return
    else:
        url = 'http://codeforces.com/contest/%s' % contest_id
    res = requests.get(url)
    if res.url != url:
        raise Exception('Invaild Contest Id')
    page = BeautifulSoup(res.text, 'lxml')
    contest_name = page.find(
        'table', attrs={
            'class': 'rtable'
        }).find('tr').find('a').text
    contest_name = contest_name.replace('#', '')
    if gym:
        contest_name = "GYM " + contest_name
    pre1 = time.strftime("%Y-%m", time.localtime())
    if not os.path.exists(pre1):
        os.mkdir(pre1)
    prefix = os.path.join(
        pre1,
        time.strftime("%Y-%m-%d", time.localtime()) + " - " + contest_name)
    if not os.path.exists(prefix):
        os.mkdir(prefix)
    tr = [
        _ for _ in page.find('table', attrs={
            'class': 'problems'
        }).findAll('tr')
    ]
    threads = []
    for i in range(1, len(tr)):
        td = [_ for _ in tr[i].findAll('td')]
        idx = td[0].text.strip()
        name = td[1].find('a').text.strip()
        threads.append(
            threading.Thread(
                target=parseProblem,
                args=(url + '/problem/' + idx, idx + '-' + name, prefix)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def parseProblem(url, name, prefix):
    print(url, name, prefix)
    p1 = BeautifulSoup(requests.get(url).text, 'lxml')
    test_case = [
        _.prettify(formatter=None).strip()[5:-6].replace('<br/>', '\n')
        for _ in p1.findAll('div', attrs={
            'class': 'sample-test'
        })[0].findAll('pre')
    ]
    open(os.path.join(prefix, name + '.cc'), 'a').close()
    with open(os.path.join(prefix, name + '.sample'), 'w') as fp:
        for i in range(0, len(test_case), 2):
            fp.write('-- Example %i\n' % (i / 2))
            fp.write(test_case[i])
            fp.write('--\n')
            fp.write(test_case[i + 1] + '\n')


@click.command(help='Test code with all sample files')
@click.argument('code', type=click.Path(exists=True))
@click.argument('samples', type=click.Path(exists=True), nargs=-1)
def test(code, samples):
    CXX_FLAGS = '-O2 -std=c++14'
    prefix = os.path.splitext(code)[0]
    compile_cmd = ['g++', code, '-o', prefix]
    compile_cmd.extend(CXX_FLAGS.split())
    if subprocess.Popen(compile_cmd).wait() != 0:
        return
    if len(samples) == 0:
        samples = (os.path.splitext(code)[0] + '.sample', )
    sta, sample_in, sample_out = 0, [], []
    cas_num = 0
    result = []
    for sample in samples:
        with open(sample, 'r') as fp:
            for line in fp.readlines()[1:]:
                if line.startswith('--'):
                    if not sta:
                        sta = True
                    else:
                        result.append(
                            testCase(prefix, '\n'.join(sample_in).strip(),
                                     '\n'.join(sample_out).strip(), cas_num))
                        cas_num += 1
                        sample_in, sample_out = [], []
                        sta = False
                else:
                    sample_in.append(
                        line.strip()) if not sta else sample_out.append(
                            line.strip())
            result.append(
                testCase(prefix, '\n'.join(sample_in).strip(),
                         '\n'.join(sample_out).strip(), cas_num))
            cas_num += 1
            sample_in, sample_out = [], []
    print('=' * 80)
    for i in range(len(result)):
        print('Test #%i: ' % i +
              (Color('{autogreen}PASSED{/autogreen}')
               if result[i] else Color('{autored}FAILED{/autored}')))


def testCase(prefix, sample_in, sample_out, cas_num):
    print('Test #%i:' % cas_num)
    print('input:')
    print(sample_in)
    print('\nExpected output:')
    print(sample_out)
    print('\nExecution result:')
    t = subprocess.Popen(['./' + prefix], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout_data, stderr_data = t.communicate(
        input=bytes(sample_in, encoding='utf-8'))
    stdout_data = str(stdout_data, encoding='utf-8').strip()
    stderr_data = str(stderr_data, encoding='utf-8').strip()
    stdout_data = '\n'.join([_.strip() for _ in stdout_data.split('\n')])
    print(stdout_data)
    print('\nStderr output:')
    print(stderr_data)
    print('Verdict: ', 'PASSED' if stdout_data == sample_out else 'FAILED')
    print('-' * 80)
    return stdout_data == sample_out


def main():
    cli.add_command(contest)
    cli.add_command(parse)
    cli.add_command(test)
    cli()


if __name__ == '__main__':
    main()
