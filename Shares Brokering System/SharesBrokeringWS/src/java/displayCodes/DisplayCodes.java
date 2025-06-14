//9"
// Code to create web services for displaying currency codes
package displayCodes;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Collections;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PUT;
import javax.ws.rs.core.MediaType;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

/**
 * REST Web Service
 *
 * @author dayee
 */
@Path("displayCodes")
public class DisplayCodes {
    
    String URL_code = "http://localhost:8084/CurConvRS/webresources/curCodes";
    
    @Context
    private UriInfo context;

    /**
     * Creates a new instance of DisplayCodes
     */
    public DisplayCodes() {
    }

    /**
     * Retrieves representation of an instance of displayCodes.DisplayCodes
     * @return an instance of java.lang.String
     */
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String getText() {
        //TODO return proper representation object
        
        StringBuilder st = new StringBuilder();
        StringBuilder str = new StringBuilder();
        try
        {
            URL url = new URL(URL_code);
            HttpURLConnection url_connection = (HttpURLConnection) url.openConnection();
            url_connection.setRequestMethod("GET");
            BufferedReader br = new BufferedReader(new InputStreamReader(url_connection.getInputStream()));
            String output = "";
            while((output = br.readLine())!= null)
            {
                st.append(output + "\n");
            }
            
            JSONParser parser = new JSONParser();
            String result = st.toString();
            JSONObject jsonObject = (JSONObject) parser.parse(result);
            JSONArray codes = (JSONArray)jsonObject.get("CurrConv");
            
            for(Object o : codes)
            {
                JSONObject company = (JSONObject) o;
                String name = (String)company.get("name");
                str.append(name + "\n");
                String code = (String)company.get("code");
                str.append(code + "\n");
                Double rate = (Double)company.get("rate");
                str.append(rate + "\n"); 
            }
            br.close();
            
        } catch (Exception e) {
            e.printStackTrace();
        } 
        return str.toString();
    }

    /**
     * PUT method for updating or creating an instance of DisplayCodes
     * @param content representation for the resource
     */
    @PUT
    @Consumes(MediaType.TEXT_PLAIN)
    public void putText(String content) {
    }
}
