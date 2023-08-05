# RomoNepali

Romonised nepali input method for LInux.This uses [romonisednepali](https://github.com/psuzn/romonisedNepali) to convert the raw input to unicode characters.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)

## Installation
(This is in  alpha version so might not be stable.)

<B>1.First install [node](http://blog.teamtreehouse.com/install-node-js-npm-linux) (also npm) and [pip](https://www.tecmint.com/install-pip-in-linux/).</B>


<B>2.Install [romonisednepali](https://github.com/psuzn/romonisedNepali) using npm</B>

```sh
$ npm install -g romonisednepali 
```
(If any error occurred please refer [here](https://github.com/psuzn/romonisedNepali) to install by other methods)


You must install [romonisednepali](https://github.com/psuzn/romonisedNepali) beacuse it uses this to convert into romonised nepali.




<B>3.Install romonepali</B>


Using pip:

```sh
$ sudo pip install romonepali
```

Or 

Manually:

```sh
$ git clone https://github.com/psuzn/romoNepali.git
$ cd romoNepali
$ sudo python3 setup.py install 
```

## Usage

Just execute ```romonepali``` from the terminal

```sh
$ romonepali

```
For the verbose output give ```-v``` flag 
```sh
$ romonepali -v

```

## Support
This is in  alpha version and might cause some problem. so you can help me make it stable.


Please [open an issue](https://github.com/psuzn/romoNepali/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/psuzn/romoNepali/compare/).
