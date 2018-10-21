package main

import (
	"fmt"
	"os"

	tf "github.com/tensorflow/tensorflow/tensorflow/go"
	"github.com/tensorflow/tensorflow/tensorflow/go/op"
)

func tfTest() {
	os.Setenv("TF_CPP_MIN_LOG_LEVEL", "2") //Disable log: Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 FMA
	// Construct a graph with an operation that produces a string constant.
	s := op.NewScope()
	c := op.Const(s, "Hello from TensorFlow version "+tf.Version())
	graph, err := s.Finalize()
	if err != nil {
		panic(err)
	}

	// Execute the graph in a session.
	sess, err := tf.NewSession(graph, nil)
	if err != nil {
		panic(err)
	}
	output, err := sess.Run(nil, []tf.Output{c}, nil)
	if err != nil {
		panic(err)
	}
	fmt.Println(output[0].Value())
}

// func generator(Z,hsize=[16, 16],reuse=False):
//     with tf.variable_scope("GAN/Generator",reuse=reuse):
//         h1 = tf.layers.dense(Z,hsize[0],activation=tf.nn.leaky_relu)
//         h2 = tf.layers.dense(h1,hsize[1],activation=tf.nn.leaky_relu)
//         out = tf.layers.dense(h2,2)

// 	return out