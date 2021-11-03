# Packet reordering

## Introduction

The task of this kata is to implement a receiver that receives a stream of packets where packets may be out or order,
and outputs a stream of the contents of packets in correct order.

The packets are pairs `(seqn, contents)`, where `seqn` is the packet's sequence number and `contents` is
a string. When the packets are in correct order, the sequence number starts at 0 and increases by 1 for each
packet.

The packets are only "locally unordered", meaning that they may be reordered using a sliding window.

## Example

Let's assume a window size of 4. The window size is a constraint on the input stream and an argument of the receiver
function you need to implement. Let's assume further that the receiver has received packets 0, 1, 2, 4, 5. Since
packets 0, 1, and 2 are in order, they may be passed to the output stream. Next packet expected is packet 3. This
packet will be received in a window of size 4 starting at position 3:

```
0, 1, 2, ?, 4, 5, ?, ...
        |-----------|
            window
```

Until the sender has received an acknowledgment for packet 3, the sender will only send packets that belong to the
window, i.e., packets 3, 4, 5, or 6.  Once the receiver receives packet 3, it may pass packets 3, 4, and 5 to the
output stream and slide the window to position 6, which is the next packet expected.

```
0, 1, 2, 3, 4, 5, ?, ?, ?, ?, ...
                 |-----------|
                    window
```
After the sender has received an acknowledgement for all packet up to packet 5, it will send packets in the window
6, 7, 8, 9. Assume packet 6 is received next. Again, the receiver can slide the window, this time to position 7,
which is the position of the next packet expected.

Etc.

Note that when the window size is 1, the packets will be received in correct order.

## Task specifics

Your task is to implement a function `receiver(input_stream, window_size)`, where `input_stream` is an iterator of
packets and `window_size` is a positive int denoting the window size. The `input_stream` may be finite or infinite.
Each packet is a pair `(seqn, constents)`, where `seqn` represents the sequence number _modulo `window_size`_, starting
at 0, and `contents` is a string. The contents of a packet may be the empty string, but is always a string, e.g., never
None.

Sending acknowlegments for packets received to the sender is not part of the task.

The output of the function must be an iterable, such that, when iterated over, it yields the _contents_ of the packets
in correct order.
