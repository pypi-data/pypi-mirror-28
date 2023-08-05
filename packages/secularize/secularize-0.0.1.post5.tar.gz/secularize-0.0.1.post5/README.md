# HolyC-for-Linux
run HolyC on Linux secularly

[![Build Status](http://ec2-54-162-194-49.compute-1.amazonaws.com/job/holyc-for-linux/job/master/badge/icon)](http://ec2-54-162-194-49.compute-1.amazonaws.com/job/holyc-for-linux/job/master/)
[![PyPI version](https://badge.fury.io/py/secularize.svg)](https://badge.fury.io/py/secularize)

#### Disclaimer

This tool is in super-hella-mega alpha stage. If you use this, you will die. Or worse, your current operating system will be replaced with TempleOS. I've only tested this on `3.7-dev`.

#### Install

```
pip install secularize
```

#### run

`secularize examples/test.hc`

turns

`examples/test.hc`
```
F64 *s = 3;

U0 test(I16 a, U8 b, F64 c) {
  Print("hello");
}

F64 pest(I8 d) {
  Print("nothing");
}

Print("%s %s", "hello", "world");
I64 b = 2.000;
```

into

`examples/test.c`
```
void test(short a, unsigned char b, double c)
{
  printf("hello");
}

double pest(char d)
{
  printf("nothing");
}

int main()
{
  double* s = 3;
  printf("%s %s", "hello", "world");
  long b = 2.0;
}
```

#### What's Supported

- print statements
- primitive data types
- basic functions

#### What's Not Supported

Everything else. Deal with it.
