convert xc:black xc:red xc:yellow xc:green1 xc:cyan xc:blue xc:black +append -filter Cubic -resize 50x30! convert_rainbow.jpg
convert pattern:gray50 convert_grey.png
convert rose: convert_rose.png
montage rose: rose: rose: \( pattern:gray50 -set label gray \) -background chartreuse -geometry +0+0 convert_montage.png