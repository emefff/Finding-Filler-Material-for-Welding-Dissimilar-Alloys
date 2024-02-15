The shared code automatically chooses a filler material for welding of dissimilar metals. A Schaeffler diagram is overlayed in the graph window, some important curves are digitized point by point to make them useable for the calculation. 
The usual 'algorithm' when using this diagram is as follows: calculate Ni- and Cr- equivalent of all three metals (weld metal 1, weld metal 2 and filler material). Connect the two weld metals by a line in the diagram, halve the line. From this point,
draw a line to the filler material. Depending on the welding technique, filler material etc. a certain dilution of the two weld metals is achieved (usually between 20-40%, that means in the case of 20%: 10% from weld metal 1 and 10% from weld metal 2,
the rest of the weld bead will be filler material). Essentially, the newly created alloy in the weld will always lie on this line. If you absolutly do not know which filler to use, this process can tak some time in the analog world (reading datasheets,
drawing a bit etc..). 
The advantage of this little program is, that you only have to build a little database of your materials and, essentially, do some operations like in the attached code. You'll be able to check a lot of filler materials within fractions of a second.
The below example shows two alloys and a bunch of filler materials, some of them are completely unusable. Essentially, we want to find dilution points 25% and 30% in the vicinity of a chosen ferrite content (the straight lines on the right-hand side 
of the diagram). The program will measure the distances of the evaluated points to these lines and choose the best filler for the two alloys. The result looks like this:

![Bildschirmfoto vom 2024-02-15 17-10-46](https://github.com/emefff/Finding-Filler-Material-for-Welding-Dissimilar-Alloys/assets/89903493/93fd2805-a959-4902-90b5-996d20296bb5)
