package com.example.sai_pher.efua;

import android.net.Uri;
import android.os.Environment;
import android.support.design.widget.TextInputEditText;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.hardware.Camera;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import static android.provider.MediaStore.Files.FileColumns.MEDIA_TYPE_IMAGE;
import static android.provider.MediaStore.Files.FileColumns.MEDIA_TYPE_VIDEO;


public class guess_what extends AppCompatActivity {

    Camera camera;
    FrameLayout frameLayout;
    ShowCamera showCamera;
    Camera.PictureCallback pictureCallback = new Camera.PictureCallback() {
        @Override
        public void onPictureTaken(byte[] data, Camera camera) {
            //do something
            File photo = getOutputMediaFile(MEDIA_TYPE_IMAGE);
            if (photo == null) {
                Log.d("Error", "no photo take / saved");
                return;
            }
            else {

                guess_cycle(data, photo);

            }
        }
    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_guess_what);
    }

    private void guess_cycle(byte[] data, File photo) {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        TextInputEditText labelIn = findViewById(R.id.labelInput);

        String label = String.valueOf(labelIn.getText());
        String name = label + timeStamp + ".jpg";

//        send(data, label, name);
//        Toast.makeText(getApplicationContext(), "guess cycle working", Toast.LENGTH_LONG).show();
        TextView gtv = findViewById(R.id.guessCapture);
        gtv.setText("guess cycle working");

        FileOutputStream fos = null;
        try {
            fos = new FileOutputStream(photo);
            fos.write(data);
            fos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


        camera.stopPreview();
        resetCamera();
    }

    /**
     * Create a file Uri for saving an image or video
     */
    private static Uri getOutputMediaFileUri(int type) {
        return Uri.fromFile(getOutputMediaFile(type));
    }

    /**
     * Create a File for saving an image or video
     */
    private static File getOutputMediaFile(int type) {
        // To be safe, you should check that the SDCard is mounted
        // using Environment.getExternalStorageState() before doing this.

        File mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES), "Efua_V1");
        // This location works best if you want the created images to be shared
        // between applications and persist after your app has been uninstalled.

        // Create the storage directory if it does not exist
        if (!mediaStorageDir.exists()) {
            if (!mediaStorageDir.mkdirs()) {
                Log.d("MyCameraApp", "failed to create directory");
                return null;
            }
        }

        // Create a media file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        File mediaFile;
        if (type == MEDIA_TYPE_IMAGE) {
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "IMG_" + timeStamp + ".jpg");
        } else if (type == MEDIA_TYPE_VIDEO) {
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "VID_" + timeStamp + ".mp4");
        } else {
            return null;
        }

        return mediaFile;
    }

    public void capture(View v) {

        captureImage();
//        resetCamera();

    }

    public void send(final byte[] photo, final String label, final String name) {

        Toast.makeText(getApplicationContext(), "Sending: " + label + " " + name, Toast.LENGTH_LONG).show();
        Log.d("Sending: ", label + " " + name);
        TextView textView = findViewById(R.id.photoTextView);
        textView.setText(String.format("Label: %s \nName: %s", label, name));

        VolleyManager volley = new VolleyManager(this);

        String url = volley.getIP_ADDRESS() + ":3000/photo/create";

        final String encode_photo = Base64.encodeToString(photo, 0);


        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Toast.makeText(getApplicationContext(), String.valueOf(response), Toast.LENGTH_LONG).show();
                    }

                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(getApplicationContext(), String.valueOf(error), Toast.LENGTH_LONG).show();
                        Log.d("Error: ", String.valueOf(error));
                    }
                }) {
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<String, String>();
                params.put("name", name);
                params.put("label", label);
                params.put("image", encode_photo);

                return params;

            }
        };


        {
            int socketTimeout = 30000;
            RetryPolicy policy = new DefaultRetryPolicy(socketTimeout, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT);
            stringRequest.setRetryPolicy(policy);

            volley.addToRequestQueue(stringRequest);

        }

    }

    private void captureImage() {
        if (camera != null)
            camera.takePicture(null, null, pictureCallback);
    }

    private void resetCamera() {
        camera.stopPreview();
        camera.startPreview();
    }
}
