Fixed the bug when label outline cannot overlay exactly on label literals when rotate angle > 90;
However, when rotate angle > 180, the overlay problem still exist.
A possible solution is to write another draw label method, following the operations of current method but target on situation when rotate angle > 180.
