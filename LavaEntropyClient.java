// LavaEntropyClient.java
// This Java program connects to Python lava blobs server
//fetches the "entropy" (random hash) generated from the lava lamp screen
// It is supposed to print the hash in the console every 2 seconds
// you can change the every 2 seconds to whatever you want tho

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;

public class LavaEntropyClient {
    public static void main(String[] args) {
        try {
            //fetches 5 for demonstration
            for (int i = 0; i < 5; i++) {
                String entropy = fetchEntropy(); // get the hash from server
                // prints result or "Failed" if something went wrong
                System.out.println("Entropy [" + (i + 1) + "]: " + (entropy != null ? entropy : "Failed"));
                Thread.sleep(2000); //you have to wait 2 seconds before fetching again, just a small cooldown
            }
        } catch (Exception e) {
            e.printStackTrace(); //if crashes, it will explain why
        }
    }

  //talks to flask
    private static String fetchEntropy() {
        try {
            //converts string URL to URI then to URL idk
            URI uri = new URI("http://localhost:5000/entropy");
            URL url = uri.toURL();

            // open connection
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");

            //reads server response
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            StringBuilder content = new StringBuilder();
            String line;
            while ((line = in.readLine()) != null) content.append(line);
            in.close(); //close the stream
            con.disconnect(); //disconnects to free resources

            String json = content.toString().trim();
            if (json.startsWith("{") && json.endsWith("}")) {
                int start = json.indexOf(":\"") + 2; // start of hash
                int end = json.indexOf("\"", start); // end of hash
                if (start > 1 && end > start) {
                    return json.substring(start, end); // return the hash
                }
            }

            return null; // if fail return null
        } catch (Exception e) {
            return null; // if fail return null
        }
    }
}
