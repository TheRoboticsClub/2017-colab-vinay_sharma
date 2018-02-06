import tensorflow as tf
import time
import read_data
import numpy as np
import cv2
#import matplotlib.pyplot as plt

def conv2d(x, W):
  """conv2d returns a 2d convolution layer with full stride."""
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
  """max_pool_2x2 downsamples a feature map by 2X."""
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
  """weight_variable generates a weight variable of a given shape."""
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def bias_variable(shape):
  """bias_variable generates a bias variable of a given shape."""
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


mygraph = tf.Graph()

with mygraph.as_default():


    def deepnn(x):

        #x_image = tf.reshape(x, [-1, 28, 28, 1])

        W_conv1 = tf.Variable(tf.truncated_normal(shape=[8, 4, 3, 16], stddev=0.1))
        b_conv1 = tf.Variable(tf.constant(0.1, shape=[16]))
        h_conv1 = tf.nn.relu(conv2d(x, W_conv1) + b_conv1)

        h_pool1 = max_pool_2x2(h_conv1)

        W_conv2 = weight_variable([8, 4, 16, 32])
        b_conv2 = bias_variable([32])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

        h_pool2 = max_pool_2x2(h_conv2)

        W_fc1 = weight_variable([16 * 32 * 32, 1024])
        b_fc1 = bias_variable([1024])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 16*32*32])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

        keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        W_fc2 = weight_variable([1024, 2])
        b_fc2 = bias_variable([2])

        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

        return y_conv, keep_prob





# Import data

    X, Y, X_test, Y_test = read_data.read_dataset();

    l_data = len(X)
    print len(X), len(Y)
    print X[0].shape, Y[0]
    for i in range(0, 20):
        print Y[i]
        cv2.imshow("person", X[i])
        cv2.waitKey(0)

    print X[0]
    print X[1].shape, Y[1]
    print X[2].shape, Y[2]
    print len(X_test), len(Y_test)
    print X_test[0].shape, Y_test[0]
    print X_test[1].shape, Y_test[1]
    print X_test[2].shape, Y_test[2]
    #mnist = input_data.read_data_sets("mnist/", one_hot=True)

    # Create the model
    x = tf.placeholder(tf.float32, [None, 128, 64, 3])
    print x.shape
    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 2])

    # Build the graph for the deep net
    y_conv, keep_prob = deepnn(x)

    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv)

    cross_entropy = tf.reduce_mean(cross_entropy)

    train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
    true_negatives = tf.count_nonzero(tf.greater(tf.argmax(y_conv, 1), tf.argmax(y_, 1)))
    false_positives = tf.count_nonzero(tf.less(tf.argmax(y_conv, 1), tf.argmax(y_, 1)))
    #correct_prediction = tf.cast(correct_prediction, tf.float32)
    #accuracy = tf.reduce_mean(correct_prediction)
    saver = tf.train.Saver()

start_time = time.time()

batch_size = 50

with tf.Session(graph=mygraph) as sess:
    sess.run(tf.global_variables_initializer())

    #plt.ion()

    for i in range(5000):
      batch_data = X[(i*batch_size)%(l_data - batch_size) : (i*batch_size)%(l_data - batch_size) + 50]
      batch_labels = Y[(i*batch_size)%(l_data - batch_size) : (i*batch_size)%(l_data - batch_size) + 50]
      #batch = mnist.train.next_batch(batch_size)
      if i % 2 == 0:
        #train_accuracy = accuracy.eval(feed_dict={x: batch_data, y_: batch_labels, keep_prob: 1.0})

        _, loss, pred, lbl = sess.run([train_step, cross_entropy, y_conv, y_], feed_dict={x: batch_data, y_: batch_labels, keep_prob: 1.0})
        print i, loss

        #plt.figure(1)
        #plt.scatter(i, loss)
        #plt.figure(2)
        #plt.scatter(step, 100.0 - acc_v)
        #plt.pause(0.05)

    print true_negatives.eval(feed_dict={x: X_test, y_: Y_test, keep_prob: 1.0})
    print false_positives.eval(feed_dict={x: X_test, y_: Y_test, keep_prob: 1.0})

    save_path = saver.save(sess, "model/conv_net.ckpt")
    print("Model saved in file %s" % save_path)


print "Time Taken" + str(time.time() - start_time)
