package main

import (
	"math/rand"
	"time"
)

//Install Tensorflow https://www.tensorflow.org/install/lang_go

// icon:
// https://neuralnet.info/2017/09/16/%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B4%D0%B5%D0%B2%D1%83%D1%88%D0%B5%D0%BA-%D0%B2-%D1%81%D1%82%D0%B8%D0%BB%D0%B5-%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5/
// https://make.girls.moe/#/

//https://nplus1.ru/news/2018/01/19/attn-gan
//https://ru.wikipedia.org/wiki/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D0%BE-%D1%81%D0%BE%D1%81%D1%82%D1%8F%D0%B7%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D1%81%D0%B5%D1%82%D1%8C
//http://bamos.github.io/2016/08/09/deep-completion/
//http://robocraft.ru/blog/machinelearning/3693.html
//https://vbystricky.github.io/2017/09/gan.html

//TODO: https://blog.paperspace.com/implementing-gans-in-tensorflow/
//https://pgaleone.eu/tensorflow/go/2017/05/29/understanding-tensorflow-using-go/
//https://github.com/uclaacmai/Generative-Adversarial-Network-Tutorial
//https://github.com/aymericdamien/TensorFlow-Examples
//https://github.com/MorvanZhou/Tensorflow-Tutorial
//https://towardsdatascience.com/implementing-a-generative-adversarial-network-gan-dcgan-to-draw-human-faces-8291616904a

func main() {
	rand.Seed(time.Now().UTC().UnixNano()) //Init random generator
	var path string
	path = "image.png"
	draw(path)
	tfTest()
}
