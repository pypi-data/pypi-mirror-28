# JMaster

[中文文档](http://palayutm.cn/2017/12/24/JMaster/)

Parse CodeForces contests and auto test sample.

## Install

### Using pip
``` shell
$ pip3 install JMaster
```

### Manual
``` shell
$ git clone https://github.com/palayutm/JMaster.git
$ cd JMaster
$ python3 setup.py install
```

## Usage
### View contest info
``` shell
$ JMaster contest
```

![](img/contest.png)

### Parse contest
#### Parse normal contests
``` shell
$ JMaster parse CONTEST_ID
```

![](img/parse-contest.png)

#### Parse gym contests
``` shell
$ JMaster parse --gym CONTEST_ID
```

![](img/parse-gym.png)

### Test sample
``` shell
$ JMaster test CPP_FILE [SAMPLE_FILE]
```

sample code (a.cc)
``` c++
#include <bits/stdc++.h>

using namespace std;

int main(int argc, char *argv[]) {
  int a, b;
  cin >> a >> b;
  assert(a > b);    // test runtime error
  cout << a + b << endl;
  return 0;
}
```
test case (a.sample)
```
-- normal test
2 1
--
3

-- runtime error test
1 1
--
2

-- wrong answer test
2 1
--
4
```

![](img/test-problem.png)

### Further Usage
```shell
$ JMaster --help
```

## Suggestions
put
```shell
alias jt="JMaster test"
alias jp="JMaster parse"
alias jpp="JMaster parse --problem"
```
to your `$HOME/.bashrc`
