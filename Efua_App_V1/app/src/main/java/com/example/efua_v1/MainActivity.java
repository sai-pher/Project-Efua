package com.example.efua_v1;

import android.app.DownloadManager;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.res.AssetFileDescriptor;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.channels.FileChannel;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;

public class MainActivity extends AppCompatActivity {


    private DownloadManager downloadManager;
    private long downloadReference;
    private ProgressDialog progressDoalog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

//        IntentFilter filter = new IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE);
//        registerReceiver(downloadReceiver, filter);
    }

    public void guessWhat(View v){
        Intent intent = new Intent(this, GuessWhatActivity.class);
        startActivity(intent);
    }

    public void explore(View v){
        Intent intent = new Intent(this, ExploreActivity.class);
        startActivity(intent);
    }

    public void testServer(View view) {
        VolleyManager volley = new VolleyManager(this);


        String url = volley.getIP_ADDRESS() + ":3000/ok";


        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("upload", String.valueOf(response));

                        Toast.makeText(getApplicationContext(), String.valueOf(response), Toast.LENGTH_SHORT).show();
//                        textView.setText(response);
                    }

                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("error", String.valueOf(error));
                        Toast.makeText(getApplicationContext(), String.valueOf(error), Toast.LENGTH_SHORT).show();

                    }
                });

        {
            int socketTimeout = 10000;
            RetryPolicy policy = new DefaultRetryPolicy(socketTimeout, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT);
            stringRequest.setRetryPolicy(policy);

            volley.addToRequestQueue(stringRequest);

        }
    }

    public void updata(View view) {

        VolleyManager volley = new VolleyManager(this);

        String url = volley.getIP_ADDRESS() + ":3000/ml/update";

        JsonObjectRequest stringRequest = new JsonObjectRequest(Request.Method.GET, url, null, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                String filename = "model.tflite";
                FileOutputStream outputStream;

                try {
                    Log.d("Load", "loading model");
                    Toast.makeText(getApplicationContext(), "loading model ->" + String.valueOf(response.get("name")), Toast.LENGTH_SHORT).show();

                    outputStream = openFileOutput(filename, Context.MODE_PRIVATE);
                    outputStream.write((byte[]) response.get("model"));
                    outputStream.close();
                    Log.d("Load", "model loaded");
                } catch (Exception e) {
                    e.printStackTrace();
                }


                try {

                    AssetFileDescriptor fileDescriptor = getAssets().openNonAssetFd(filename);
                    FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
                    FileChannel fileChannel = inputStream.getChannel();

                    if (fileChannel.isOpen())
                        Toast.makeText(getApplicationContext(), String.valueOf(response.get("name") + " loaded"), Toast.LENGTH_SHORT).show();
                    else
                        Toast.makeText(getApplicationContext(), "chanel not open", Toast.LENGTH_SHORT).show();
                } catch (JSONException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

            }
        });


        int socketTimeout = 10000;
        RetryPolicy policy = new DefaultRetryPolicy(socketTimeout, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT);
        stringRequest.setRetryPolicy(policy);

        volley.addToRequestQueue(stringRequest);

    }

    public void update(View view) {

        VolleyManager volley = new VolleyManager(this);

        String url = volley.getIP_ADDRESS() + ":3000/ml/update";

        progressDoalog = new ProgressDialog(MainActivity.this);
        progressDoalog.setMessage("Loading....");
        progressDoalog.show();

        ApiList service = RetrofitClient.getRetrofitInstance().create(ApiList.class);
        Call<ResponseBody> call = service.update();

        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, final retrofit2.Response<ResponseBody> response) {
                progressDoalog.dismiss();

                if (response.isSuccessful()) {
                    Log.d("tag", "server contacted and has file");

                    assert response.body() != null;

                    new AsyncTask<Void, Void, Void>() {
                        @Override
                        protected Void doInBackground(Void... voids) {

                            ResponseBody body = response.body();

                            writeResponseBodyToDisk(body);


                            //                            boolean success = writeResponseBodyToDisk(response.body());

//                            Log.d("success", String.valueOf(success));

                            return null;
                        }
                    }.execute();

                } else {
                    Log.d("tag", "server contact failed");
                }

            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                progressDoalog.dismiss();
                Toast.makeText(MainActivity.this, "Something went wrong...Please try later!", Toast.LENGTH_SHORT).show();
            }
        });


    }

    private boolean writeResponseBodyToDisk(ResponseBody body) {
        try {
            // todo change the file location/name according to your needs
            File futureStudioIconFile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), "tfmodel.txt");

//            JSONParser parser = new JSONParser();


            String fileName = "tf_model.tflite";
            byte[] fileContents = body.bytes();


            try {
                InputStream inputStream = null;
                OutputStream outputStream = null;

                outputStream = openFileOutput(fileName, Context.MODE_PRIVATE);
                outputStream.write(fileContents);
                outputStream.close();

                Log.d("storage", "writen to internal");

                String path = this.getFilesDir().getAbsolutePath() + "/" + fileName;
                File file = new File(path);


                if (file.exists()) {
                    Log.d("storage", "read from internal");
                    AssetFileDescriptor fileDescriptor = getAssets().openNonAssetFd(path);
                    FileInputStream checkInputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
                    FileChannel fileChannel = checkInputStream.getChannel();
                    if (fileChannel.isOpen())
                        Log.d("storage", "read from channel");
                    else
                        Log.d("storage", "cant read from channel");


                } else
                    Log.d("storage", "cant read from internal");

            } catch (Exception e) {
                e.printStackTrace();
                Log.d("storage", "not writen to internal");

            }


//            InputStream inputStream = null;
//            OutputStream outputStream = null;
//
//            try {
//                byte[] fileReader = new byte[4096];
//
//                long fileSize = body.contentLength();
//                long fileSizeDownloaded = 0;
//
//                inputStream = body.byteStream();
//                outputStream = new FileOutputStream(futureStudioIconFile);
//
//                while (true) {
//                    int read = inputStream.read(fileReader);
//
//                    if (read == -1) {
//                        break;
//                    }
//
//                    outputStream.write(fileReader, 0, read);
//
//                    fileSizeDownloaded += read;
//
//                    Log.d("tag", "file download: " + fileSizeDownloaded + " of " + fileSize);
//                }
//
//                outputStream.flush();
//
//                return true;
//            } catch (IOException e) {
//                return false;
//            } finally {
//                if (inputStream != null) {
//                    inputStream.close();
//                }
//
//                if (outputStream != null) {
//                    outputStream.close();
//                }
//            }
        } catch (IOException e) {
            return false;
        }
        return true;
    }

//    public void update(View view){
//
//        VolleyManager volley = new VolleyManager(this);
//        String url = volley.getIP_ADDRESS() + ":3000/ml/update";
//
//        downloadManager = (DownloadManager)getSystemService(DOWNLOAD_SERVICE);
//        Uri Download_Uri = Uri.parse(url);
//        DownloadManager.Request request = new DownloadManager.Request(Download_Uri);
//
//        request.setAllowedNetworkTypes(DownloadManager.Request.NETWORK_WIFI | DownloadManager.Request.NETWORK_MOBILE);
//        //Set whether this download may proceed over a roaming connection.
//        request.setAllowedOverRoaming(false);
//        //Set the title of this download, to be displayed in notifications (if enabled).
//        request.setTitle("TfLite model");
//        //Set a description of this download, to be displayed in notifications (if enabled)
//        request.setDescription("TfLite model download complete");
//        //Set the local destination for the downloaded file to a path within the application's external files directory
//        request.setDestinationInExternalFilesDir(this, Environment.DIRECTORY_DOWNLOADS,"tf-model.json");
//
//        //Enqueue a new download and same the referenceId
//        downloadReference = downloadManager.enqueue(request);
//
//    }

//    private BroadcastReceiver downloadReceiver = new BroadcastReceiver() {
//
//        @Override
//        public void onReceive(Context context, Intent intent) {
//
//            //check if the broadcast message is for our Enqueued download
//            long referenceId = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1);
//            if(downloadReference == referenceId){
//
//                int ch;
//                ParcelFileDescriptor file;
//                StringBuffer strContent = new StringBuffer("");
//
//                //parse the JSON data and display on the screen
//                try {
//                    file = downloadManager.openDownloadedFile(downloadReference);
//                    FileInputStream fileInputStream
//                            = new ParcelFileDescriptor.AutoCloseInputStream(file);
//
//                    while( (ch = fileInputStream.read()) != -1)
//                        strContent.append((char)ch);
//
//                    JSONObject responseObj = new JSONObject(strContent.toString());
//
//                    Toast.makeText(getApplicationContext(), (CharSequence) responseObj.get("name"), Toast.LENGTH_SHORT).show();
//
//
//                } catch (FileNotFoundException e) {
//                    e.printStackTrace();
//                } catch (IOException e) {
//                    e.printStackTrace();
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                }
//
//            }
//        }
//    };

}
