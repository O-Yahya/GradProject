package com.example;

public class NotUnderLock {

    public void bufferOverflowL1() {
        int[] arr = new int[5];
        arr[5] = 10; // Array index out-of-bounds: writing to arr[5], which is out of bounds
    }
    
}
