package main;

public class Cell {
    private boolean isBasis;
    private int rate;
    private int transit;

    public Cell(int rate){
        this.rate = rate;
        isBasis = true;
        transit = -1;
    }

    @Override
    public String toString() {
        String val;
        if(isBasis) {
            val = "";
        } else {
            val = "-";
        }
        String trans = "";
        if(transit != -1){
            trans = String.valueOf(transit);
        }

        return rate + val + ":" + trans + " ";
    }

    public boolean isBasis() {
        return isBasis;
    }

    public void setBasis(boolean basis) {
        isBasis = basis;
    }

    public int getRate() {
        return rate;
    }

    public void setRate(int rate) {
        this.rate = rate;
    }

    public int getTransit() {
        return transit;
    }

    public void setTransit(int transit) {
        this.transit = transit;
    }
}
