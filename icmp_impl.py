import os
from MySQL import *
from svmutil import *

db = MySQL()

print "please enter the size of train set:"
train_count = int(input())

print "please enter the size of test set:"
test_count = int(input())


def get_data(count):
    sql = "truncate table kw_icmp"
    db.execute(sql)
    for i in range(0, count):
        print "getting data: ", (i + 1), "of", count
        os.system("python icmp.py > /dev/null 2>&1")


def sql2file(file_name):
    sql = "select * from kw_icmp"
    rel = db.query(sql)

    f = open(file_name, "wb")
    f2 = open(file_name + '.txt', "wb")
    count = 0;
    for v in rel:
        dt1 = v[3] - v[2]
        dt2 = v[5] - v[4]
        f.write("1 1:" + str(dt1) + "\n")
        f.write("0 1:" + str(dt2) + "\n")
        f2.write("1 " + str(dt1) + "\n")
        f2.write("0 " + str(dt2) + "\n")
        count += 2
    f.close()
    f2.close()
    return count


print "getting train data:"
get_data(train_count)

print "transfer train data:"
data_count = sql2file("train.in")

print "training:"
y, x = svm_read_problem('train.in')
m = svm_train(y[:data_count], x[:data_count], '-s 0 -c 10 -g 0.7')

print "getting test data:"
get_data(test_count)

print "transfer test data:"
data_count = sql2file("test.in")

print "predict:"
y2, x2 = svm_read_problem('test.in')
p_label, p_acc, p_val = svm_predict(y2[:data_count], x2[:data_count], m)
