//9"
// Code to create web services for getting latest rates
package latestRate;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PUT;
import javax.ws.rs.core.MediaType;

/**
 * REST Web Service
 *
 * @author dayee
 */
@Path("latestRate")
public class LatestRate {

    String URL_latest = "http://api.exchangeratesapi.io/v1/latest?access_key=e7c5199d76f5fcaa506b259a0affd582";
    
    @Context
    private UriInfo context;

    /**
     * Creates a new instance of LatestRate
     */
    public LatestRate() {
    }

    /**
     * Retrieves representation of an instance of latestRate.LatestRate
     * @return an instance of java.lang.String
     */
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String getText() {
        //TODO return proper representation object
        StringBuilder st = new StringBuilder();
        try
        {
            URL url = new URL(URL_latest);
            HttpURLConnection url_connection = (HttpURLConnection) url.openConnection();
            url_connection.setRequestMethod("GET");
            BufferedReader br = new BufferedReader(new InputStreamReader(url_connection.getInputStream()));
            String output = "";
            while((output = br.readLine())!= null)
            {
                st.append(output + "\n");
            }
            
            br.close();
            
        } catch (Exception e) {
            e.printStackTrace();
        } 
        return st.toString();
    }

    /**
     * PUT method for updating or creating an instance of LatestRate
     * @param content representation for the resource
     */
    @PUT
    @Consumes(MediaType.TEXT_PLAIN)
    public void putText(String content) {
    }
}
