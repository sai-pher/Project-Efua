package com.example.efua_v1;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.POST;
import retrofit2.http.Streaming;

public interface ApiList {

    @Streaming
    @POST("/ml/update")
    Call<ResponseBody> update();
}
