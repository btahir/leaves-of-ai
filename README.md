# Leaves of AI

Generate Walt Whitman Poetry Using Deep Learning.

Project inspired by the NaNoGenMo series: https://github.com/NaNoGenMo/2018

The generated novel is attached in the whitman_novel.md file.

This project was built using the fastai library (which is in turn built on Pytorch). We used an AWD-LSTM based char-RNN network to generate our text.

All the processing steps are in the jupyter notebook. The other fields are used to build a web app that generates Walt Whitman poetry on demand. It is hosted using Zeit.

The app can be seen live here: https://leaves-of-ai.now.sh/

![alt text](https://github.com/btahir/leaves-of-ai/blob/master/app-snap.jpg)

Inference takes a few minutes and the text generation is still prone to errors depending on which root word you use to generate the text. 

There is room for improvement by using better prediction methods such as beam search. Hopefully - I will be implementing that soon.
