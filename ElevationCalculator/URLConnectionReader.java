import java.net.*;
import java.io.*;
import org.json.*;

public class URLConnectionReader {
    //method to receive data in a string format from a server
    public static String getResponse(URL serverAddr) throws Exception {
        String myOverAllLine = new String();
        String inputLine = new String();
        try { //try to get data
            URLConnection yc = serverAddr.openConnection(); //open connection to server
            BufferedReader in = new BufferedReader(new InputStreamReader(yc.getInputStream())); //open and read buffer
            while ((inputLine = in.readLine()) != null) { //read data
                myOverAllLine = myOverAllLine + inputLine; //concatonate data together
            }
            in.close();
            return myOverAllLine; //return the data for processing
        } catch (Exception e) { //test for failure
            return "failure"; //give indication
        }
    }
    public static void main(String[] args) throws Exception {
        String address = new String();
        address = "SA65HN"; //enter address/ postcode here
        //get data from google servers
        URL latLonAPI = new URL("https://maps.googleapis.com/maps/api/geocode/json?address=+" + address+ "&key=AIzaSyCRrXIgyBIHSftKEuJj30WRCKKrRIVHt5Y");
        JSONObject myJ = new JSONObject(getResponse(latLonAPI)); //process json format
        JSONArray plcId = myJ.getJSONArray("results");
        JSONObject proc = plcId.getJSONObject(0);
        JSONObject myGeometry = proc.getJSONObject("geometry").getJSONObject("location");
        double lat = myGeometry.getDouble("lat"); //store the latitude and longitude
        double lng = myGeometry.getDouble("lng");

        //get elevation data from google server
        URL myElevation = new URL("https://maps.googleapis.com/maps/api/elevation/json?locations=" + lat+ "," + lng + "&key=AIzaSyBhVYWzw3pQNoNtS4bi5F2FpnEDes4Yek0");
        JSONObject receivedElev = new JSONObject(getResponse(myElevation)); //process json data
        JSONArray result = receivedElev.getJSONArray("results");
        JSONObject j = result.getJSONObject(0);
        double myElev = (j.getDouble("elevation")); //store the elevation

        System.out.println(myElev); //print elevation

    }
}
