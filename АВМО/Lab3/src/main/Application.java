package main;

import java.io.IOException;

public class Application {
    public static void main(String[] args) throws IOException {
        Table table = new Table("table.txt");
        table.printTable();
        table.logic();
    }
}
