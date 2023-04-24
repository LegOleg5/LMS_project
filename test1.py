from subprocess import Popen, PIPE


def test_system(filename, true_answers, tests):
    for i in range(len(tests)):
        test = tests[i]
        t = ''
        for el in test:
            t += (str(el) + '\n')
        print(t)

        proc = Popen(f'{filename}', shell=True, stdout=PIPE, stdin=PIPE)
        print(1)
        outs, errs = proc.communicate(input=bytes(t, 'utf-8'))
        answer = (int(str(outs, 'utf-8').rstrip()),)
        print(answer, true_answers[i])
        if answer == true_answers[i]:
            print('ok')


filename1 = 'test2.py'
true_answers1 = [(3,), (8,), (10,)]
tests1 = [(1, 2), (3, 5), (9, 1)]
test_system(filename1, true_answers1, tests1)
