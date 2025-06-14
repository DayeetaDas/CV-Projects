//9"
// Code to create web services for converting currencies
package currConvert;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PUT;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;

/**
 * REST Web Service
 *
 * @author dayee
 */
@Path("currConvert")
public class CurrConvert {

    String convert = "http://localhost:8084/CurConvRS/webresources/exchangeRate";
    
    @Context
    private UriInfo context;

    /**
     * Creates a new instance of CurrConvert
     */
    public CurrConvert() {
    }

    /**
     * Retrieves representation of an instance of currConvert.CurrConvert
     * @return an instance of java.lang.String
     */
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String getText(@QueryParam("fromCur") String fromCur,
                          @QueryParam("toCur") String toCur) {
        //TODO return proper representation object
        String URL_convert = convert + "?fromCur=" + fromCur + "&toCur=" + toCur;
        StringBuilder str = new StringBuilder();
        try
        {
            URL url = new URL(URL_convert);
            HttpURLConnection url_connection = (HttpURLConnection) url.openConnection();
            url_connection.setRequestMethod("GET");
            BufferedReader br = new BufferedReader(new InputStreamReader(url_connection.getInputStream()));
            String output = "";
            while((output = br.readLine())!= null)
            {
                str.append(output + "\n");
            }
            
            br.close();
            
        } catch (Exception e) {
            e.printStackTrace();
        } 
        return str.toString();
    }

    /**
     * PUT method for updating or creating an instance of CurrConvert
     * @param content representation for the resource
     */
    @PUT
    @Consumes(MediaType.TEXT_PLAIN)
    public void putText(String content) {
    }
}
