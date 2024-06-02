package com.example;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class VulnerableApp {

    public void bufferOverflowL1() {
        int[] arr = new int[5];
        arr[4] = 10; // Within bounds
        arr[5] = 10; // Array index out-of-bounds: writing to arr[5], which is out of bounds
    }

    // Method with a variable index that might be out of bounds
    public void bufferOverflowL2() {
        int[] arr = new int[5];
        int index = 5;
        if (index >= 0 && index < 6) {
            arr[index] = 10; // Array index out-of-bounds: index could be 5, which is out of bounds
        }
    }

    // Method with an uncontrolled index
    public void bufferOverflowL5() {
        int[] arr = new int[5];
        int index = (int) (Math.random() * 10); // Random value could be out of bounds
        if (index < arr.length) {
            arr[index] = 10; // Within bounds check added
        }
    }

    // Method with potential null pointer dereference
    public void nullPointerDereference() {
        String str = null;
        if (str.equals("test")) { // Null pointer dereference
            System.out.println("This is never reached");
        }
    }

    // Method with potential resource leak
    public void resourceLeak() {
        try {
            java.io.FileInputStream fis = new java.io.FileInputStream("test.txt");
            // Forgetting to close the file
        } catch (java.io.IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        VulnerableApp app = new VulnerableApp();
        app.bufferOverflowL1();
        app.bufferOverflowL2();
        app.bufferOverflowL5();
        app.nullPointerDereference();
        app.resourceLeak();
    }
}
