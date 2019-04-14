package com.example.sai_pher.efua;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

    }

    public void guessWhat(View view) {
        Intent intent = new Intent(this, guess_what.class);
        startActivity(intent);
    }

    public void explore(View view) {
        Intent intent = new Intent(this, ExplorePage.class);
        startActivity(intent);
    }

    public void testServer(View view) {
//        Toast.makeText(getApplicationContext(), "good", Toast.LENGTH_SHORT).show();

        final TextView textView = findViewById(R.id.textView);

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
}
