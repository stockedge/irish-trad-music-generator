# irish-trad-music-generator

Stacked LSTMを使ってケルト民族音楽のメロディを自動生成する。

元ネタはこの記事。
[The Infinite Irish Trad Session](https://highnoongmt.wordpress.com/2015/08/07/the-infinite-irish-trad-session/)
この記事ではRNNを使っていたので、LSTMを代わりに使ったらどうなるかやってみた。

こちらも同様にRNNだけど参考になる。
[Composing Music With Recurrent Neural Networks](http://www.hexahedria.com/2015/08/03/composing-music-with-recurrent-neural-networks/)

## 実際にどういう曲が作れるか
作成した曲をSoundCloudで公開中です。

https://soundcloud.com/issei-mori-688064393/stacked-lstm

## TODO
Chaotic Inspiration Algorithmと組み合わせる。
Coca, Andres E., Débora C. Corrêa, and Liang Zhao. "Computer-aided music composition with LSTM neural network and chaotic inspiration." Neural Networks (IJCNN), The 2013 International Joint Conference on. IEEE, 2013.

Audio Chord Estimationと組み合わせてコード進行も自動生成させる。
http://www.music-ir.org/mirex/wiki/2016:Audio_Chord_Estimation

