package com.example.efua_v1;

import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;

public class TfLiteModel {

    @SerializedName("name")
    private String name;
    @SerializedName("lables")
    private ArrayList<String> lables;
    @SerializedName("model")
    private byte model;

    public TfLiteModel(String name, ArrayList<String> lables, byte model) {
        this.name = name;
        this.lables = lables;
        this.model = model;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public ArrayList<String> getLables() {
        return lables;
    }

    public void setLables(ArrayList<String> lables) {
        this.lables = lables;
    }

    public byte getModel() {
        return model;
    }

    public void setModel(byte model) {
        this.model = model;
    }
}
