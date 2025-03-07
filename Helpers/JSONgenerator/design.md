我需要在JSONgenerator里边添加一个把炼金配方和数据转成json的编码器以及相配套的解码器。

这个json是一个数组，它的的格式如下：
id:(number)
name:(string)
tags:[(string1),(string2)]...
materials:{
    type:"class"/"material"
    id:""
}
rewards:[{
    level:(number)
    property:(string),
    id:[]
},{}...]

请你将这个编码器做成带GUI的，方便我输入。

同时，rewards的id的编码器与解码器也需要制作。
它的内容是对一个3*3的方格进行编码，每个格子有三种可能，圈，星或空白。同时这个方格上的所有空白格子可能有颜色，但这些颜色一定是一样的。