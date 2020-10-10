# msm5232wsg

USAGE: python msm5232wsg.py any".fxb"file(made by Chip32 VSTi)

OKI MSM5232 サウンドチップの出力波形に似せようとした WaveTable を作成して、フリーの VSTi である Chip32 (Sam氏作成) 用の .fxb 形式のファイルと、１５個の wav ファイル（8Bit, 48kHz, モノラル, 32 サンプル）を出力するスクリプトです。  
引数には予め Chip32 で Export しておいた任意の fxb 形式のファイルを指定してください（ヘッダー等の情報を参照するためのみに使用し、中のデータは使いませんのでどんなデータのものでも構いません。ファイルの上書きもしません）。  
このスクリプトを実行すると、実施した時点の日時で "YYMMDDhhmmss" 形式で新しいフォルダが作られます。そして、フォルダの中に１個の Chip32用の fxb ファイルと１５個の wav ファイルが収められます。  
fxb ファイルは、 MSM5232likeWaveTable.fxb という名前です。wav ファイルは、MSM5232Table01～15.wav という名前です。fxbファイルに入っている最後の１６番目の MSM5232dummy は数合わせのダミーです（読み込むと最初に表示されてしまいますが・・・）。  

この wav ファイルは、SONICWARE社製 ELZ_1 （エルザワン）　シンセサイザーの 8BIT WAVMEM SYNTH　波形データとして読み込ませることができます（たぶん）。  

このスクリプトは、私自身の python と github の勉強用に作ったものです。特に、実物の MSM5232 と音が違うという点については、あくまで、「MSM5232風」ということでご了解願います。  
Windows PC 上で python 3.8.3 を使用しました。  

まともに動かなかったりファイルが壊れたりしても当方は一切責任を負いません。リスクを承知の上で使ってください。  
既知の問題：音を柔らかくしたかったので、Chip32 のフィルターの値を２にセットしようと思ったのですが、なぜか１になってしまいます。読み込み後、適宜手動で調整してください。

波形の作成にあたって、以下のページを参照しました。  
http://sr4.sakura.ne.jp/acsound/taito/taito5232.html  

This script creates 15 WaveTables that I tried to imitate OKI MSM5232 tones.  
The script outputs a .fxb file for Chip32 (created by Sam), a free VSTi, and 15 wav files (8Bit, 48kHz, mono, 32 samples).    
One argument is necessary and it must be an arbitrary fxb-format file created by and for Chip32 (for the use to get headers and other information).  
When you run this script, a new folder will be created with the "YYMMDDhhmmss" format at the time of execution. The folder will contain an fxb file and wav files.  
The fxb-format file is named "MSM5232likeWaveTable.fxb". Wave files are named "MSM5232Table01...15.wav".  
Notice: The 16th wavetable named MSM5232dummy in the fxb file that appears at first when loaded by Chip32 is just a dummy file to make fxps 16 and it has no sound.  

Those wav files are expected be able to be loaded as 8-bit WAVMEM SYNTH wavetable data for the SONICWARE ELZ_1 synthesizer.  

I made this script for my python and github studies sake.
I used python 3.8.3 on a Windows PC.  

A known problem: I wanted to set the value of the filter of Chip32 to 2 to make sound softer, but for some reason it's set to 1.  

The following page was consulted in creating the wavetables:
http://sr4.sakura.ne.jp/acsound/taito/taito5232.html  

# Some graphs of wavetables made by this script.

![Figure1](https://user-images.githubusercontent.com/68761912/95644717-75865280-0af3-11eb-9904-3d5cafd55079.png)
![FigureD](https://user-images.githubusercontent.com/68761912/95644721-7c14ca00-0af3-11eb-9322-6987c727499b.png)
![FigureE](https://user-images.githubusercontent.com/68761912/95644728-820aab00-0af3-11eb-9052-a45dc3799389.png)
![FigureF](https://user-images.githubusercontent.com/68761912/95644732-859e3200-0af3-11eb-86ed-d67b512253fd.png)

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.   
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.  
