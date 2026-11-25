"""Narration, one list per scene, one string per on-screen beat.
Edit freely: beat lengths follow word counts (or the recorded clip, see common.py)."""
NAME = "Vivek Krishna"
STUDENT_ID = "E25B070706"
WORDS_PER_SECOND = 2.25

NARRATION = {
1: [
 "Hello. In this video we ask one question: what does a matrix actually do?",
 "Here are two copies of the same grid, each carrying the same letter F. We will use two simple moves. One is a quarter turn, anticlockwise. The other is a shear, which slides the grid sideways.",
 "On the left, turn first, and then shear. On the right, shear first, and then turn.",
 "The same two moves, but the pictures are different! Why does the order matter? To answer that, we need to see a matrix as a movement.",
],
2: [
 "A matrix is a rectangular table of numbers. This one, C, has two rows and three columns, so we call it a two by three matrix.",
 "Each entry has an address: the row first, then the column. So c two three is the entry in row two, column three. Here, it is four.",
 "As a machine, an m by n matrix takes n numbers in, one for each column, and gives m numbers out, one for each row.",
 "Now take a two by two matrix. Call the basic arrows e one, which is one, zero, and e two, which is zero, one. The columns tell us where they land. Column one is where e one goes. Column two is where e two goes.",
 "By the end, you will be able to explain why matrices add, scale and multiply the way they do.",
],
3: [
 "Let us watch the shear matrix B move the plane. The arrow e one stays put, at one, zero. The arrow e two slides across to one, one. Those are exactly the columns of B. Notice that grid lines stay straight, parallel and evenly spaced, and the origin stays fixed.",
 "Now follow the vector v, equal to one, two. Before the move, it is one step of e one plus two steps of e two. After the move, the recipe is the same, using the new arrows: one times column one, plus two times column two. That gives B v, which is three, two.",
 "Next, addition. The quarter turn, A, sends v to minus two, one. The shear, B, sends v to three, two. Adding the matrices means adding their outputs, tip to tail. We reach one, three.",
 "Columns are outputs too, so they add in the same way, and that is why we add matching entries. The two matrices must have the same size, or the outputs could not be added.",
 "Scaling is simpler. Two times B doubles every output, so three, two becomes six, four. Every entry of B is doubled.",
],
4: [
 "Now for multiplication. The product A B means: do B first, and then do A. We read from right to left, because the vector enters on the right.",
 "To find the matrix of the combined move, follow the two basic arrows. After B, they stand at the columns of B.",
 "Push column one through A. One times the first column of A, plus zero times the second, gives zero, one. That is column one of the product.",
 "Push column two through A. One times the first column, plus one times the second, gives minus one, one. That is column two of the product.",
 "Now look at a single entry. The top left entry took row one of A with column one of B: zero times one, plus minus one times zero, equals zero.",
 "Top right: row one with column two. Zero times one, plus minus one times one, gives minus one.",
 "Bottom left: row two with column one. One times one, plus zero times zero, gives one.",
 "Bottom right: row two with column two. One times one, plus zero times one, gives one. So the row times column rule is just bookkeeping for doing one move after another.",
],
5: [
 "Back to our puzzle. Turning first and then shearing is B A, with columns one, one and minus one, zero. Shearing first and then turning is A B, with columns zero, one and minus one, one. They are different matrices.",
 "Test them on v. A B sends it to minus two, three. B A sends it to minus one, one. So in general, A B is not equal to B A.",
 "This also explains the size rule. An m by n matrix times an n by p matrix works, because the p inputs become n numbers, and those n numbers are exactly what the next machine needs. The result is m by p.",
],
6: [
 "To summarise. One: the columns of a matrix show where the basic arrows land. Two: adding and scaling matrices means adding and scaling their outputs. Three: multiplying matrices means doing one move after another, so order matters.",
 "Thank you for watching.",
],
}

if __name__ == "__main__":
    total = 0
    for n, beats in NARRATION.items():
        w = sum(len(b.split()) for b in beats); s = w / WORDS_PER_SECOND; total += s
        print(f"\nSCENE {n}  (about {s:.0f} s)\n" + "\n\n".join(beats))
    print(f"\nTOTAL about {total/60:.1f} min")
