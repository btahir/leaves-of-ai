# leaves-of-ai

Generate Walt Whitman Poetry Using Deep Learning.

This project was built using the fastai library (which is in turn built on Pytorch). We used an AWD-LSTM based char-RNN network to generate our text.

All the processing steps are in the jupyter notebook. The other fiels are used to build a web app that generates Walt Whitman poetry on demand. It is hosted using Zeit.

The app can be seen live here: https://leaves-of-ai.now.sh/

Inference takes a few minutes and the text generation is still prone to errors depending on which oot word you use to generate the text.
