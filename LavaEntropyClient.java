// LavaEntropyClient.java
// This Java program connects to Python lava blobs server
//fetches the "entropy" (random hash) generated from the lava lamp screen
// It is supposed to print the hash in the console every 2 seconds.

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;

public class LavaEntropyClient {
    public static void main(String[] args) {
        try {
            // Do 5 fetches for demonstration
            for (int i = 0; i < 5; i++) {
                String entropy = fetchEntropy(); // get the hash from server
                // Print the result or "Failed" if something went wrong
                System.out.println("Entropy [" + (i + 1) + "]: " + (entropy != null ? entropy : "Failed"));
                Thread.sleep(2000); // wait 2 seconds before fetching again
            }
        } catch (Exception e) {
            e.printStackTrace(); // if anything crashes, print why
        }
    }

    // This function talks to the Flask server and gets the entropy
    private static String fetchEntropy() {
        try {
            // Convert string URL to URI then to URL (Java 20+ safe)
            URI uri = new URI("http://localhost:5000/entropy");
            URL url = uri.toURL();

            // Open connection
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET"); // we are just reading data

            // Read the server response
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            StringBuilder content = new StringBuilder();
            String line;
            while ((line = in.readLine()) != null) content.append(line);
            in.close(); // close the stream
            con.disconnect(); // disconnect to free resources

            // The server returns JSON like {"entropy":"<hash>"}
            // simple manual parse to get the hash
            String json = content.toString().trim();
            if (json.startsWith("{") && json.endsWith("}")) {
                int start = json.indexOf(":\"") + 2; // start of hash
                int end = json.indexOf("\"", start); // end of hash
                if (start > 1 && end > start) {
                    return json.substring(start, end); // return the actual hash
                }
            }

            return null; // if parsing failed, return null
        } catch (Exception e) {
            return null; // if connection fails, return null
        }
    }
}
