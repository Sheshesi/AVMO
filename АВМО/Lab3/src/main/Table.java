package main;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Table {
    private Cell[][] table;
    private List<Integer> columnNumbers = new ArrayList<>();
    private List<Integer> lineNumbers = new ArrayList<>();
    private int m = 3;  //Поставщики - столбец
    private int n = 4;  //Потребители - строка
    private int delta = 0;

    public Cell[][] getTable() {
        return table;
    }

    public List<Integer> getColumnNumbers() {
        return columnNumbers;
    }

    public List<Integer> getLineNumbers() {
        return lineNumbers;
    }

    public void checkLiveniess(){
        int columnSum = 0;
        int lineSum = 0;
        for (int i = 0; i < n; i++) {
            if(table[m][i].getRate() != 0){
                lineSum += table[m][i].getRate();
            }
        }
        for (int i = 0; i < m; i++) {
            if(table[i][n].getRate() != 0){
                columnSum += table[i][n].getRate();
            }
        }
        if(columnSum > lineSum){
            delta = 1;
            int val = columnSum - lineSum;
            Cell[][] newTable;
            n++;
            newTable = new Cell[m+1][];
            for (int i = 0; i < m+1; i++) {
                newTable[i] = new Cell[n+1];
            }
            for (int i = 0; i < m+1; i++) {
                for (int j = 0; j < n-1; j++) {
                    newTable[i][j] = table[i][j];
                }
            }
            for (int i = 0; i < m; i++) {
                newTable[i][n-1] = new Cell(0);
                newTable[i][n] = table[i][n-1];
            }

            newTable[m][n-1] = new Cell(val);
            table = newTable;

        } else if (lineSum > columnSum){
            delta = -1;
            int val = lineSum - columnSum;
            Cell[][] newTable;
            m++;
            newTable = new Cell[m+1][];
            for (int i = 0; i < m+1; i++) {
                newTable[i] = new Cell[n+1];
            }
            for (int i = 0; i < m-1; i++) {
                for (int j = 0; j < n+1; j++) {
                    newTable[i][j] = table[i][j];
                }
            }
            for (int i = 0; i < n; i++) {
                newTable[m-1][i] = new Cell(0);
                newTable[m][i] = table[m-1][i];
            }

            newTable[m-1][n] = new Cell(val);
            table = newTable;
        }

        System.out.println("col: " + columnSum);
        System.out.println("line: " + lineSum);
    }

    public Table(String filePath) throws IOException {
        table = new Cell[m+1][];
        for (int i = 0; i < m+1; i++) {
            table[i] = new Cell[n+1];
        }

        File file = new File(filePath);
        BufferedReader bufferedReader = new BufferedReader(new FileReader(file));
        String line = bufferedReader.readLine();
        int height = 0;
        while (line != null){
            String[] split = line.split(" ");
            for (int i = 0; i < split.length; i++) {
                table[height][i] = new Cell(Integer.parseInt(split[i]));
            }
            height++;
            line = bufferedReader.readLine();
        }
        checkLiveniess();
    }

    public void printTable(){
        System.out.printf("Постав              Потребители                   Запасы\n");
        for (int i = 0; i < m+1; i++) {
            if(i == m){
                System.out.printf("Потреб  ");
            }else {
                System.out.printf("A%d      ", i+1);
            }
            for (int j = 0; j < n+1; j++) {
                if(i == m && j == n){

                } else {
                    if (table[i][j] != null) {
                        System.out.printf("%8s", table[i][j]);
                    }
                }
            }
            System.out.println();
        }
    }

    public void logic(){
        while (!false) {
            findDelta();
            if(checker()){
                printTable();
                break;
            }
            System.out.println("\n");
        }
        System.out.println("Стоимость перевозок: " + getAnsw());
    }

    public boolean isEnd(){
        boolean isEnd = true;
        for (int i = 0; i < n; i++) {
            if(table[m][i].getRate() != 0){
                isEnd = false;
            }
        }
        for (int i = 0; i < m; i++) {
            if(table[i][n].getRate() != 0){
                isEnd = false;
            }
        }

        return isEnd;
    }

    public void findDelta(){
        for (int i = 0; i < m; i++) {
            List<Cell> lister = Arrays.asList(table[i]);
            lister = lister.stream().limit(n-delta).collect(Collectors.toList());

//            boolean flag = true;
//            for(Cell c : lister){
//                if(c.getRate() != 0){
//                    flag = false;
//                }
//            }

            List<Cell> list = lister.stream()
                    .filter(cell -> cell.isBasis())
                    .sorted((c1, c2) -> c1.getRate() - c2.getRate())
                    .limit(2).collect(Collectors.toList());
            if(list.size() < 2 ){
                if(list.size() == 1){
                    columnNumbers.add(list.get(0).getRate());
                } else {
                    columnNumbers.add(-1);
                }
            } else {
                columnNumbers.add(Math.abs(list.get(0).getRate() - list.get(1).getRate()));
            }
        }

        for (int i = 0; i < n; i++) {
            List<Cell> lister = createListFromColumn(i).stream().limit(m).collect(Collectors.toList());

//            boolean flag = true;
//            for(Cell c : lister){
//                if(c.getRate() != 0){
//                    flag = false;
//                }
//            }

            List<Cell> list = lister.stream()
                    //.filter(cell -> cell.getRate() != 0)
                    .filter(cell -> cell.isBasis())
                    .sorted((c1, c2) -> c1.getRate() - c2.getRate())
                    .limit(2).collect(Collectors.toList());
            if(list.size() < 2 ){
                if(list.size() == 1){
                    lineNumbers.add(list.get(0).getRate());
                } else {
                    lineNumbers.add(-1);
                }
            } else {
                lineNumbers.add(Math.abs(list.get(0).getRate() - list.get(1).getRate()));
            }
        }

        int lineNumbersIndex = -1;
        int maxValueLine = Integer.MIN_VALUE;
        int columnNumbersIndex = -1;
        int maxValueColumn = Integer.MIN_VALUE;

        for (int i = 0; i < lineNumbers.size(); i++) {
            if(maxValueLine < lineNumbers.get(i)){
                lineNumbersIndex = i;
                maxValueLine = lineNumbers.get(i);
            }
        }

        for (int i = 0; i < columnNumbers.size(); i++) {
            if(maxValueColumn < columnNumbers.get(i)){
                columnNumbersIndex = i;
                maxValueColumn = columnNumbers.get(i);
            }
        }

        //System.out.println("Line :" + maxValueLine + "  COl: " + maxValueColumn);
        int maxIndex = -1;
        boolean isLine = false;
        if(maxValueColumn > maxValueLine){
            maxIndex = columnNumbersIndex;
            isLine = true;
        } else {
            maxIndex = lineNumbersIndex;
            isLine = false;
        }

        if(columnNumbersIndex == -1 && lineNumbersIndex == -1){
            maxIndex = 2;
            isLine = true;
        }
        System.out.println("Столбец-" + maxIndex);
        poehali(maxIndex, isLine);
        columnNumbers.clear();
        lineNumbers.clear();
    }

    public void poehali(int index, boolean isLine){

        if (isLine == false) {
            List<Cell> listFromColumn = createListFromColumn(index);
            int indexMinValue = findMaxElementIndexInList(listFromColumn);
            System.out.println("Строка-" + indexMinValue);
            vuborkaIvuchet(indexMinValue, index);
            printTable();
        } else {
            List<Cell> listFromLine = Arrays.asList(table[index]);
            listFromLine = listFromLine.stream().limit(n).collect(Collectors.toList());
            if(delta == 1){
                listFromLine = listFromLine.stream().limit(n-1).collect(Collectors.toList());
            }
            int indexMinValue = findMaxElementIndexInList(listFromLine);
            System.out.println("Строка-" + indexMinValue);
            vuborkaIvuchet(index, indexMinValue);
            printTable();
        }

    }

    public boolean checker(){
        int counter = 0;
        int indX = -1;
        int indY = -1;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if(table[i][j].isBasis() == true){
                    counter++;
                    indX = i;
                    indY = j;
                }
            }
        }
        if(counter == 1 && indX != -1 && indY != -1){
            int val1 = table[indX][n].getRate();
            table[indX][n].setRate(0);
            int val2 = table[m][indY].getRate();
            table[m][indY].setRate(0);
            if(val1 < val2){
                table[indX][indY].setBasis(false);
                table[indX][indY].setTransit(val1);
            } else {
                table[indX][indY].setBasis(false);
                table[indX][indY].setTransit(val2);
            }
            return true;
        }
        return false;
    }

    public void vuborkaIvuchet(int x, int y){
        int RightVal = table[x][n].getRate();
        int BottVal = table[m][y].getRate();
        boolean flag = true;
        int val;
        if(RightVal < BottVal){
            val = RightVal;
            for (int i = 0; i < n; i++) {
                if(i != y) {
                    table[x][i].setBasis(false);
                }
            }
        } else if(BottVal < RightVal){
            val = BottVal;
            for (int i = 0; i < m; i++) {
                if(i != x) {
                    table[i][y].setBasis(false);
                }
            }
        } else if(BottVal == RightVal) {
            val = RightVal;

            List<Cell> list1 = createListFromColumn(y);
            List<Cell> list2 = Arrays.asList(table[x]);
            int minVal1 = Integer.MAX_VALUE;
            int minVal2 = Integer.MAX_VALUE;
            int ind1 = -1;
            int ind2 = -1;
            for (int i = 0; i < list1.size(); i++) {
                if((list1.get(i).getRate() < minVal1) && (i != x) && (list1.get(i).isBasis())){
                    minVal1 = list1.get(i).getRate();
                    ind1 = i;
                }
            }

            for (int i = 0; i < list2.size() - 1; i++) {
                if((list2.get(i).getRate() < minVal2) && (i != y) && (list2.get(i).isBasis())){
                    minVal2 = list2.get(i).getRate();
                    ind2 = i;
                }
            }
            System.out.println("IND1-" +ind1 + " IND2-" + ind2);
            if(ind2 == m){
                table[ind2][ind2+1].setTransit(0);
                table[x][y].setBasis(false);
                table[x][n].setRate(table[x][n].getRate() - val);
                table[m][y].setRate(table[m][y].getRate() - val);
                table[x][y].setTransit(val);
                return;
            }
            if(minVal1 < minVal2){
                if(ind1 != -1) {
                    table[ind2][x].setTransit(0);
                }
            } else {
                if(ind2 != -1) {
                    System.out.println("Y:=" + y);
                    table[ind1][y].setTransit(0);
                }
            }

            for (int i = 0; i < n; i++) {
                if(i != y) {
                    table[x][i].setBasis(false);
                }
            }
            for (int i = 0; i < m; i++) {
                if(i != x) {
                    table[i][y].setBasis(false);
                }
            }
        } else {
            val = 0;
        }
        table[x][y].setBasis(false);
        table[x][n].setRate(table[x][n].getRate() - val);
        table[m][y].setRate(table[m][y].getRate() - val);
        table[x][y].setTransit(val);
    }

    public int findMaxElementIndexInList(List<Cell> list){
        int minValue = Integer.MAX_VALUE;
        int index = -1;
        for (int i = 0; i < list.size(); i++) {
            if(list.get(i).getRate() < minValue && list.get(i).isBasis()){
                minValue = list.get(i).getRate();
                index = i;
            }
        }

        return index;
    }

    public List<Cell> createListFromColumn(int indexOfColumn){
        List<Cell> tempList = new ArrayList<>();
        for (int j = 0; j < m; j++) {
            tempList.add(table[j][indexOfColumn]);
        }
        return tempList;
    }

    public int getAnsw(){
        int value = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if(table[i][j].getTransit() != 0 && table[i][j].getTransit() != -1){
                    value += table[i][j].getRate()*table[i][j].getTransit();
                }
            }
        }
        return value;
    }
}
