# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np

from training_data import sample_data
from plot import draw_plot

#Code from https://github.com/aadilh/blogs/tree/new/basic-gans/basic-gans/code

#TODO: https://github.com/znxlwm/pytorch-MNIST-CelebA-GAN-DCGAN

#Functions for creating ANN

def generator(input_data,hsize=[16, 16],reuse=False):
    with tf.variable_scope("GAN/Generator",reuse=reuse):
        #1st param - input data, 2nd - layer size, activation - activation function
        h1 = tf.layers.dense(input_data,hsize[0],activation=tf.nn.leaky_relu)
        h2 = tf.layers.dense(h1,hsize[1],activation=tf.nn.leaky_relu)
        out = tf.layers.dense(h2,2)

    return out

def discriminator(input_data,hsize=[16, 16],reuse=False):
    with tf.variable_scope("GAN/Discriminator",reuse=reuse):
        h1 = tf.layers.dense(input_data,hsize[0],activation=tf.nn.leaky_relu)
        h2 = tf.layers.dense(h1,hsize[1],activation=tf.nn.leaky_relu)
        h3 = tf.layers.dense(h2,2)
        out = tf.layers.dense(h3,1)

    return out, h3

def get_loss_functions(real_logits, generator_logits):
    '''Loss functions for discriminator and generator showing how good or bad they work'''
    disc_loss = tf.reduce_mean(
        tf.nn.sigmoid_cross_entropy_with_logits(logits=real_logits,labels=tf.ones_like(real_logits)) + 
        tf.nn.sigmoid_cross_entropy_with_logits(logits=generator_logits,labels=tf.zeros_like(generator_logits))
    )
    gen_loss = tf.reduce_mean(
        tf.nn.sigmoid_cross_entropy_with_logits(logits=generator_logits,labels=tf.ones_like(generator_logits))
    )
    return gen_loss, disc_loss

def set_train_steps(gen_loss, disc_loss):
    '''Generate training steps'''
    gen_rate = 0.001
    disc_rate = 0.001
    gen_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,scope="GAN/Generator")
    disc_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES,scope="GAN/Discriminator")

    gen_step = tf.train.RMSPropOptimizer(learning_rate=gen_rate).minimize(gen_loss,var_list = gen_vars) # G Train step
    disc_step = tf.train.RMSPropOptimizer(learning_rate=disc_rate).minimize(disc_loss,var_list = disc_vars) # D Train step

    return gen_step, disc_step

def train_discriminator(session, r_rep, g_rep, disc_step, disc_loss, real_batch, generator_batch, real_placeholder, generator_placeholder):
    nd_steps = 10
    for _ in range(nd_steps):
        _, dloss = session.run(
            [disc_step, disc_loss], 
            feed_dict={real_placeholder: real_batch, generator_placeholder: generator_batch}
        )
    rrep_dstep, grep_dstep = session.run(
        [r_rep, g_rep], 
        feed_dict={real_placeholder: real_batch, generator_placeholder: generator_batch}
    )
    return dloss, rrep_dstep, grep_dstep

def train_generator(session, r_rep, g_rep, gen_step, gen_loss, real_batch, generator_batch, real_placeholder, generator_placeholder):
    ng_steps = 10
    for _ in range(ng_steps):
        _, gloss = session.run(
            [gen_step, gen_loss], 
            feed_dict={generator_placeholder: generator_batch}
        )

    rrep_gstep, grep_gstep = session.run(
        [r_rep, g_rep], 
        feed_dict={real_placeholder: real_batch, generator_placeholder: generator_batch}
    )
    return gloss, rrep_gstep, grep_gstep

def sample_Z(m, n):
    return np.random.uniform(-1., 1., size=[m, n])

def main():
    real_placeholder = tf.placeholder(tf.float32,[None,2])
    generator_placeholder = tf.placeholder(tf.float32,[None,2])

    generator_result = generator(generator_placeholder)
    
    #logit is probability function
    real_logits, r_rep = discriminator(real_placeholder)
    generator_logits, g_rep = discriminator(generator_result,reuse=True)

    gen_loss, disc_loss = get_loss_functions(real_logits, generator_logits)
    gen_step, disc_step = set_train_steps(gen_loss, disc_loss)

    session = tf.Session() #Start TensorFlow session
    tf.global_variables_initializer().run(session=session)

    batch_size = 100

    x_plot = sample_data(n=batch_size)

    f = open('logs.csv','w')
    f.write('Iteration,Discriminator Loss,Generator Loss\n')

    for i in range(10001):
        real_batch = sample_data(n=batch_size)
        generator_batch = sample_Z(batch_size, 2)

        dloss, rrep_dstep, grep_dstep = train_discriminator(
            session, r_rep, g_rep, disc_step, disc_loss, real_batch, generator_batch, real_placeholder, generator_placeholder
        )

        gloss, rrep_gstep, grep_gstep = train_generator(
            session, r_rep, g_rep, gen_step, gen_loss, real_batch, generator_batch, real_placeholder, generator_placeholder
        )

        if i%10 == 0:
            print ("Iterations: %d\t Discriminator loss: %.4f\t Generator loss: %.4f" % (i,dloss,gloss))
            f.write("%d,%f,%f\n"%(i,dloss,gloss))

        if i%1000 == 0:
            draw_plot(x_plot, session, generator_result, generator_placeholder, generator_batch, i, rrep_dstep, rrep_gstep, grep_dstep, grep_gstep)

    f.close()

#Call main function
main()
