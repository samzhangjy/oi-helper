# OI Helper

Yet another helper for **Olympiad in Informatics**!

## Usage

Clone this repo and run the following command:

```bash
$ python oi-helper.py
```

Or you can download the latest stable release in the right panel.

### Problem parsing

OI-Helper will crawl for the specified problem and extract limitations and test samples. To do this, run:

```bash
$ oi-helper parse P1001  # https://www.luogu.com.cn/problem/P1001
```

This will also generate a blank template program called `P1001.cpp` in current folder if not exist.

### Running your program

```bash
$ oi-helper run ./P1001.cpp
```

The above command will first look for sample cases parsed before in its database and run them. Then OI Helper will walk through the current directory and look for patterns such as `P1001-1.in` or `P1001-1.out`.

Example output below.

```
Running sample 0 ...
  AC / 0.02s / 604.0K
Running sample 1 ...
  AC / 0.01s / 476.0K
Discovered 2 local testcases in /Volumes/Data/Develop/Python/OI-Helper .
Running testcase 1 ...
  AC / 0.01s / 604.0K
Running testcase 2 ...
  AC / 0.01s / 604.0K
```

### Submitting to OJ

Before submitting, you'll need to login first:

```bash
$ oi-helper login
```

This will ask for your credentials and a Captcha.

To submit program to a problem, run:

```bash
$ oi-helper submit ./P1001.cpp
```

This will automatically submit your program to online judge. Example output below.

```
Solution submitted with record ID 84279206.
Compiling...
Compiled successfully.
Subtask 1: AC / 0.03s / 808.0K
  #0: AC / 0.003s / 664.1K / ok accepted
  #8: AC / 0.003s / 668.0K / ok accepted
  #3: AC / 0.003s / 664.1K / ok accepted
  #6: AC / 0.003s / 668.0K / ok accepted
  #2: AC / 0.003s / 668.0K / ok accepted
  #5: AC / 0.003s / 789.1K / ok accepted
  #1: AC / 0.003s / 664.1K / ok accepted
  #4: AC / 0.003s / 668.0K / ok accepted
  #7: AC / 0.003s / 742.2K / ok accepted
  #9: AC / 0.003s / 668.0K / ok accepted
Status: Accepted / 100pts / 0.03s / 808.0K
```

## Documentation

Use `oi-helper [COMMAND] --help` to see the manual.

## Contributing

Contributions are highly welcomed!

## Licensing

OI Helper is published under the MIT license. See `LICENSE` for details.
